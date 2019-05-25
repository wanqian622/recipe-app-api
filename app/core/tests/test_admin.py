from django.test import TestCase, Client
from django.contrib.auth import get_user_model
# generate url for our django admin page
from django.urls import reverse
# allow us to make test requests to our app


class AdminSiteTests(TestCase):
    # the set up test is a function run before every test that we run
    def setUp(self):
        # our setUp is going to consist of creating our test Client
        # add a new user that we can use to test
        # and make sure the user is loged into our client
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin.@gmail.com',
            password='password123'
        )
        # Use the client help function that allows us to log a user in
        # with the Django auth
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="password123",
            name="Test"
        )

    # test the users are listed in our django admin
    def test_users_listed(self):
        """Test that users are listed on user page"""
        # generate a url for our listed user page
        url = reverse('admin:core_user_changelist')
        # perform http get on the url
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        # admin/core/user/id
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
