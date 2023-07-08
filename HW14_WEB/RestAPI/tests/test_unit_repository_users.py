import datetime
import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,

)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session and user object, which will be used in the tests.
        
        :param self: Represent the instance of the object itself
        :return: A set of values that are used for testing
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(
            id=1,
            username='New_User',
            email='user_test@meta.ua',
            password='12345678',
            confirmed=True,
        )
        self.contact_test = Contact(
            id=1,
            first_name='Erik',
            last_name='Satie',
            email='gnossienne@mail.com',
            date_of_birth=datetime.date(year=1990, month=8, day=9),
        )

    async def test_get_user_by_email(self):
        """
        The test_get_user_by_email function tests the get_user_by_email function.
        It does this by creating a mock user, and then setting the return value of
        the session query to be that mock user. It then calls get_user_by email with 
        that mocked session, and checks if it returns the same mocked user.
        
        :param self: Represent the instance of the object that is passed to the method
        :return: The user object
        :doc-author: Trelent
        """
        user = self.user
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_create_user(self):
        """
        The test_create_user function tests the create_user function.
        It does this by creating a UserModel object with the username, email, and password attributes set to self.user's username, email and password respectively.
        The result variable is then assigned to await create_user(body=body, db=self.session). This means that it will wait for the asynchronous function create_user() to finish executing before continuing on with its own execution (the test).
        create_user() returns an instance of UserModel which is stored in result so we can check if it has been created correctly or not.
        
        :param self: Represent the instance of the object
        :return: The result of the create_user function
        :doc-author: Trelent
        """
        body = UserModel(
            username=self.user.username,
            email=self.user.email,
            password=self.user.password,
        )
        result = await create_user(body=body, db=self.session)

        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_confirmed_email(self):
        """
        The test_confirmed_email function tests the confirmed_email function in UserModel.py
            The test_confirmed_email function is a coroutine that takes two arguments: self and email.
            The test_confirmed_email function uses the MagicMock library to mock an object, which is then used as a parameter for the confirmed email method. 
            This allows us to check if our code works without having to actually run it on real data.
        
        :param self: Access the attributes and methods of the class in python
        :return: None
        :doc-author: Trelent
        """
        result = await confirmed_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)

    async def test_update_token(self):
        """
        The test_update_token function tests the update_token function in UserModel.py
            The test_update_token function takes a user and token as parameters, and updates the user's token to be equal to that of the given token.
            If no error is raised, then it returns None.
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        user = self.user
        token = None
        result = await update_token(user=user, token=token, db=self.session)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

