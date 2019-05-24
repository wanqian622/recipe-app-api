from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        # pass email, address and a password to verify that user has
        # beed created.
        email = "test@gmail.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # assertion to make sure the user create correctly
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # when we call create_user function and we do not
        # pass an email address so we just pass a blank string
        # or we just pass a non-value, then we want to make sure
        # we raise a value error that says the email address was
        # not provided
        with self.assertRaises(ValueError):
            # every thing we run here should raise
            # the ValueError, if it does not raise the value error
            # this test will fail.
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creatong a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
