from unittest.mock import MagicMock

from src.database.models import User


def test_create_user(client, user, monkeypatch):
    """
    The test_create_user function tests the /api/auth/signup endpoint.
    It does this by making a POST request to the endpoint with a JSON payload containing user data.
    The test asserts that the response status code is 201, which indicates that an object was created successfully.
    The test also asserts that 'id' is in the response body, which means it contains a valid user ID.
    
    :param client: Make requests to the flask application
    :param user: Pass in the user object that was created by the fixture
    :param monkeypatch: Mock the send_email function
    :return: A 201 status code and a json object with an id
    :doc-author: Trelent
    """
    mock_send_email = MagicMock()
    monkeypatch.setattr('src.routes.auth.send_email', mock_send_email)
    response = client.post(
        '/api/auth/signup',
        json=user,
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert 'id' in data


def test_repeat_create_user(client, user):
    """
    The test_repeat_create_user function tests that a user cannot be created twice.
    It does this by creating a user, then attempting to create the same user again.
    The second attempt should fail with an HTTP 409 status code and an error message.
    
    :param client: Make requests to the api
    :param user: Pass the user data into the function
    :return: A 409 status code and a message that the account already exists
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/signup',
        json=user,
    )
    assert response.status_code == 409, response.text
    data = response.json()
    assert data['detail'] == 'Account already exists'


def test_login_user_not_confirmed(client, user):
    """
    The test_login_user_not_confirmed function tests that a user cannot login if they have not confirmed their email.
    The test_login_user_not_confirmed function takes in the client and user parameters, which are passed from conftest.py.
    The response variable is assigned to the result of calling client's post method with '/api/auth/login' as its first argument, 
    and data={'username': user['email'], 'password': user['password']} as its second argument (the username and password are taken from the dictionary returned by conftest's createUser function). The assert statement checks that response's status code is
    
    :param client: Make requests to the flask application
    :param user: Pass in the user dictionary that is created by the fixture
    :return: A 401 status code and a detail message
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/login',
        data={'username': user.get('email'), 'password': user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'Email not confirmed'


def test_login_user(client, session, user):
    """
    The test_login_user function tests the login endpoint.
    It does this by first creating a user, then confirming that user's account.
    Then it sends a POST request to the /api/auth/login endpoint with the email and password of that user as data in JSON format.
    The response is checked for status code 200 (OK) and then its JSON content is parsed into a dictionary called 'data'.  The token_type key in 'data' should be equal to &quot;bearer&quot;. 
    
    :param client: Make requests to the flask application
    :param session: Create a new user in the database
    :param user: Create a user in the database
    :return: The following:
    :doc-author: Trelent
    """
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        '/api/auth/login',
        data={'username': user.get('email'), 'password': user.get('password')},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['token_type'] == 'bearer'


def test_login_wrong_password(client, user):
    """
    The test_login_wrong_password function tests the login endpoint with an incorrect password.
    It asserts that the response status code is 401, and that the detail key in the JSON response body is 'Invalid password'.
    
    :param client: Make requests to the flask application
    :param user: Create a user in the database
    :return: A 401 status code and an error message
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/login',
        data={'username': user.get('email'), 'password': 'password'},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'Invalid password'


def test_login_wrong_email(client, user):
    """
    The test_login_wrong_email function tests the login endpoint with an invalid email.
    It asserts that the response status code is 401, and that the detail key in the JSON response body is 'Invalid email'.
    
    :param client: Make requests to the api
    :param user: Create a user in the database
    :return: A 401 status code and a message
    :doc-author: Trelent
    """
    response = client.post(
        '/api/auth/login',
        data={'username': 'email', 'password': user.get('password')},
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data['detail'] == 'Invalid email'