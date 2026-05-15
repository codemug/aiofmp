"""CLI subcommands for the harvester."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

import click

from aiofmp import FmpClient
from aiofmp.cachedclient import CachedClient
from aiofmp.harvester import categories  # noqa: F401  — triggers registration imports
from aiofmp.harvester.config import (
    HarvestConfig,
    load_config_from_yaml,
)
from aiofmp.harvester.manager import HarvesterManager

logger = logging.getLogger(__name__)


def _resolve_api_key(api_key_opt: str | None) -> str:
    key = api_key_opt or os.environ.get("FMP_API_KEY")
    if not key:
        click.echo(
            "error: FMP_API_KEY env var or --api-key option is required", err=True
        )
        sys.exit(2)
    return key


def _build_cached_client(api_key: str) -> tuple[FmpClient, CachedClient]:
    """Build a real FmpClient + CachedClient pair. Patched in tests."""
    fmp = FmpClient(api_key=api_key)
    cached = CachedClient(fmp)
    return fmp, cached


def _print_dry_run_plan(cfg: HarvestConfig, restrict_to: str | None) -> None:
    click.echo(f"state_dir: {cfg.state_dir}")
    click.echo(
        f"budget: soft={cfg.budget.monthly_soft_cap_gb}GB hard={cfg.budget.monthly_hard_cap_gb}GB"
    )
    click.echo("")
    click.echo(f"{'category':30s} {'enabled':8s} {'interval':10s}")
    click.echo("-" * 50)
    for name, cat in cfg.categories.items():
        if restrict_to and name != restrict_to:
            continue
        flag = "yes" if cat.enabled else "no"
        click.echo(f"{name:30s} {flag:8s} {cat.interval:10s}")


async def _run_once(
    cfg: HarvestConfig,
    api_key: str,
    restrict_to: str | None,
) -> int:
    fmp, cached = _build_cached_client(api_key)
    rc = 0
    async with cached:
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=cached)
        await mgr.start()
        targets = list(mgr._categories.keys())
        if restrict_to:
            targets = [t for t in targets if t == restrict_to]
            if not targets:
                click.echo(
                    f"error: category {restrict_to!r} not enabled in config", err=True
                )
                return 2
        for name in targets:
            await mgr._categories[name]._run_once_and_record()
            run = mgr.state.get_latest_run(name)
            status = run.status.value if run else "missing"
            items = run.items_attempted if run else 0
            ok = run.items_succeeded if run else 0
            click.echo(f"{name:30s} {status:20s} {ok}/{items} items")
            if run and run.error:
                rc = 1
        await mgr.close()
    return rc


async def _run_forever(cfg: HarvestConfig, api_key: str) -> int:
    fmp, cached = _build_cached_client(api_key)
    async with cached:
        mgr = HarvesterManager(cfg, fmp_client=fmp, cached_client=cached)
        await mgr.start()
        mgr.install_signal_handlers()
        try:
            await mgr.run_until_stopped()
        finally:
            await mgr.close()
    return 0


@click.command("harvest")
@click.option(
    "--config",
    "config_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
@click.option(
    "--once", is_flag=True, help="Run each enabled category's next-due cycle and exit."
)
@click.option(
    "--category",
    "category_name",
    default=None,
    help="Restrict to a single category (with --once).",
)
@click.option("--dry-run", is_flag=True, help="Print the plan; fetch nothing.")
@click.option("--api-key", default=None, help="Override FMP_API_KEY env var.")
def harvest(
    config_path: str,
    once: bool,
    category_name: str | None,
    dry_run: bool,
    api_key: str | None,
) -> None:
    """Run the aiofmp harvester."""
    cfg = load_config_from_yaml(config_path)
    logging.basicConfig(level=getattr(logging, cfg.log_level.upper(), logging.INFO))

    if dry_run:
        _print_dry_run_plan(cfg, restrict_to=category_name)
        sys.exit(0)

    key = _resolve_api_key(api_key)
    if once:
        rc = asyncio.run(_run_once(cfg, key, restrict_to=category_name))
        sys.exit(rc)
    else:
        rc = asyncio.run(_run_forever(cfg, key))
        sys.exit(rc)


@click.command("harvest-status")
@click.option(
    "--config",
    "config_path",
    required=True,
    type=click.Path(exists=True, dir_okay=False),
)
def harvest_status(config_path: str) -> None:
    """Print a tabular summary of the harvester state store."""
    cfg = load_config_from_yaml(config_path)
    state_dir = Path(os.path.expanduser(cfg.state_dir))
    from aiofmp.harvester.state import StateStore

    store = StateStore(state_dir / "harvester.sqlite")
    store.initialize()

    click.echo(f"{'category':30s} {'status':20s} {'finished_at':30s} {'items':10s}")
    click.echo("-" * 95)
    for name in sorted(cfg.categories.keys()):
        run = store.get_latest_run(name)
        if run is None:
            click.echo(f"{name:30s} {'never_ran':20s} {'-':30s} {'-':10s}")
            continue
        items = f"{run.items_succeeded}/{run.items_attempted}"
        finished = run.finished_at or "(running)"
        click.echo(f"{name:30s} {run.status.value:20s} {finished:30s} {items:10s}")
