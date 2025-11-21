import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    """Test the home endpoint returns success"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert 'message' in data

def test_health_endpoint(client):
    """Test the health endpoint (may fail occasionally)"""
    response = client.get('/health')
    # Accept both healthy and unhealthy responses
    assert response.status_code in [200, 503]
    data = response.get_json()
    assert 'status' in data

def test_data_endpoint(client):
    """Test the data endpoint returns proper structure"""
    response = client.get('/api/data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'users' in data
    assert 'active_sessions' in data
    assert 'uptime_percentage' in data
    assert isinstance(data['users'], int)

def test_calculate_endpoint(client):
    """Test the calculate endpoint with various inputs"""
    test_cases = [
        (5, 20),   # 5 * 2 + 10 = 20
        (0, 10),   # 0 * 2 + 10 = 10
        (10, 30),  # 10 * 2 + 10 = 30
    ]
    for input_val, expected in test_cases:
        response = client.get(f'/api/calculate/{input_val}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['result'] == expected

def test_invalid_endpoint(client):
    """Test that invalid endpoints return 404"""
    response = client.get('/api/invalid')
    assert response.status_code == 404
