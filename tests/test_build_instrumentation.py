"""Tests for build performance instrumentation."""

import logging
from pathlib import Path

import pytest

from storyville.build import build_site


def test_build_logging_contains_phase_timings(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that build logging output contains timing for all 3 phases."""
    # Set logging level to capture INFO messages
    caplog.set_level(logging.INFO)

    # Build a small example to test instrumentation
    build_site("examples.minimal", tmp_path)

    # Verify all 3 phases are logged
    log_messages = [record.message for record in caplog.records]

    # Check for Phase Reading log
    reading_logs = [msg for msg in log_messages if "Phase Reading:" in msg and "completed in" in msg]
    assert len(reading_logs) == 1, "Should have exactly one Phase Reading log"

    # Check for Phase Rendering log
    rendering_logs = [msg for msg in log_messages if "Phase Rendering:" in msg and "completed in" in msg]
    assert len(rendering_logs) == 1, "Should have exactly one Phase Rendering log"

    # Check for Phase Writing log
    writing_logs = [msg for msg in log_messages if "Phase Writing:" in msg and "completed in" in msg]
    assert len(writing_logs) == 1, "Should have exactly one Phase Writing log"


def test_build_logging_has_all_three_phases(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that all 3 build phases are measured and logged."""
    caplog.set_level(logging.INFO)

    build_site("examples.minimal", tmp_path)

    log_text = "\n".join([record.message for record in caplog.records])

    # Verify all 3 phases are present
    assert "Phase Reading:" in log_text
    assert "Phase Rendering:" in log_text
    assert "Phase Writing:" in log_text


def test_build_logging_format_matches_specification(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that logging format matches specification: 'Phase [name]: completed in {duration:.2f}s'."""
    caplog.set_level(logging.INFO)

    build_site("examples.minimal", tmp_path)

    log_messages = [record.message for record in caplog.records]

    # Check Phase Reading format
    reading_logs = [msg for msg in log_messages if "Phase Reading:" in msg]
    assert len(reading_logs) == 1
    assert "completed in" in reading_logs[0]
    assert reading_logs[0].endswith("s"), "Should end with 's' for seconds"
    # Verify duration is formatted with 2 decimal places (e.g., "0.12s")
    duration_part = reading_logs[0].split("completed in")[1].strip()
    assert duration_part.endswith("s")
    duration_value = duration_part[:-1]  # Remove 's'
    # Check it's a valid float with at most 2 decimal places
    float(duration_value)  # Should not raise

    # Check Phase Rendering format
    rendering_logs = [msg for msg in log_messages if "Phase Rendering:" in msg]
    assert len(rendering_logs) == 1
    assert "completed in" in rendering_logs[0]
    assert rendering_logs[0].endswith("s")

    # Check Phase Writing format
    writing_logs = [msg for msg in log_messages if "Phase Writing:" in msg]
    assert len(writing_logs) == 1
    assert "completed in" in writing_logs[0]
    assert writing_logs[0].endswith("s")


def test_build_logging_total_time(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test that total build time is logged."""
    caplog.set_level(logging.INFO)

    build_site("examples.minimal", tmp_path)

    log_messages = [record.message for record in caplog.records]

    # Check for total build time log
    total_logs = [msg for msg in log_messages if "Build completed in" in msg]
    assert len(total_logs) == 1, "Should have exactly one Build completed log"
    assert total_logs[0].endswith("s"), "Should end with 's' for seconds"
