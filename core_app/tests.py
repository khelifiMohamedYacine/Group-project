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


def create_user(username:str, email:str, password:str, account_type:AccountType=AccountType.USER.value, points:int=0):
    """
    This is a helper function that adds a user account to the (temporary testing) database using the given parameters.
    It can be called by the test functions to create a test user for them.
    It returns True if the test user was created successfully, and False if it wasn't.

    Within the same test function, try not to create accounts with the same username or email.
    """
    try:
        # Tries to create a new account with the parameters.
        testUser = UserAccount(username=username, email=email, account_type=account_type, reward_pts=points)
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

    def test_register_using_at_symbol(self):
        """
        Tests that users cannot register for an account using an username with a '@', or an email without a '@'.
        They should be redirected to the register page, and the response should have a status code of 302.
        """
        url = reverse("register")
        data1 = {"username" : "user@001", "email" : "001@email.com", "password" : "password001", "confirm_password" : "password001"}

        response1 = self.client.post(url, data1)

        self.assertRedirects(response1, "/register/", status_code=302, target_status_code=200)
        # The username contains the @ symbol, making it invalid.
        # Therefore, the registration should fail, and the status code should be 302.

        data2 = {"username" : "user001", "email" : "001email.com", "password" : "password001", "confirm_password" : "password001"}

        response2 = self.client.post(url, data2)

        self.assertRedirects(response2, "/register/", status_code=302, target_status_code=200)
        # The email does not contain the @ symbol, making it invalid.
        # Therefore, the registration should fail, and the status code should be 302.


    def test_register_with_non_matching_passwords(self):
        """
        Tests that users cannot register for an account if their inputted passwords do not match.
        They should be redirected to the register page, and the response should have a status code of 302.
        """
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
        Tests that the 'Log In' button is shown in the navbar when the user is logged out,
        and the 'Logout' button is shown when the user is logged in.
        """
        # First, access the Home page while not logged in.
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

    def test_admin_button(self):
        """
        Tests that the 'Admin Dashboard' button only appears in the navbar if the user is logged into an admin account.
        Otherwise, it should be hidden.
        Note that this does not test access to the Admin page itself.
        """
         # First, access the Home page while not logged in.
        url = reverse("home")
        response1 = self.client.get(url)

        self.assertNotContains(response1, '<a class="nav-link active" href="/game_admin/dashboard/"><i class="fas fa-user-cog"></i> Admin Dashboard</a>')
        # assertNotContains() asserts that its first argument does not contain its second argument.
        # The HTML for the admin button should NOT be present within the HTML code for the Home Page

        # Then, access the Home page while logged into a non-admin account.
        create_user("user001", "001@email.com", "password001", AccountType.USER.value)
        self.client.login(username="user001", password="password001")

        response2 = self.client.get(url)

        self.assertNotContains(response2, '<a class="nav-link active" href="/game_admin/dashboard/"><i class="fas fa-user-cog"></i> Admin Dashboard</a>')
        # The HTML for the admin button still should not be present within the HTML code for the Home Page

        # Finally, access the Home page while logged into an admin account.
        self.client.logout()
        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value)
        self.client.login(username="user002", password="password002")

        response3 = self.client.get(url)

        self.assertContains(response3, '<a class="nav-link active" href="/game_admin/dashboard/"><i class="fas fa-user-cog"></i> Admin Dashboard</a>')
        # Now, the HTML for the admin button should be present within the HTML code for the Home page

    def test_other_buttons(self):
        """
        Tests that each navbar button leading to page X does not appear when the user is on page X.
        This behaviour was manually implemented in navbar.html using Django template coding. 
        """
        response1 = self.client.get(reverse("home"))

        self.assertNotContains(response1, '<a class="nav-link" href="/home/"><i class="fas fa-home"></i> Home</a>')
        # The HTML for the home button should not be present on the Home page

        response2 = self.client.get(reverse("games_page"))

        self.assertNotContains(response2, '<a class="nav-link" href="/games/"><i class="fas fa-play-circle"></i> Games</a>')
        # The HTML for the games button should not be present on the Games page

        response3 = self.client.get(reverse("videos"))

        self.assertNotContains(response3, '<a class="nav-link" href="/videos/"><i class="fas fa-play-circle"></i> Videos</a>')
        # The HTML for the videos button should not be present on the Sustainability Videos page

        response4 = self.client.get(reverse("maps"))

        self.assertNotContains(response4, '<a class="nav-link" href="/maps/"><i class="fas fa-map-marker-alt"></i> Uni map</a>')
        # The HTML for the map button should not be present on the University Map page

        response5 = self.client.get(reverse("leaderboard"))

        self.assertNotContains(response5, '<a class="nav-link" href="/leaderboard/"><i class="fas fa-mobile-alt"></i> Leaderboard</a>')
        # The HTML for the leaderboard button should not be present on the Leaderboard page

        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value)
        self.client.login(username="user002", password="password002")

        response6 = self.client.get(reverse("admin_dashboard"))

        self.assertNotContains(response6, '<a class="nav-link active" href="/admin_page/"><i class="fas fa-user-cog"></i> Admin Dashboard</a>')
        # The HTML for the admin button should not be present on the Admin Dashboard page


class HomeViewTests(TestCase):
    """
    This is the class for the home_view() tests.
    """

    def test_welcome_message(self):
        """
        Tests that the welcome message on the Home Page is different depending on whether the user is logged in or not.
        """
        # First, access the Home page while not logged in.
        url = reverse("home")
        response1 = self.client.get(url)
        
        self.assertContains(response1, 'Welcome!')
        self.assertContains(response1, '<p class="h4 fw-bold" style="text-align: center;">Log In To Play The Game</p>')
        # The Home page should display "Welcome" and "Log In To Play The Game"

        # Then, access the Home page while logged into an account.
        create_user("user001", "001@email.com", "password001")
        self.client.login(username="user001", password="password001")

        response2 = self.client.get(url)

        self.assertContains(response2, 'Welcome, user001!')
        # The welcome message on the home page should now include the user's username

    def test_reward_points(self):
        """
        Tests that the Home page displays the user's current number of reward points, given they have logged into an account.
        """
        # When an account is first created, it has 0 reward points by default.
        create_user("user001", "001@email.com", "password001", AccountType.USER.value)
        self.client.login(username="user001", password="password001")

        url = reverse("home")
        response1 = self.client.get(url)
        
        self.assertContains(response1, '<p class="h4 fw-bold" style="text-align: center;">Reward Points: 0</p>')
        # The Home page should display that the user has 0 reward points.

        # This time, create an account and manually give it 25 reward points.
        self.client.logout()
        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value, 25)
        self.client.login(username="user002", password="password002")

        response2 = self.client.get(url)

        self.assertContains(response2, '<p class="h4 fw-bold" style="text-align: center;">Reward Points: 25</p>')
        # The Home page should now display that the user has 25 reward points.


class LeaderboardViewTests(TestCase):
    """
    This is the class for the leaderboard_view() tests.
    """

    def test_leaderboard_with_no_accounts(self):
        """
        Tests that there are no errors when the Leaderboard page is displayed without any accounts existing.
        The header of the leaderboard table should still be present, but there should be no other rows.
        """
        # Obviously by default there are no accounts in the test database.
        url = reverse("leaderboard")
        response1 = self.client.get(url)
        
        self.assertContains(response1, '<tbody>\n            \n        </tbody>')
        # Note: as we are testing the HTML code directly, the whitespaces and newline characters are necessary.
        # No <tr> tags or other text between the <tbody> tags indicates that the leaderboard works as intended..

    def test_leaderboard_with_one_account(self):
        """
        Tests that the leaderboard displays what it should when only one account exists.
        """
        create_user("user001", "001@email.com", "password001", AccountType.USER.value, 77)

        url = reverse("leaderboard")
        response1 = self.client.get(url)
        
        self.assertContains(response1, '<tr>\n                    <td>1</td>\n                    <td>user001</td>\n                    <td>77</td>\n                </tr>')
        # The leaderboard table should contain one (non-header) row: 1 - user001 - 77.

    def test_leaderboard_with_multiple_accounts(self):
        """
        Tests that the leaderboard displays what it should when multiple accounts exist.
        This includes properly ranking the accounts by the number of reward points they have.
        """
        # Create five different accounts with different numbers of reward points.
        create_user("user001", "001@email.com", "password001", AccountType.USER.value, 20)
        create_user("user002", "002@email.com", "password002", AccountType.ADMIN.value, 40)
        create_user("user003", "003@email.com", "password003", AccountType.USER.value, 50)
        create_user("user004", "004@email.com", "password004", AccountType.USER.value, 10)
        create_user("user005", "005@email.com", "password005", AccountType.ADMIN.value, 30)

        url = reverse("leaderboard")
        response1 = self.client.get(url)

        self.assertContains(response1, '<tr>\n                    <td>1</td>\n                    <td>user003</td>\n                    <td>50</td>\n                </tr>')
        self.assertContains(response1, '<tr>\n                    <td>2</td>\n                    <td>user002</td>\n                    <td>40</td>\n                </tr>')
        self.assertContains(response1, '<tr>\n                    <td>3</td>\n                    <td>user005</td>\n                    <td>30</td>\n                </tr>')
        self.assertContains(response1, '<tr>\n                    <td>4</td>\n                    <td>user001</td>\n                    <td>20</td>\n                </tr>')
        self.assertContains(response1, '<tr>\n                    <td>5</td>\n                    <td>user004</td>\n                    <td>10</td>\n                </tr>')
        # The users should be ordered based on their reward points, not based on the order they were created