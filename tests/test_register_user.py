import requests
import allure
import pytest

from config.users import get_valid_user
from config.config import Config
from config.message import ErrorMessages


@allure.epic("Регистрация пользователя")
class TestUserRegistration:

    def setup_method(self, method):
        self.access_token = None

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        user = get_valid_user()
        response = requests.post(Config.USER_CREATE_URL, json=user)
        assert response.status_code == 200
        assert response.json().get("success") is True
        self.access_token = response.json().get("accessToken")

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self):
        user = get_valid_user()

        user_1 = requests.post(Config.USER_CREATE_URL, json=user)
        assert user_1.status_code == 200

        user_2 = requests.post(Config.USER_CREATE_URL, json=user)
        assert user_2.status_code == 403
        assert user_2.json().get("message") == ErrorMessages.USER_ALREADY_EXISTS

    @allure.title("Создание пользователя без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_fields(self, missing_field):
        user = get_valid_user()
        user.pop(missing_field)

        response = requests.post(Config.USER_CREATE_URL, json=user)

        assert response.status_code == 403
        assert response.json().get("message") == ErrorMessages.REQUIRED_FIELDS_MISSING

    def teardown_method(self, method):
        with allure.step("Удаляем пользователя, если он был создан"):
            if self.access_token:
                headers = {"Authorization": self.access_token}
                requests.delete(Config.USER_DELETE_URL, headers=headers)