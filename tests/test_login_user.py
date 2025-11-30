import requests
import allure
import pytest
from config.config import Config
from config.message import ErrorMessages


@allure.epic("Авторизация")
class TestUserLogin:

    @allure.title("Успешный логин пользователя")
    def test_login_valid_user(self, registered_user):
        with allure.step("Отправляем запрос на логин с валидными данными"):
            response = requests.post(Config.USER_LOGIN_URL, json={
                "email": registered_user["email"],
                "password": registered_user["password"]
            })

        assert response.status_code == 200
        assert response.json().get("accessToken") is not None

    @pytest.mark.parametrize(
        "email, password, case_title",
        [
            ("wrong_email@example.com", "correct_password", "Неверный email"),
            ("correct_email", "wrong_password", "Неверный пароль"),
            ("wrong_email@example.com", "wrong_password", "Неверный email и пароль")
        ],
        ids=["Неверный email", "Неверный пароль", "Неверные email и пароль"]
    )
    @allure.title("Негативные проверки логина: {case_title}")
    def test_login_with_invalid_credentials(self, registered_user, email, password, case_title):
        test_email = registered_user["email"] if email == "correct_email" else email
        test_password = registered_user["password"] if password == "correct_password" else password

        with allure.step(f"Пытаемся залогиниться с: email={test_email}"):
            response = requests.post(Config.USER_LOGIN_URL, json={
                "email": test_email,
                "password": test_password
            })

        assert response.status_code == 401
        assert response.json()["message"] == ErrorMessages.INVALID_CREDENTIALS
