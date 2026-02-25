from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_root_redirects_to_static():
    # Arrange: client already available
    # Act (don't follow redirects so we can inspect the response)
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code in (307, 308)
    assert "/static/index.html" in response.headers["location"]


def test_get_activities_returns_db():
    # Arrange: we know the in-memory activities dict
    expected = activities
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert response.json() == expected


def test_signup_and_unregister_flow():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act: sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert sign up succeeded and email added
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

    # Act: unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert unregister succeeded and email removed
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent():
    # Arrange
    activity = "Chess Club"
    email = "nobody@mergington.edu"

    # make sure not signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 400


def test_unregister_invalid_activity():
    # Arrange
    invalid = "Unknown"
    email = "a@a.com"

    # Act
    response = client.post(f"/activities/{invalid}/unregister", params={"email": email})
    # Assert
    assert response.status_code == 404
