import pytest
from app import app, db
from models import User, Project, Task

@pytest.fixture
def client():
    app.config.from_object('config.TestConfig')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_user_creation(client):
    user = User(username="testuser")
    user.set_password("testpass")
    db.session.add(user)
    db.session.commit()

    assert user in db.session

def test_project_creation(client):
    project = Project(name="Project A", description="Test Project")
    db.session.add(project)
    db.session.commit()

    assert project in db.session
    user = User(username='')