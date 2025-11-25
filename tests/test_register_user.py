import requests
import allure
import pytest
from config.config import Config
from config.users import get_valid_user
from config.message import ErrorMessages
from conftest import delete_user


@allure.epic("Регистрация пользователя")
class TestUserRegistration:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self):
        user = get_valid_user()
        access_token = None
        try:
            response = requests.post(Config.USER_CREATE_URL, json=user)
            assert response.status_code == 200
            assert response.json().get("success") is True
            access_token = response.json().get("accessToken")
            assert access_token is not None
        finally:
            delete_user(access_token)

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_register_existing_user(self, existing_user):
        response = requests.post(Config.USER_CREATE_URL, json=existing_user)
        assert response.status_code == 403
        assert response.json().get("message") == ErrorMessages.USER_ALREADY_EXISTS

    @allure.title("Создание пользователя без обязательных полей: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_fields(self, missing_field):
        user = get_valid_user()
        user.pop(missing_field)

        response = requests.post(Config.USER_CREATE_URL, json=user)
        assert response.status_code == 403
        assert response.json().get("message") == ErrorMessages.REQUIRED_FIELDS_MISSING