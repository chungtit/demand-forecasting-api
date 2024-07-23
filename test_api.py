from fastapi.testclient import TestClient
from forecast import app, api

client = TestClient(app)


def test_get_forecast():
    """
    Test the get_forecast endpoint to ensure it returns a forecast for the specified number of days.
    """
    with TestClient(app) as client:
        response = client.get("/v1/inference?days_to_forecast=30")
        assert response.status_code == 200
        assert len(response.json()) == 30


def test_update_data():
    """
    Test the update_data endpoint to ensure it updates the data and retrains the model.
    """
    with TestClient(app) as client:
        response = client.post(
            "/v1/update-data",
            files={
                "file": (
                    "data/data_training.csv",
                    open("data/data_training.csv", "rb"),
                    "text/csv",
                )
            },
        )
        assert response.status_code == 200
        assert response.json() == {
            "message": "Data updated and model retrained successfully"
        }
