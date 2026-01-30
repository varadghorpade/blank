import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the page loads and authors are present."""
    rv = client.get('/')
    assert b"Subnet Calculator" in rv.data
    assert b"Shyam Borole" in rv.data
    assert b"Devansh Naik" in rv.data

def test_subnet_calculation(client):
    """Test a valid subnet calculation."""
    rv = client.post('/', data={'ip_address': '192.168.1.10', 'cidr': '24'})
    assert b"192.168.1.0" in rv.data  # Network ID
    assert b"192.168.1.255" in rv.data # Broadcast IP

def test_invalid_input(client):
    """Test invalid input handling."""
    rv = client.post('/', data={'ip_address': '999.999.999.999', 'cidr': '24'})
    assert b"Invalid IP Address" in rv.data
