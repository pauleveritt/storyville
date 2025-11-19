"""Tests for pytest plugin configuration handling."""

import pytest


def test_config_reads_enabled_from_ini(pytestconfig: pytest.Config):
    """Test reading enabled setting from pytest config."""
    enabled: bool = pytestconfig.getini("storytime_enabled")

    assert isinstance(enabled, bool)
    # Default should be True
    assert enabled is True


def test_config_enabled_defaults_to_true(pytestconfig: pytest.Config):
    """Test that enabled setting defaults to True."""
    enabled: bool = pytestconfig.getini("storytime_enabled")
    assert enabled is True


def test_plugin_is_loaded(pytestconfig: pytest.Config):
    """Test that the storytime plugin is loaded."""
    assert pytestconfig.pluginmanager.has_plugin("storytime")
