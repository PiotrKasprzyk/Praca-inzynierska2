import pytest
from app import app, db, Post, User
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Witamy w Diet and Workout Manager" in response.data

def test_register(client):
    response = client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Konto zosta\u0142o utworzone" in response.data

def test_login(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Zalogowano pomy\u015blnie" in response.data

def test_logout(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"Witamy w Diet and Workout Manager" in response.data

def test_create_diet_plan(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    response = client.post('/create_plan', data={
        'meal_name': 'Breakfast',
        'recipe': 'Omelette',
        'meal_type': 'Breakfast',
        'kcal': 300,
        'carbs': 20,
        'protein': 25,
        'fat': 10,
        'submit_diet': 'Save Diet Plan'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Plan diety zosta\u0142 zapisany" in response.data

def test_create_workout_plan(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    response = client.post('/create_plan', data={
        'exercise_name': 'Push Up',
        'day': 'Monday',
        'sets': 3,
        'reps': 12,
        'submit_workout': 'Save Workout Plan'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Plan treningowy zosta\u0142 zapisany" in response.data

def test_add_post(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    response = client.post('/add_post', data={
        'title': 'Test Post',
        'content': 'This is a test post.',
        'submit_post': 'Save Post'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Post zosta\u0142 dodany" in response.data

def test_add_comment(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post('/add_post', data={
        'title': 'Test Post',
        'content': 'This is a test post.',
        'submit_post': 'Save Post'
    }, follow_redirects=True)
    post = Post.query.first()
    response = client.post(url_for('add_comment', post_id=post.id), data={
        'comment': 'This is a test comment.',
        'submit_comment': 'Save Comment'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Komentarz zosta\u0142 dodany" in response.data

def test_like_post(client):
    client.post('/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password'
    }, follow_redirects=True)
    client.post('/add_post', data={
        'title': 'Test Post',
        'content': 'This is a test post.',
        'submit_post': 'Save Post'
    }, follow_redirects=True)
    post = Post.query.first()
    response = client.post(url_for('like_post', post_id=post.id), follow_redirects=True)
    assert response.status_code == 200
    assert b"Post zosta\u0142 polubiony" in response.data
