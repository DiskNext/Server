from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    from pkg.conf.appmeta import BackendVersion
    response = client.get("/api/site/ping")
    assert response.status_code == 200
    assert response.json() == {
        "code": 0, 
        'data': BackendVersion, 
        'msg': None}