import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

# Initial activities data for testing
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "A club for students who enjoy playing chess.",
        "participants": []
    },
    "Robotics Team": {
        "description": "Design and build robots to compete in local and national competitions.",
        "participants": []
    },
    "Drama Club": {
        "description": "Perform plays and skits throughout the school year.",
        "participants": []
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball games and tournaments.",
        "participants": []
    },
    "Soccer Club": {
        "description": "Train for soccer matches and improve teamwork skills.",
        "participants": []
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts.",
        "participants": []
    },
    "Music Band": {
        "description": "Form a band to play instruments and perform music.",
        "participants": []
    },
    "Debate Club": {
        "description": "Engage in debates on various topics to build critical thinking.",
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and learn about scientific principles.",
        "participants": []
    }
}


@pytest.fixture
def client():
    """FastAPI test client with fresh activities state"""
    activities.clear()
    for key, value in INITIAL_ACTIVITIES.items():
        activities[key] = {'description': value['description'], 'participants': []}
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Not needed anymore, reset is in client"""
    pass


@pytest.fixture
def sample_email():
    """Sample email for testing"""
    return "student@mergington.edu"