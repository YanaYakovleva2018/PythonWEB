import datetime 
import unittest
from unittest.mock import MagicMock
from datetime import date

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contact_by_id,
    get_contacts,
    get_birthdays,
    create_contact,
    update_contact,
    remove_contact,
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        """
        The setUp function is called before each test function.
        It creates a new session object and a user object, which are used in the tests.
        
        :param self: Represent the instance of the class
        :return: A test contact
        :doc-author: Trelent
        """
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)
        self.test_contact = Contact(
            id=1,
            first_name='Yana',
            last_name='Yakovlieva',
            email='yanayakovleva362@gmail.com',
            phone_number="+380951609826",
            date_of_birth=datetime.date(year=1999, month=1, day=7)
        )

    async def test_get_contacts(self):
        """
        The test_get_contacts function tests the get_contacts function.
        
        :param self: Access the attributes and methods of the class
        :return: A list of contacts
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().offset().limit().all.return_value = contacts
        result = await get_contacts(skip=0, 
                                    limit=10, 
                                    first_name='', 
                                    last_name='', 
                                    email='', 
                                    user=self.user, 
                                    db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_f_by_first_name(self):
        """
        The test_get_contacts_f_by_first_name function tests the get_contacts function by passing in a first name and checking to see if it returns the correct contact.
        
        
        :param self: Access the attributes and methods of the class in python
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0,
                                    limit=10, 
                                    first_name=self.contact_test.first_name, 
                                    last_name='', 
                                    email='', 
                                    user=self.user,
                                      db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_last_name(self):
        """
        The test_get_contacts_by_last_name function tests the get_contacts function.
        It does this by creating a list of three contacts, and then setting the return value of 
        self.session.query().filter().all to be that list of contacts (this is done using MagicMock). 
        Then it calls get_contacts with a last name matching one of those three contacts, and checks that 
        the result is equal to the list created earlier.
        
        :param self: Access the class attributes
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, 
                                    limit=10, 
                                    first_name='', 
                                    last_name=self.contact_test.last_name, 
                                    email='', 
                                    user=self.user, 
                                    db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_by_email(self):
        """
        The test_get_contacts_by_email function tests the get_contacts function by passing in a contact's email address.
        The test_get_contacts_by_email function then checks to see if the result of calling get contacts with that email is equal to 
        the list of contacts.
        
        :param self: Refer to the class instance itself
        :return: A list of contacts that match the email address
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().all.return_value = contacts
        result = await get_contacts(skip=0, 
                                    limit=10, 
                                    first_name='', 
                                    last_name='', 
                                    email=self.contact_test.email, 
                                    user=self.user, 
                                    db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        """
        The test_get_contact_by_id function tests the get_contact_by_id function in ContactModel.py
            The test is successful if the result of calling get_contact_by_id with a contact id, user, and db session 
            returns a list containing the contact object that was passed to it.
        
        :param self: Access the attributes and methods of the class in python
        :return: The contacts list
        :doc-author: Trelent
        """
        contacts = [self.contact_test, Contact(), Contact()]
        self.session.query().filter().first.return_value = contacts
        result = await get_contact_by_id(contact_id=self.contact_test.id, 
                                         user=self.user, 
                                         db=self.session)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        """
        The test_create_contact function tests the create_contact function.
            The test_create_contact function takes in a body, db, and user as parameters.
            The test_create_contact function then creates a result variable that is equal to the create contact method with those parameters passed into it. 
            Then we assert that each of the attributes of result are equal to their corresponding attribute in body.
        
        :param self: Represent the instance of the class
        :return: A contactmodel object with the correct attributes
        :doc-author: Trelent
        """
        body = ContactModel(
            first_name=self.contact_test.first_name,
            last_name=self.contact_test.last_name,
            email=self.contact_test.email,
            phone=self.contact_test.email,
            date_of_birth=self.contact_test.date_of_birth)
        
        result = await create_contact(body=body, db=self.session, user=self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.date_of_birth, body.date_of_birth)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact(self):
        """
        The test_remove_contact function tests the remove_contact function in ContactModel.py
            The test_remove_contact function is a unit test that checks if the remove contact 
            functionality works as intended. It does this by creating a mock session object, and 
            then using it to create a mock contact object with an id of 1, which is then used to 
            call the remove_contact function from ContactModel.py with parameters of 1 for contact id, 
            self.session for db and self.user for user (which are also both mocked objects). The result of this call should be equal to our original
        
        :param self: Represent the instance of the class
        :return: The contact object
        :doc-author: Trelent
        """
        contact = self.contact_test
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=self.contact_test.id, 
                                      db=self.session, 
                                      user=self.user)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        """
        The test_remove_contact_not_found function tests the remove_contact function in ContactModel.py
        to ensure that it returns None when a contact is not found.
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=self.contact_test.id, 
                                      db=self.session, 
                                      user=self.user)
        self.assertIsNone(result)

    async def test_update_contact(self):
        """
        The test_update_contact function tests the update_contact function.
            The test_update_contact function takes in a contact, body, session, and user as parameters.
            The test_update_contact function then returns the result of the update contact.
        
        :param self: Access the attributes and methods of the class in python
        :return: The contact
        :doc-author: Trelent
        """
        contact = self.contact_test
        body = ContactModel(
            first_name='Yana',
            last_name=self.contact_test.last_name,
            email=self.contact_test.email,
            phone=self.contact_test.email,
            date_of_birth=self.contact_test.date_of_birth)
        self.session.query().filter().first.return_value = contact
        result = await update_contact(contact_id=self.contact_test.id, 
                                      body=body, 
                                      db=self.session, 
                                      user=self.user)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        """
        The test_update_contact_not_found function tests the update_contact function.
        The test_update_contact_not_found function is a unit test that checks if the update contact 
        method returns None when it cannot find a contact with the given id in the database. 
        This is done by mocking out all of its dependencies and setting up an expected result, then checking to see if they match.
        
        :param self: Represent the instance of the class
        :return: None
        :doc-author: Trelent
        """
        body = ContactModel(
            first_name='Yana',
            last_name=self.contact_test.last_name,
            email=self.contact_test.email,
            phone=self.contact_test.email,
            date_of_birth=self.contact_test.date_of_birth)
        self.session.query().filter().first.return_value = None
        result = await update_contact(contact_id=self.contact_test.id, 
                                      body=body, 
                                      db=self.session, 
                                      user=self.user)
        self.assertIsNone(result)

    async def test_get_contacts_birthdays(self):
        """
        The test_get_contacts_birthdays function tests the get_birthdays function.
        It does this by creating a mock session object and two mock contacts, one of which has today's date as its birthday.
        The test then calls the get_birthdays function with these parameters: offset=0, limit=10, user=self.user (a MagicMock object), and session = self.session (the mocked session). 
        The result is compared to the list of contacts created earlier in order to determine whether or not it matches.
        
        :param self: Represent the instance of the object that is passed to the method
        :return: Contacts
        :doc-author: Trelent
        """
        today = date.today()
        contacts = [
            Contact(id=1, first_name='Yana', last_name='Yakovlieva',
                    email='yanayakovleva362@gmail.com', date_of_birth=today),
            Contact(id=2, first_name='Lana', last_name='Banana',
                    email='lana_banana@example.com', date_of_birth=today),
        ]
        self.session.query().filter().offset().limit().all.return_value = contacts

        result = await get_birthdays(0, 10, self.user, self.session)
        self.assertEqual(result, contacts)

if __name__ == '__main__':
    unittest.main()