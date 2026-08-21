"""
Unit tests for FMPBaseClient session lifecycle.

Regression coverage for the shared-session concurrency race: the MCP server
reuses a single global client that many in-flight requests enter concurrently
via ``async with client:``. The first scope to exit must NOT close the session
out from under the others (which produced "Connector is closed" and
"'NoneType' object has no attribute 'get'" in production).
"""

import asyncio
from unittest.mock import AsyncMock, patch

import pytest

from aiofmp.base import FMPBaseClient


class _FakeSession:
    """Minimal stand-in for aiohttp.ClientSession that tracks close()."""

    instances: list["_FakeSession"] = []

    def __init__(self, *args, **kwargs):
        self.closed = False
        _FakeSession.instances.append(self)

    async def close(self):
        self.closed = True


@pytest.fixture(autouse=True)
def _reset_fake_sessions():
    _FakeSession.instances.clear()
    yield
    _FakeSession.instances.clear()


class _CapturingSession:
    """Session stand-in that records the query params handed to aiohttp."""

    def __init__(self):
        self.sent: list[dict] = []

    def get(self, url, params=None, headers=None):
        self.sent.append(dict(params or {}))

        class _Ctx:
            async def __aenter__(self_inner):
                return object()

            async def __aexit__(self_inner, *a):
                return False

        return _Ctx()

    async def close(self):
        pass


class TestQueryParamNormalization:
    """aiohttp/yarl raise on bool and None query values, so a boolean filter had
    to be normalized before it reached the request or it could never be sent."""

    @pytest.mark.asyncio
    async def test_bools_become_lowercase_strings_and_none_is_dropped(self):
        client = FMPBaseClient(api_key="test-key")
        session = _CapturingSession()
        client._session = session

        async def _ok(response):
            return []

        client._handle_response = _ok

        await client._make_request(
            "company-screener",
            {
                "isEtf": False,
                "isActivelyTrading": True,
                "exchange": "NASDAQ",
                "limit": 10,
                "sector": None,
            },
        )

        sent = session.sent[0]
        assert sent["isEtf"] == "false", "False must survive as the string FMP expects"
        assert sent["isActivelyTrading"] == "true"
        assert sent["exchange"] == "NASDAQ"  # strings pass through untouched
        assert sent["limit"] == 10  # ints pass through untouched
        assert "sector" not in sent  # an unset filter is simply not sent
        assert sent["apikey"] == "test-key"
        assert not any(isinstance(v, bool) for v in sent.values())


class TestSessionLifecycle:
    """Reference-counted start()/close() for safe concurrent use."""

    @pytest.mark.asyncio
    async def test_overlapping_scopes_share_one_session(self):
        client = FMPBaseClient(api_key="test")
        with patch("aiofmp.base.aiohttp.ClientSession", _FakeSession):
            await client.start()  # scope A enters
            session = client._session
            assert session is not None

            await client.start()  # scope B enters (concurrent)
            assert client._session is session  # reuse, not a second session
            assert len(_FakeSession.instances) == 1

            # Scope A exits — session MUST survive for still-active scope B.
            await client.close()
            assert client._session is session
            assert session.closed is False

            # Scope B exits — last user gone, now it closes.
            await client.close()
            assert client._session is None
            assert session.closed is True

    @pytest.mark.asyncio
    async def test_new_session_created_after_full_drain(self):
        client = FMPBaseClient(api_key="test")
        with patch("aiofmp.base.aiohttp.ClientSession", _FakeSession):
            await client.start()
            first = client._session
            await client.close()
            assert client._session is None

            # A later request re-opens a fresh session.
            await client.start()
            assert client._session is not None
            assert client._session is not first
            await client.close()

    @pytest.mark.asyncio
    async def test_concurrent_enter_exit_keeps_session_alive_mid_flight(self):
        """Mimics repro: many concurrent `async with` scopes, one shared client."""
        client = FMPBaseClient(api_key="test")
        observed_closed_mid_request = []

        with patch("aiofmp.base.aiohttp.ClientSession", _FakeSession):

            async def one_request():
                async with client:  # start() / close()
                    # Yield control so other scopes interleave enter/exit here.
                    await asyncio.sleep(0)
                    # The session we're about to "use" must be open.
                    observed_closed_mid_request.append(client._session is None)
                    await asyncio.sleep(0)

            await asyncio.gather(*[one_request() for _ in range(20)])

        # No request ever saw a torn-down session while inside its own scope.
        assert not any(observed_closed_mid_request)
        # And everything is cleaned up after the last scope exits.
        assert client._session is None


# --- HTTP 429 is two different conditions ------------------------------------


class _Resp:
    """Minimal stand-in for aiohttp's response, enough for _handle_response."""

    def __init__(self, status, body=""):
        self.status = status
        self._body = body

    async def text(self):
        return self._body

    async def read(self):
        return self._body.encode()


@pytest.mark.asyncio
async def test_a_bandwidth_429_is_not_a_rate_limit_error():
    """FMP overloads 429, and only the body distinguishes the two.

    A per-minute limit clears in seconds and is worth retrying. An exhausted
    rolling BYTE allowance persists until the window rolls, so the transparent
    retry loop can never succeed -- a real deployment sat in it for ten hours
    at 5s/10s/20s, fetching nothing.
    """
    from aiofmp.base import FMPBandwidthError, FMPBaseClient, FMPRateLimitError

    client = FMPBaseClient(api_key="k")
    body = '{"Error Message": "Bandwidth Limit Reach . Please upgrade your plan"}'
    with pytest.raises(FMPBandwidthError):
        await client._handle_response(_Resp(429, body))

    # It must NOT be catchable as a rate-limit error, or the retry loop's
    # `except FMPRateLimitError` arm swallows it again.
    assert not issubclass(FMPBandwidthError, FMPRateLimitError)


@pytest.mark.asyncio
async def test_a_per_minute_429_is_still_a_rate_limit_error():
    """The transparent retry path must keep working for the transient case."""
    from aiofmp.base import FMPBaseClient, FMPRateLimitError

    client = FMPBaseClient(api_key="k")
    body = '{"Error Message": "Limit Reach . Please upgrade your plan"}'
    with pytest.raises(FMPRateLimitError):
        await client._handle_response(_Resp(429, body))


@pytest.mark.asyncio
async def test_an_unreadable_429_body_falls_back_to_rate_limit():
    """A body we cannot read must not become a permanent failure: the transient
    reading is the safe default, since it only costs a retry."""
    from aiofmp.base import FMPBaseClient, FMPRateLimitError

    class _Broken(_Resp):
        async def text(self):
            raise RuntimeError("connection closed")

    client = FMPBaseClient(api_key="k")
    with pytest.raises(FMPRateLimitError):
        await client._handle_response(_Broken(429))


@pytest.mark.asyncio
async def test_the_retry_loop_gives_up_immediately_on_a_bandwidth_429():
    """The behaviour the whole distinction exists for.

    `except FMPRateLimitError` must not catch it, so the request is attempted
    ONCE and the error reaches the caller instead of looping 5s/10s/20s against
    an allowance that cannot come back for days.
    """
    from aiofmp.base import FMPBandwidthError, FMPBaseClient, FMPRateLimitError

    client = FMPBaseClient(api_key="k", max_retries=3)
    client._session = _CapturingSession()
    attempts = []

    async def _bandwidth(_response):
        attempts.append(1)
        raise FMPBandwidthError("exhausted")

    client._handle_response = _bandwidth
    with pytest.raises(FMPBandwidthError):
        await client._make_request("profile", {"symbol": "AAPL"})
    assert len(attempts) == 1, "a bandwidth 429 must not be retried"

    # The transient sibling still retries, so the fix is a split and not a
    # blanket removal of 429 handling.
    client2 = FMPBaseClient(api_key="k", max_retries=2)
    client2._session = _CapturingSession()
    tries = []

    async def _ratelimited(_response):
        tries.append(1)
        raise FMPRateLimitError("slow down")

    client2._handle_response = _ratelimited
    client2.retry_delay = 0
    with patch("asyncio.sleep", new=AsyncMock()):
        with pytest.raises(FMPRateLimitError):
            await client2._make_request("profile", {"symbol": "AAPL"})
    assert len(tries) == 3, "a per-minute limit keeps its transparent retries"
