import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database.models import Base
from src.database.db import get_db


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope='module')
def session():
    """
    The session function is a fixture that creates a new database session for
    a test to use. It's useful whenever you have code that uses the database,
    such as when testing models or API routes. The session function returns a 
    SessionLocal class, which is an object created by SQLAlchemy and used to 
    interact with the database.
    
    :return: A session object
    :doc-author: Trelent
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope='module')
def client(session):
    """
    The client function is a fixture that allows us to override the get_db function in our app.py file so that we can use it with pytest. The yield statement will return the session object, and then close it when we are done using it.

    :param session: Create a new database session for each test
    :return: A testclient object
    :doc-author: Trelent
    """

    def override_get_db():
        """
        The override_get_db function is a fixture that allows us to override the get_db function
            in our app.py file so that we can use it with pytest. The yield statement will return the session object,
            and then close it when we are done using it.
        
        :return: A context manager
        :doc-author: Trelent
        """
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope='module')
def user():
    """
    The user function returns a dictionary with the following keys:
        username, email, password.
        The values are strings that represent a user's credentials.
    
    :return: A dict with the keys username, email and password
    :doc-author: Trelent
    """
    return {'username': 'Lana', 'email': 'lana_banana@example.com', 'password': 'AHS12345678'}