from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    from pkg.conf.appmeta import BackendVersion
    import uuid
    
    response = client.get("/api/site/ping")
    json_response = response.json()
    
    assert response.status_code == 200
    assert json_response['code'] == 0
    assert json_response['data'] == BackendVersion
    assert json_response['msg'] is None
    assert 'instance_id' in json_response
    try:
        uuid.UUID(json_response['instance_id'], version=4)
    except (ValueError, TypeError):
        assert False, f"instance_id is not a valid UUID4: {json_response['instance_id']}"