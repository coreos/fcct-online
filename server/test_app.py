import pytest

from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client


def test_root_get(client):
    """
    / should 404
    """
    resp = client.get('/')
    assert resp.status_code == 404


def test_config_get(client):
    """
    /config should reject GET
    """
    resp = client.get('/config')
    assert resp.status_code == 405


def test_config_post(client):
    """
    /config should accept POST when the content is JSON
    and a valid config_string is provided
    """
    # Not JSON
    resp = client.post('/config', data={}, follow_redirects=True)
    assert resp.json['success'] is False
    assert resp.json['message'].startswith('failed:')
    assert resp.status_code == 400

    # JSON but empty
    resp = client.post('/config', json={}, follow_redirects=True)
    assert resp.json['success'] is False
    assert resp.json['message'].startswith('failed:')
    assert resp.status_code == 400

    # Valid JSON
    config_string = '''\
variant: fcos
version: 1.0.0
passwd:
  users:
    - name: core
      ssh_authorized_keys:
        - key1'''
    resp = client.post(
        '/config',
        json={'config_string': config_string},
        follow_redirects=True)
    assert resp.status_code == 200
    assert resp.json.get('err_lines') is None  # No errors
    assert resp.json['success'] is True  # Should succeed
    assert resp.json['message'].get('ignition') is not None  # Expected result
