class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
            "Soccer Club", "Art Studio", "Music Band", "Debate Club", "Science Club"
        ]

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for activity in expected_activities:
            assert activity in data

    def test_get_activities_response_structure(self, client):
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        for name, details in response.json().items():
            assert required_fields.issubset(details.keys()), (
                f"Activity '{name}' is missing required fields"
            )


class TestSignup:
    def test_signup_success(self, client):
        # Arrange
        activity = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_signup_duplicate_email_fails(self, client):
        # Arrange
        activity = "Chess Club"
        email = "duplicate@mergington.edu"
        client.post(f"/activities/{activity}/signup?email={email}")

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert "already" in response.json()["detail"].lower()

    def test_signup_activity_not_found(self, client):
        # Arrange
        activity = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        assert response.status_code == 404

    def test_signup_adds_email_to_participants(self, client):
        # Arrange
        activity = "Chess Club"
        email = "verify@mergington.edu"

        # Act
        client.post(f"/activities/{activity}/signup?email={email}")

        # Assert
        activities = client.get("/activities").json()
        assert email in activities[activity]["participants"]


class TestUnregister:
    def test_unregister_success(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # pre-seeded participant

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 200
        assert email in response.json()["message"]

    def test_unregister_not_registered_fails(self, client):
        # Arrange
        activity = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"].lower()

    def test_unregister_activity_not_found(self, client):
        # Arrange
        activity = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        assert response.status_code == 404

    def test_unregister_removes_email_from_participants(self, client):
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # pre-seeded participant

        # Act
        client.delete(f"/activities/{activity}/unregister?email={email}")

        # Assert
        activities = client.get("/activities").json()
        assert email not in activities[activity]["participants"]


class TestRoot:
    def test_root_redirects_to_static_index(self, client):
        # Arrange
        # client is configured with follow_redirects=False in conftest

        # Act
        response = client.get("/")

        # Assert
        assert response.status_code in (301, 302, 307, 308)
        assert response.headers["location"] == "/static/index.html"
