from django.test import TestCase
from core_app.models import UserAccount, AccountType
from django.urls import reverse
from core_app.tests import create_user

# Comments explaining how Django tests work can be found in the tests.py file of core_app.

class AdminViewsTests(TestCase):
    """
    This is the class for testing the following:
    - admin_map_view()
    - location_list()
    - delete_location_view()
    """

    def test_admin_map_access(self):
        """
        Tests that only admin accounts can access the Admin Map page (used for adding new locations or viewing current ones).
        Users not logged in at all should be redirected to the Login page, while those logged into a non-admin account
        should served a HTTP 403 error.
        """
        # First, access the page while not logged in.
        url = reverse("locations:admin_map_view")
        response1 = self.client.get(url)

        self.assertRedirects(response1, "/login/?next=/game_admin/map", status_code=302, target_status_code=200)
        # The user should be redirected to the Login page in this case.

        # Then, access the page while logged into a non-admin account.
        create_user("user001", "001@email.com", "password001", AccountType.USER.value)
        self.client.login(username="user001", password="password001")

        response2 = self.client.get(url)

        self.assertEqual(response2.status_code, 403)
        # The user should be served a HTTP 403 error page (unauthorised access error) in this case.

        # Finally, access the page while logged into an admin account.
        self.client.logout()
        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value)
        self.client.login(username="user002", password="password002")

        response3 = self.client.get(url)

        self.assertEqual(response3.status_code, 200)
        # The user should be allowed through to the Admin Map page, and the status code should be 200.

    def test_update_location_access(self):
        """
        Tests that only admin accounts can access the Update Location page (used for updating current locations).
        Users not logged in at all should be redirected to the Login page, while those logged into a non-admin account
        should served a HTTP 403 error.
        """
        # First, access the page while not logged in.
        url = reverse("locations:location_list")
        response1 = self.client.get(url)

        self.assertRedirects(response1, "/login/?next=/game_admin/update-location/", status_code=302, target_status_code=200)
        # The user should be redirected to the Login page in this case.

        # Then, access the page while logged into a non-admin account.
        create_user("user001", "001@email.com", "password001", AccountType.USER.value)
        self.client.login(username="user001", password="password001")

        response2 = self.client.get(url)

        self.assertEqual(response2.status_code, 403)
        # The user should be served a HTTP 403 error page (unauthorised access error) in this case.

        # Finally, access the page while logged into an admin account.
        self.client.logout()
        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value)
        self.client.login(username="user002", password="password002")

        response3 = self.client.get(url)

        self.assertEqual(response3.status_code, 200)
        # The user should be allowed through to the Update Location page, and the status code should be 200.

    def test_delete_location_access(self):
        """
        Tests that only admin accounts can access the Delete Location page (used for updating current locations).
        Users not logged in at all should be redirected to the Login page, while those logged into a non-admin account
        should served a HTTP 403 error.
        """
        # First, access the page while not logged in.
        url = reverse("locations:delete_location")
        response1 = self.client.get(url)

        self.assertRedirects(response1, "/login/?next=/game_admin/delete-location/", status_code=302, target_status_code=200)
        # The user should be redirected to the Login page in this case.

        # Then, access the page while logged into a non-admin account.
        create_user("user001", "001@email.com", "password001", AccountType.USER.value)
        self.client.login(username="user001", password="password001")

        response2 = self.client.get(url)

        self.assertEqual(response2.status_code, 403)
        # The user should be served a HTTP 403 error page (unauthorised access error) in this case.

        # Finally, access the page while logged into an admin account.
        self.client.logout()
        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value)
        self.client.login(username="user002", password="password002")

        response3 = self.client.get(url)

        self.assertEqual(response3.status_code, 200)
        # The user should be allowed through to the Delete Location page, and the status code should be 200.