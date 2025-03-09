from django.test import TestCase
from .models import UserAccount, AccountType
from django.urls import reverse

"""
IMPORTANT NOTES:
= A temporary database (with the same model structure but no data) is created for each test.
= The regular Django database is unaffected.
= Use "python manage.py test core_app" to run the tests listed here.
"""

# Create your tests here.


def create_user(username:str, email:str, password:str, account_type:AccountType=AccountType.USER.value):
    """
    This is a helper function that adds a user account to the (temporary testing) database using the given parameters.
    It can be called by the test functions to create a test user for them.
    It returns True if the test user was created successfully, and False if it wasn't.

    Within the same test function, try not to create accounts with the same username or email.
    """
    try:
        # Tries to create a new account with the parameters.
        testUser = UserAccount(username=username, email=email, account_type=account_type)
        testUser.set_password(password)
        testUser.save() # Saves the account to the testing database.
        return True
    except:
        # If any error or excpetion is thrown.
        print("An error or exception occurred while creating a user account.")
        return False
    

class LoginViewTests(TestCase):
    """
    Every test function in Django needs to be part of a class that inherits from the django.test.TestCase superclass.
    This is the class for the login_view() tests
    """

    def test_login_without_account(self):
        """
        Tests that users cannot log in with a username/email that doesn't belong to any existing accounts.
        They should be returned to the login page, and the response should have a status code of 200.
        """
        url = reverse("login", args=())
        # reverse() is useful if you want to call view functions that take arguments other than the request itself.
        data = {"username_or_email" : "Non-Existent-Username", "password" : "password"}
        # Creates the request.POST dictionary that would come as part of a POST request (a.k.a the POST request variables).

        response = self.client.post(url, data)
        # Use "self.client.get()" if you are testing a GET request rather than a POST request.
        # If you don't want to use the reverse() function, then use "response = self.client.post("login/", data)" instead:

        self.assertEqual(response.status_code, 200)
        # Similar to JUnit's version, assertEqual() asserts that it's first argument is equal to the second.
        
        # Since no accounts have been created during this test, there are no accounts to log into.
        # Therefore, the login should fail, the user should be returned to the login page, and the status code should be 200.

    def test_login_with_wrong_password(self):
        """
        Tests that users cannot login using the wrong password, for an existing account with a given username or email.
        They should be returned to the login page, and the response should have a status code of 200.
        """
        create_user("user001", "001@email.com", "password001")
        # Creates a user with the given username, email and password.

        url = reverse("login")
        data1 = {"username_or_email" : "user001", "password" : "password002"}
        data2 = {"username_or_email" : "001@email.com", "password" : "password002"}
        # Simulate logging in with the following details.

        response1 = self.client.post(url, data1)
        response2 = self.client.post(url, data2)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        # The username/email belongs to an existing account, but the password given is incorrect in both.
        # Therefore, the login(s) should fail, the user should be returned to the login page, and the status code should be 200.

    def test_login_with_correct_password(self):
        """
        Tests that users can log in successfully, using the username/email and password of an existing account.
        They should be redirected to the home page, and the response should have a status code of 302.
        """
        create_user("user001", "001@email.com", "password001")
        
        url = reverse("login")
        data1 = {"username_or_email" : "user001", "password" : "password001"}
        data2 = {"username_or_email" : "001@email.com", "password" : "password001"}

        response1 = self.client.post(url, data1)
        response2 = self.client.post(url, data2)

        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 302)
        # The username and email given belong to an existing account, and the password given is correct.
        # Therefore, the login(s) should succeed, the user should be redirected to the home page, and the status code should be 302.

        # For redirects in particular, if you wanted to get a regular response (containing the HTML content of the page),
        # then add "follow=True" to "self.client.post()".
        # For regular responses (where you use render() to return a HTML template), you don't need to do this.        

        self.assertRedirects(response1, "/home/", status_code=302, target_status_code=200)
        # This is a more complete way to test redirects, allowing you to check that the user ends up on the correct page.


class RegisterViewTests(TestCase):
    """
    This is the class for the register_view() tests

    Validation that should be implemented into register_view():
    = Check that the inputted username does not have the '@' character (so an email cannot be used for the username and vice versa)
    """

    def test_register_with_taken_username(self):
        """
        Tests that users cannot register for an account using a username that already belongs to an existing account.
        They should be redirected to the register page, and the response should have a status code of 302.
        """
        create_user("user001", "001@email.com", "password001")
        # Create an existing user before trying to register for an account

        url = reverse("register")
        data = {"username" : "user001", "email" : "002@email.com", "password" : "password002", "confirm_password" : "password002"}

        response = self.client.post(url, data)

        self.assertRedirects(response, "/register/", status_code=302, target_status_code=200)
        # The username given is already being used by an existing account.
        # Therefore, the registration should fail, and the status code should be 302.

    def test_register_with_taken_email(self):
        """
        Tests that users cannot register for an account using an email that already belongs to an existing account.
        They should be redirected to the register page, and the response should have a status code of 302.
        """
        create_user("user001", "001@email.com", "password001")

        url = reverse("register")
        data = {"username" : "user002", "email" : "001@email.com", "password" : "password002", "confirm_password" : "password002"}

        response = self.client.post(url, data)

        self.assertRedirects(response, "/register/", status_code=302, target_status_code=200)
        # The email given is already being used by an existing account.
        # Therefore, the registration should fail, and the status code should be 302.

    def test_register_with_non_matching_passwords(self):
        """
        Tests that users cannot register for an account if their inputted passwords do not match.
        They should be redirected to the register page, and the response should have a status code of 302.
        """
        create_user("user001", "001@email.com", "password001")

        url = reverse("register")
        data = {"username" : "user001", "email" : "001@email.com", "password" : "password001", "confirm_password" : "password002"}

        response = self.client.post(url, data)

        self.assertRedirects(response, "/register/", status_code=302, target_status_code=200)
        # The password given is different from the confirmation password.
        # Therefore, the registration should fail, and the status code should be 302.

    def test_register_with_valid_details(self):
        """
        Tests that users can register for an account if they give a unique username and email, along with matching passwords.
        They should be redirected to the login page, and the response should have a status code of 302.
        """
        create_user("user001", "001@email.com", "password001")

        url1 = reverse("register")
        data1 = {"username" : "user002", "email" : "002@email.com", "password" : "password002", "confirm_password" : "password002"}

        response1 = self.client.post(url1, data1)

        self.assertRedirects(response1, "/login/", status_code=302, target_status_code=200)
        # The username and email given are unique, and the two passwords match
        # Therefore, the registration should succeed in creating an account, and the status code should be 302.

        url2 = reverse("login")
        data2 = {"username_or_email" : "002@email.com", "password" : "password002"}

        response2 = self.client.post(url2, data2)
        # Attempt to log into the newly created account

        self.assertRedirects(response2, "/home/", status_code=302, target_status_code=200)
        # The details of the account just created have been used to log in
        # Therefore, the login(s) should succeed, the user should be redirected to the home page, and the status code should be 302.


class LogoutViewTests(TestCase):
    """
    This is the class for the logout_view() tests.
    Note that logout_view() does not correspond to any specific Logout page (since there isn't one).
    """

    def test_logout_while_logged_in(self):
        """
        Tests that users can log out (ideally using the Logout button within the navigation bar) if they are currently logged in.
        They should be redirected to the login page, and the response should have a status code of 302.
        """
        create_user("user001", "001@email.com", "password001")

        self.client.login(username="user001", password="password001")
        # Django's login() function is what properly logs a user account in (it is used by login_view() as well)
        # There is an equivalent logout() function which logout_view() uses

        url = reverse("logout")
        response = self.client.get(url)

        self.assertRedirects(response, "/login/", status_code=302, target_status_code=200)
        # If logging out, the user should be redirected to the login page, and the status code should be 302.

    def test_logout_while_logged_out(self):
        """
        Tests what happens if the user attempts to log out while not being logged in.
        Though not intended, the user can do this by using the logout URL to manually invoke logout_view().
        The outcome should be the same as if the user was previously logged in, with no other side effects.
        """
        # By default, the user is not logged into any account
        
        url = reverse("logout")
        response = self.client.get(url)

        self.assertRedirects(response, "/login/", status_code=302, target_status_code=200)
        # The user should still be redirected to the login page, and the status code should be 302.


class NavbarTests(TestCase):
    """
    This is the class for the navbar tests.
    These check that the navbar displays the buttons its meant to, given the page and login status.
    """

    def test_login_logout_button(self):
        """
        Tests that the blue button within the right-side of the navbar is a log in button when the user is logged out,
        and a log out button when the user is logged in.
        """
        # First, access the home page while not logged in.
        url = reverse("home")
        response1 = self.client.get(url)

        self.assertContains(response1, '<a class="nav-item nav-link login-btn" href="/login/">Log In</a>')
        # assertContains() asserts that its first argument contains (is a superstring of) its second argument.
        # The HTML for the login button should be present within the HTML code for the Home Page

        # Then, access the Home page while logged into an account.
        create_user("user001", "001@email.com", "password001")
        self.client.login(username="user001", password="password001")

        response2 = self.client.get(url)

        self.assertContains(response2, '<a class="nav-item nav-link login-btn" href="/logout/">Logout</a>')
        # Now, the HTML for the logout button should be present within the HTML code for the Home Page