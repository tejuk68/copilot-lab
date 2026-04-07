"""Tests for GET /activities endpoint"""

def test_get_all_activities(client):
    """Test that GET /activities returns all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Science Club" in data


def test_get_activities_structure(client):
    """Test that each activity has required fields"""
    response = client.get("/activities")
    data = response.json()
    for activity_name, activity_data in data.items():
        assert "description" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["participants"], list)


def test_get_activities_empty_participants(client):
    """Test that all activities start with empty participants lists"""
    response = client.get("/activities")
    data = response.json()
    for activity_name, activity_data in data.items():
        assert activity_data["participants"] == []


def test_get_activities_specific_content(client):
    """Test specific activity content"""
    response = client.get("/activities")
    data = response.json()
    assert data["Chess Club"]["description"] == "A club for students who enjoy playing chess."
    assert data["Robotics Team"]["description"] == "Design and build robots to compete in local and national competitions."