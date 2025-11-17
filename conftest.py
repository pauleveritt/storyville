"""Global pytest configuration."""

import pytest


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure anyio to use asyncio backend only."""
    return "asyncio"
