import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities as original_activities


@pytest.fixture
def client():
    """Provide a TestClient with a fresh copy of activities for each test."""
    # Store original state
    original_state = copy.deepcopy(original_activities)

    yield TestClient(app, follow_redirects=False)

    # Restore original state after each test
    original_activities.clear()
    original_activities.update(original_state)
