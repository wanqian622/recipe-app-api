# allow us to mark the behavior of the django_get_db function
# we basically simulate the db being available and not being available
from unittest.mock import patch
from django.core.management import call_command
# the error when the django throws the db is unavailable
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

    # what happens when we call our command
    # and the db is already available
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        # To set up our test, we need to simulate the
        # behavior of django when the db is avaiable
        # our command is going to try and retrieve
        # the db connection from django
        # override the behavior of the connection handler
        # to return T or F instead of throwing error
        # use patch to mark the connection handler to just
        # return true everytime it's called
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # whenever django.db.utils.ConnectionHandler.__getitem__' is called
            # instead of actually performing this, we will override it and just
            # replace it with a mock object
            # which just does two thing , return the value we specify here
            # and allows us to monitor how many times it was called
            # and different cause that make it
            gi.return_value = True
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 1)

    # check the wait_for_db command will try the db 5 times and then on the
    # six time it will be successful and continue
    @patch('time.sleep', return_value=True)
    # replace the behavior of time sleep with a mock function that returns true
    # so we will not actually wait so that we could speed up the test
    def test_wait_for_db(self, ts):
        """Test waiting for db """
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # set side effect
            # the first five times you call this __getitem__
            # it will raise the operational error
            # And the six time, it will not raise the error and just return
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
