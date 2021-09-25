import json

from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class SignUpTest(APITestCase):

    signup_url = "/users/signup"

    def test_signupview_post_user_registration_success(self):
        user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, data=user_data)
        self.assertEqual(201, response.status_code)

    def test_signupview_post_duplicated_email(self):
        exist_user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, exist_user_data)
        self.assertEqual(201, response.status_code)

        new_user_data = {
            "email":"email@test.com",
            "phone_number":"01011113333",
            "name":"testuser",
            "nickname":"test",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, new_user_data)
        self.assertEqual(400, response.status_code)

    def test_signupview_post_duplicated_phone_number(self):
        exist_user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, exist_user_data)
        self.assertEqual(201, response.status_code)

        new_user_data = {
            "email":"email99@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"test",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, new_user_data)
        self.assertEqual(400, response.status_code)

    def test_signupview_post_duplicated_nickname(self):
        exist_user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, exist_user_data)
        self.assertEqual(201, response.status_code)

        new_user_data = {
            "email":"email99@test.com",
            "phone_number":"01011113333",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, new_user_data)
        self.assertEqual(400, response.status_code)

    def test_signupview_post_invalid_password(self):
        user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234"
        }
        response = self.client.post(self.signup_url, data=user_data)
        self.assertEqual(400, response.status_code)

    def test_signupview_post_keyerror_email(self):
        user_data = {
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, data=user_data)
        self.assertEqual(400, response.status_code)

    def test_signupview_post_keyerror_phone_number(self):
        user_data = {
            "email":"email@test.com",
            "name":"testuser",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, data=user_data)
        self.assertEqual(400, response.status_code)
    
    def test_signupview_post_keyerror_name(self):
        user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "nickname":"testtest",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, data=user_data)
        self.assertEqual(400, response.status_code)
    
    def test_signupview_post_keyerror_nickname(self):
        user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "password": "1234test"
        }
        response = self.client.post(self.signup_url, data=user_data)
        self.assertEqual(400, response.status_code)
    
    def test_signupview_post_keyerror_password(self):
        user_data = {
            "email":"email@test.com",
            "phone_number":"01011112222",
            "name":"testuser",
            "nickname":"testtest"
        }
        response = self.client.post(self.signup_url, data=user_data)
        self.assertEqual(400, response.status_code)
    

class LoginTest(APITestCase):

    login_url = "/users/login"

    def setUp(self):
        self.user = User.objects.create(
            id=1,
            email="email@test.com",
            phone_number="01011112222",
            name="testuser",
            nickname="testtest",
            password="1234test",
        )
        self.user.set_password("1234test")
        self.user.save()

        self.superuser = User.objects.create(
            id=2,
            email="admin@test.com",
            phone_number="01011113333",
            name="testuser",
            nickname="testadmin",
            password="1234test",
            is_staff=True,
            is_superuser=True,
        )
        self.superuser.set_password("1234test")
        self.superuser.save()

    def tearDown(self):
        self.user.delete()
        self.superuser.delete()

    def test_loginview_post_success(self):
        user_data = {
            "email":"email@test.com",
            "password":"1234test"
        }
        response = self.client.post(self.login_url, data=user_data)
        response_data = response.json()
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in response_data)

    def test_loginview_post_password_does_not_match(self):
        user_data = {
            "email":"email@test.com",
            "password":"1234"
        }
        response = self.client.post(self.login_url, data=user_data)
        self.assertEqual(400, response.status_code)

    def test_loginview_post_user_does_not_exists(self):
        user_data = {
            "email":"doesnotexist",
            "password":"1234test"
        }
        response = self.client.post(self.login_url, data=user_data)
        self.assertEqual(400, response.status_code)

    def test_loginview_post_keyerror_email(self):
        user_data = {
            "password":"1234test"
        }
        response = self.client.post(self.login_url, data=user_data)
        self.assertEqual(400, response.status_code)

    def test_loginview_post_keyerror_password(self):
        user_data = {
            "email":"email@test.com"
        }
        response = self.client.post(self.login_url, data=user_data)
        self.assertEqual(400, response.status_code)


class LogoutTest(APITestCase):

    logout_url = "/users/logout"
    login_url = "/users/login"

    def setUp(self):
        self.user = User.objects.create(
            id=1,
            email="email@test.com",
            phone_number="01011112222",
            name="testuser",
            nickname="testtest",
            password="1234test",
        )
        self.user.set_password("1234test")
        self.user.save()

    def _login(self):
        data = {
            "email": "email@test.com", 
            "password": "1234test"
            }
        response = self.client.post(self.login_url, data)
        response_data = response.json()
        if "access" in response_data:
            self.client.credentials(HTTP_AUTHORIZATION="Bearer %s" % response_data['access'])
        return response.status_code, response_data

    def tearDown(self):
        self.user.delete()

    def test_logoutview_post_success(self):
        _, response_data = self._login()
        data = {"refresh": response_data["refresh"]}
        response = self.client.post(self.logout_url, data=data)
        self.assertEqual(204, response.status_code)