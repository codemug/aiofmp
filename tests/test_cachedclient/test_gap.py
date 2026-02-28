"""Tests for the gap detection module."""

from datetime import date

import pytest

from aiofmp.cachedclient.gap import (
    DateParamType,
    DateRange,
    compute_gaps,
    denormalize_from_date,
    normalize_to_date,
    parse_response_date,
)


class TestDateRange:
    def test_valid_range(self):
        dr = DateRange(start=date(2020, 1, 1), end=date(2020, 12, 31))
        assert dr.start == date(2020, 1, 1)
        assert dr.end == date(2020, 12, 31)

    def test_same_date_range(self):
        dr = DateRange(start=date(2020, 6, 15), end=date(2020, 6, 15))
        assert dr.start == dr.end

    def test_invalid_range_raises(self):
        with pytest.raises(ValueError, match="must be <="):
            DateRange(start=date(2020, 12, 31), end=date(2020, 1, 1))


class TestComputeGaps:
    def test_no_stored_data(self):
        """No stored data -> full requested range returned."""
        requested = DateRange(date(2020, 1, 1), date(2024, 12, 31))
        gaps = compute_gaps(requested, None, None)
        assert len(gaps) == 1
        assert gaps[0] == requested

    def test_stored_covers_fully(self):
        """Stored range fully covers requested -> no gaps."""
        requested = DateRange(date(2021, 1, 1), date(2023, 12, 31))
        gaps = compute_gaps(requested, date(2020, 1, 1), date(2024, 12, 31))
        assert gaps == []

    def test_stored_exactly_matches(self):
        """Stored range exactly matches requested -> no gaps."""
        requested = DateRange(date(2020, 1, 1), date(2024, 12, 31))
        gaps = compute_gaps(requested, date(2020, 1, 1), date(2024, 12, 31))
        assert gaps == []

    def test_gap_on_right(self):
        """Stored: [2020-2023], Requested: [2020-2025] -> gap [2024-2025]."""
        requested = DateRange(date(2020, 1, 1), date(2025, 12, 31))
        gaps = compute_gaps(requested, date(2020, 1, 1), date(2023, 12, 31))
        assert len(gaps) == 1
        assert gaps[0].start == date(2024, 1, 1)
        assert gaps[0].end == date(2025, 12, 31)

    def test_gap_on_left(self):
        """Stored: [2022-2025], Requested: [2020-2025] -> gap [2020-2021]."""
        requested = DateRange(date(2020, 1, 1), date(2025, 12, 31))
        gaps = compute_gaps(requested, date(2022, 1, 1), date(2025, 12, 31))
        assert len(gaps) == 1
        assert gaps[0].start == date(2020, 1, 1)
        assert gaps[0].end == date(2021, 12, 31)

    def test_gaps_on_both_sides(self):
        """Stored: [2022-2023], Requested: [2020-2025] -> two gaps."""
        requested = DateRange(date(2020, 1, 1), date(2025, 12, 31))
        gaps = compute_gaps(requested, date(2022, 1, 1), date(2023, 12, 31))
        assert len(gaps) == 2
        # Left gap
        assert gaps[0].start == date(2020, 1, 1)
        assert gaps[0].end == date(2021, 12, 31)
        # Right gap
        assert gaps[1].start == date(2024, 1, 1)
        assert gaps[1].end == date(2025, 12, 31)

    def test_stored_is_subset_of_requested(self):
        """Stored range is inside requested range -> gaps on both sides."""
        requested = DateRange(date(2020, 1, 1), date(2024, 12, 31))
        gaps = compute_gaps(requested, date(2021, 6, 1), date(2023, 6, 1))
        assert len(gaps) == 2
        assert gaps[0].end == date(2021, 5, 31)
        assert gaps[1].start == date(2023, 6, 2)

    def test_stored_completely_before_requested(self):
        """Stored ends before requested starts -> full request is a gap."""
        requested = DateRange(date(2024, 1, 1), date(2025, 12, 31))
        gaps = compute_gaps(requested, date(2020, 1, 1), date(2022, 12, 31))
        assert len(gaps) == 1
        assert gaps[0] == requested

    def test_stored_completely_after_requested(self):
        """Stored starts after requested ends -> full request is a gap."""
        requested = DateRange(date(2020, 1, 1), date(2021, 12, 31))
        gaps = compute_gaps(requested, date(2023, 1, 1), date(2025, 12, 31))
        assert len(gaps) == 1
        assert gaps[0] == requested


class TestNormalizeToDate:
    def test_none(self):
        assert normalize_to_date(None, DateParamType.STRING) is None

    def test_string(self):
        result = normalize_to_date("2024-06-15", DateParamType.STRING)
        assert result == date(2024, 6, 15)

    def test_date_object(self):
        d = date(2024, 6, 15)
        result = normalize_to_date(d, DateParamType.DATE_OBJ)
        assert result == d

    def test_string_with_datetime_suffix(self):
        result = normalize_to_date("2024-06-15 10:30:00", DateParamType.STRING)
        assert result == date(2024, 6, 15)


class TestDenormalizeFromDate:
    def test_string_type(self):
        result = denormalize_from_date(date(2024, 6, 15), DateParamType.STRING)
        assert result == "2024-06-15"
        assert isinstance(result, str)

    def test_date_type(self):
        d = date(2024, 6, 15)
        result = denormalize_from_date(d, DateParamType.DATE_OBJ)
        assert result == d
        assert isinstance(result, date)


class TestParseResponseDate:
    def test_date_only(self):
        assert parse_response_date("2024-06-15") == date(2024, 6, 15)

    def test_datetime(self):
        assert parse_response_date("2024-06-15 10:30:00") == date(2024, 6, 15)
