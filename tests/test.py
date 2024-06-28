import pytest
from unittest.mock import patch, MagicMock
from load_balancer.core import LoadBalancer
from flask import Flask, json

app = Flask(__name__)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def load_balancer():
    lb = LoadBalancer()
    lb.consistent_hash = MagicMock()
    return lb

def test_get_server(load_balancer):
    load_balancer.consistent_hash.add_request.return_value = 'server1'
    server, port = load_balancer.get_server()
    assert server == 'server1'
    assert port == 4000

def test_get_replicas(load_balancer):
    load_balancer.replicas = {'server1', 'server2'}
    response = load_balancer.get_replicas()
    assert response['status'] == 'success'
    assert response['message']['N'] == 2
    assert set(response['message']['replicas']) == {'server1', 'server2'}

def test_add_replica(load_balancer, client):
    load_balancer.replicas = set()
    load_balancer.consistent_hash.add_server = MagicMock()
    load_balancer.handle_add = MagicMock()
    data = {"n": 2, "hostnames": ["server1", "server2"]}
    with app.test_request_context(json=data, method='POST'):
        response = load_balancer.add_replica()
        assert response['status'] == 'success'
        assert len(load_balancer.replicas) == 2
        load_balancer.handle_add.assert_any_call('server1')
        load_balancer.handle_add.assert_any_call('server2')

def test_handle_add(load_balancer):
    load_balancer.spawn = MagicMock()
    load_balancer.consistent_hash.add_server = MagicMock()
    load_balancer.handle_add('server1')
    assert 'server1' in load_balancer.replicas
    load_balancer.consistent_hash.add_server.assert_called_once_with('server1')

def test_handle_error(load_balancer):
    load_balancer.spawn = MagicMock()
    load_balancer.consistent_hash.add_server = MagicMock()
    load_balancer.consistent_hash.remove_server = MagicMock()
    with patch('loadbalancer.LoadBalancer.forward') as mock_forward:
        load_balancer.handle_error(server='server1', path='/test', method='GET')
        assert any('emergency_' in s for s in load_balancer.replicas)
        mock_forward.assert_called_once_with('/test', 'GET')

def test_remove_replica(load_balancer, client):
    load_balancer.replicas = {'server1', 'server2'}
    load_balancer.consistent_hash.remove_server = MagicMock()
    load_balancer.handle_remove = MagicMock()
    data = {"n": 2, "hostnames": ["server1", "server2"]}
    with app.test_request_context(json=data, method='DELETE'):
        response = load_balancer.remove_replica()
        assert response['status'] == 'success'
        assert len(load_balancer.replicas) == 0
        load_balancer.handle_remove.assert_any_call('server1')
        load_balancer.handle_remove.assert_any_call('server2')

def test_handle_remove(load_balancer):
    load_balancer.kill = MagicMock()
    load_balancer.consistent_hash.remove_server = MagicMock()
    load_balancer.replicas = {'server1'}
    load_balancer.handle_remove('server1')
    assert 'server1' not in load_balancer.replicas
    load_balancer.consistent_hash.remove_server.assert_called_once_with('server1')
