"""Gap detection for the cached client.

Computes which date ranges need to be fetched from the upstream API
given what's already stored locally.
"""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from enum import Enum


class DateParamType(str, Enum):
    """How date parameters are typed in the SDK method signature."""

    STRING = "string"  # from_date: str ("YYYY-MM-DD")
    DATE_OBJ = "date"  # from_date: datetime.date


@dataclass(frozen=True)
class DateRange:
    """An inclusive date range [start, end]."""

    start: date
    end: date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError(
                f"DateRange start ({self.start}) must be <= end ({self.end})"
            )


def compute_gaps(
    requested: DateRange,
    stored_min: date | None,
    stored_max: date | None,
) -> list[DateRange]:
    """Compute date range gaps that need to be fetched from the API.

    Given a requested date range and the min/max dates of stored data,
    returns 0, 1, or 2 DateRange objects representing gaps.

    Args:
        requested: The date range the caller wants.
        stored_min: Earliest date in local storage (None if no data stored).
        stored_max: Latest date in local storage (None if no data stored).

    Returns:
        List of DateRange gaps to fetch. Empty if storage fully covers the request.
    """
    if stored_min is None or stored_max is None:
        return [requested]

    gaps: list[DateRange] = []

    # Gap on the left: request starts before stored data
    if requested.start < stored_min:
        gap_end = min(stored_min - timedelta(days=1), requested.end)
        if gap_end >= requested.start:
            gaps.append(DateRange(start=requested.start, end=gap_end))

    # Gap on the right: request ends after stored data
    if requested.end > stored_max:
        gap_start = max(stored_max + timedelta(days=1), requested.start)
        if gap_start <= requested.end:
            gaps.append(DateRange(start=gap_start, end=requested.end))

    return gaps


def normalize_to_date(
    value: str | date | None, param_type: DateParamType
) -> date | None:
    """Convert a date parameter value to a date object.

    Args:
        value: The raw value from the caller (str or date or None).
        param_type: How the SDK method declares this parameter.

    Returns:
        A date object, or None if the value is None.
    """
    if value is None:
        return None
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        return date.fromisoformat(value[:10])
    raise TypeError(f"Cannot normalize {type(value)} to date")


def denormalize_from_date(value: date, param_type: DateParamType) -> str | date:
    """Convert a date object back to the format expected by the SDK method.

    Args:
        value: A date object.
        param_type: How the SDK method declares the date parameter.

    Returns:
        A string or date object matching the SDK's expected type.
    """
    if param_type == DateParamType.DATE_OBJ:
        return value
    return value.isoformat()


def parse_response_date(date_str: str) -> date:
    """Parse a date string from an API response to a date object.

    Handles both "YYYY-MM-DD" and "YYYY-MM-DD HH:MM:SS" formats.
    """
    return date.fromisoformat(str(date_str)[:10])
