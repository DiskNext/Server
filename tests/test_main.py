from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def is_valid_instance_id(instance_id):
    """Check if a string is a valid UUID4."""
    
    import uuid
    
    try:
        uuid.UUID(instance_id, version=4)
    except (ValueError, TypeError):
        assert False, f"instance_id is not a valid UUID4: {instance_id}"

def test_read_main():
    from pkg.conf.appmeta import BackendVersion
    
    response = client.get("/api/site/ping")
    json_response = response.json()
    
    assert response.status_code == 200
    assert json_response['code'] == 0
    assert json_response['data'] == BackendVersion
    assert json_response['msg'] is None
    assert 'instance_id' in json_response
    is_valid_instance_id(json_response['instance_id'])
        
    response = client.get("/api/site/config")
    json_response = response.json()
    
    assert response.status_code == 200
    assert json_response['code'] == 0
    assert json_response['data'] is not None
    assert json_response['msg'] is None
    assert 'instance_id' in json_response
    is_valid_instance_id(json_response['instance_id'])