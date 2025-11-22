import requests
import allure
import pytest
from config.users import get_valid_user
from config.config import Config
from config.message import ErrorMessages


@allure.epic("Авторизация")
class TestUserLogin:

    def setup_method(self, method):
        with allure.step("Создаём уникального пользователя"):
            self.user = get_valid_user()
            response = requests.post(Config.USER_CREATE_URL, json=self.user)
            self.access_token = None
            if response.status_code == 200:
                self.access_token = response.json().get("accessToken")

    @allure.title("Успешный логин пользователя")
    def test_login_valid_user(self):
        response = requests.post(Config.USER_LOGIN_URL, json={
            "email": self.user["email"],
            "password": self.user["password"]
        })
        assert response.status_code == 200
        assert response.json().get("accessToken") is not None

    @pytest.mark.parametrize(
        "email, password, case_title", [
            ("wrong_email@example.com", "correct_password", "Неверный email"),
            ("correct_email", "wrong_password", "Неверный пароль"),
            ("wrong_email@example.com", "wrong_password", "Неверный email и пароль")
        ]
    )
    @allure.title("Негативные проверки логина:")
    def test_login_with_invalid_credentials(self, email, password, case_title):
        test_email = self.user["email"] if email == "correct_email" else email
        test_password = self.user["password"] if password == "correct_password" else password

        response = requests.post(Config.USER_LOGIN_URL, json={
            "email": test_email,
            "password": test_password
        })
        assert response.status_code == 401
        assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS

    def teardown_method(self, method):
        with allure.step("Удаляем пользователя, если он был создан"):
            if self.access_token:
                headers = {"Authorization": self.access_token}
                requests.delete(Config.BASE_URL  + Config.USER_DELETE_URL, headers=headers)
