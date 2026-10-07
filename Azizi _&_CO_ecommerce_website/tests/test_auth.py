from app.models.user import User
from app.extensions import db


def test_user_registration(client, db):
    """Test user sign up creates a record in the database."""
    response = client.post('/auth/register', data={
        'full_name': 'Test Shopper',
        'email': 'shopper@azizi.com',
        'password': 'securepassword123',
        'confirm_password': 'securepassword123'
    }, follow_redirects=True)

    assert response.status_code == 200
    user = User.query.filter_by(email='shopper@azizi.com').first()
    assert user is not None
    assert user.full_name == 'Test Shopper'
    assert user.check_password('securepassword123') is True


def test_user_login_and_logout(client, db):
    """Test user login authentication flow and session termination."""
    # Create test user manually
    user = User(full_name='Login Test', email='login@azizi.com')
    user.set_password('mypassword')
    db.session.add(user)
    db.session.commit()

    # Test login POST request
    response = client.post('/auth/login', data={
        'email': 'login@azizi.com',
        'password': 'mypassword'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Test logout GET request
    logout_response = client.get('/auth/logout', follow_redirects=True)
    assert logout_response.status_code == 200