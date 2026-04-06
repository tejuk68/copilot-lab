"""Tests for POST /activities/{activity_name}/signup endpoint"""

def test_signup_valid_activity(client, sample_email):
    """Test successful signup for valid activity"""
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "signed up" in data["message"].lower()
    assert sample_email in data["message"]


def test_signup_adds_participant(client, sample_email):
    """Test that signup adds email to participants list"""
    client.post("/activities/Chess Club/signup", params={"email": sample_email})
    response = client.get("/activities")
    data = response.json()
    assert sample_email in data["Chess Club"]["participants"]


def test_signup_multiple_emails(client):
    """Test signing up multiple different emails for same activity"""
    emails = ["alice@school.edu", "bob@school.edu", "charlie@school.edu"]
    for email in emails:
        response = client.post(f"/activities/Drama Club/signup", params={"email": email})
        assert response.status_code == 200

    response = client.get("/activities")
    data = response.json()
    assert len(data["Drama Club"]["participants"]) == 3
    assert set(data["Drama Club"]["participants"]) == set(emails)


def test_signup_activity_not_found(client, sample_email):
    """Test signup for non-existent activity returns 404"""
    response = client.post(
        "/activities/Nonexistent Club/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_email(client, sample_email):
    """Test that duplicate signup is prevented"""
    # First signup
    client.post("/activities/Chess Club/signup", params={"email": sample_email})
    # Second signup should fail
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_case_sensitive_activity_name(client, sample_email):
    """Test that activity name is case-sensitive"""
    response = client.post(
        "/activities/chess club/signup",  # lowercase
        params={"email": sample_email}
    )
    assert response.status_code == 404  # Should not find "chess club"


def test_signup_all_activities(client, sample_email):
    """Test that user can signup for all activities"""
    activities_list = [
        "Chess Club", "Robotics Team", "Drama Club", "Basketball Team",
        "Soccer Club", "Art Club", "Music Band", "Debate Club", "Science Club"
    ]
    for activity in activities_list:
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200

    # Verify user is in all activities
    response = client.get("/activities")
    data = response.json()
    for activity in activities_list:
        assert sample_email in data[activity]["participants"]


def test_signup_empty_email(client):
    """Test signup with empty email"""
    response = client.post("/activities/Chess Club/signup", params={"email": ""})
    # The app currently allows empty email
    assert response.status_code == 200
    response_get = client.get("/activities")
    data = response_get.json()
    assert "" in data["Chess Club"]["participants"]


def test_signup_special_characters_email(client):
    """Test signup with email containing special characters"""
    special_email = "test+tag@example.com"
    response = client.post("/activities/Chess Club/signup", params={"email": special_email})
    assert response.status_code == 200
    response_get = client.get("/activities")
    data = response_get.json()
    assert special_email in data["Chess Club"]["participants"]


def test_signup_then_get_integration(client, sample_email):
    """Integration test: signup then verify in GET /activities"""
    # Signup
    client.post("/activities/Chess Club/signup", params={"email": sample_email})
    # Get activities
    response = client.get("/activities")
    data = response.json()
    assert sample_email in data["Chess Club"]["participants"]
    assert len(data["Chess Club"]["participants"]) == 1


def test_multiple_activities_same_user_integration(client, sample_email):
    """Integration test: user signs up for multiple activities"""
    activities = ["Chess Club", "Drama Club", "Science Club"]
    for activity in activities:
        client.post(f"/activities/{activity}/signup", params={"email": sample_email})

    response = client.get("/activities")
    data = response.json()
    for activity in activities:
        assert sample_email in data[activity]["participants"]
        assert len(data[activity]["participants"]) == 1


def test_signup_state_persistence_integration(client):
    """Integration test: state persists across multiple requests"""
    emails = ["user1@school.edu", "user2@school.edu"]
    # Signup two users
    for email in emails:
        client.post("/activities/Chess Club/signup", params={"email": email})

    # Simulate multiple GET requests
    for _ in range(3):
        response = client.get("/activities")
        data = response.json()
        assert len(data["Chess Club"]["participants"]) == 2
        assert set(data["Chess Club"]["participants"]) == set(emails)