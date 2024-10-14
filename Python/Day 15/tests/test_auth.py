def test_register_user(client):
    response = client.post('/auth/register', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'testuser'