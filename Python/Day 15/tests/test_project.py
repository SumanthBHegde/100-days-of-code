def test_get_projects(client):
    response = client.get('/projects')
    assert response.status_code == 200

def test_create_project(client):
    response = client.post('/projects', json={
        'name': 'Project X',
        'description': 'This is a test project.'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'Project X'