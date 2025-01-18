from fastapi.testclient import TestClient

from builder.server import app

#client = TestClient(app=app)


def test_get_config_status():
    with TestClient(app=app) as client:
        response = client.get("/config")
        assert response.status_code == 200
        assert response.json() == {"db_url": "sqlite:///microant_test.db"}