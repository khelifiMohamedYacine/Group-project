from django.test import TestCase
from core_app.models import UserAccount, AccountType
from django.urls import reverse
from core_app.tests import create_user

# Comments explaining how Django tests work can be found in the tests.py file of core_app.

class AdminViewsTests(TestCase):
    """
    This is the class for testing the following:
    - admin_jumping_view() (from views.py in core_app)
    """

    def test_admin_jumping_access(self):
        """
        Tests that only admin accounts can access the Manage Jumping Game page.
        Users logged into non-admin accounts should be redirected to the Home Page, while users not logged
        in at all should be redirected to the Login page.
        """
        # First, access the page while not logged in.
        url = reverse("admin_jumping")
        response1 = self.client.get(url)

        self.assertRedirects(response1, "/login/", status_code=302, target_status_code=200)
        # The user should be redirected to the Login page in this case.

        # Then, access the page while logged into a non-admin account.
        create_user("user001", "001@email.com", "password001", AccountType.USER.value)
        self.client.login(username="user001", password="password001")

        response2 = self.client.get(url)

        self.assertRedirects(response2, "/home/", status_code=302, target_status_code=200)
        # The user should be redirected to the Home page in this case.

        # Finally, access the page while logged into an admin account.
        self.client.logout()
        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value)
        self.client.login(username="user002", password="password002")

        response3 = self.client.get(url)

        self.assertEqual(response3.status_code, 200)
        # The user should be allowed through to the Manage Jumping Game page, and the status code should be 200.