from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_signup_and_unregister_flow():
    # choose a known activity
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # ensure not already signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

    # unregister
    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent():
    activity = "Chess Club"
    email = "nobody@mergington.edu"

    # make sure not signed up
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    response = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert response.status_code == 400


def test_unregister_invalid_activity():
    response = client.post(f"/activities/Unknown/unregister", params={"email": "a@a.com"})
    assert response.status_code == 404
