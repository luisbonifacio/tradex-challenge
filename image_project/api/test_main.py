from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_send_null_image():
    response = client.post(
        "/image/",
        headers={"X-Token": "test"},
        json={
            ""
        },
    )
    assert response.status_code == 203
    assert response.json() == {
        "detail": "No Content found. Please send a valid base64 image."}
