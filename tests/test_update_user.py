import pytest
import requests
import allure
from config.users import *
from config.config import *
from config.message import ErrorMessages


@allure.epic("Обновление данных пользователя")
class TestUserUpdate:

    def setup_method(self, method):
        with allure.step("Создаём уникального пользователя"):
            self.user = get_valid_user()
            response = requests.post(Config.USER_CREATE_URL, json=self.user)
            self.access_token = None
            if response.status_code == 200:
                self.access_token = response.json().get("accessToken")

    @pytest.mark.parametrize(
        "update_field, new_value, case_title",
        [
            ("name", get_random_name(), "Обновление имени"),
            ("email", get_random_email(), "Обновление email")
        ]
    )
    @allure.title("{case_title}")
    def test_update_user_data_authorized(self, update_field, new_value, case_title):
        headers = {"Authorization": self.access_token}
        response = requests.patch(Config.UPDATE_USER, headers=headers, json={
            update_field: new_value
        })
        assert response.status_code == 200
        assert response.json()["user"][update_field] == new_value

    @pytest.mark.parametrize(
        "update_field, new_value, case_title",
        [
            ("name", get_random_name(), "Обновление имени без авторизации"),
            ("email", get_random_email(), "Обновление email без авторизации")
        ]
    )
    @allure.title("{case_title}")
    def test_update_user_data_unauthorized(self, update_field, new_value, case_title):
        response = requests.patch(Config.UPDATE_USER, json={
            update_field: new_value
        })
        assert response.status_code == 401
        assert response.json()["message"] == ErrorMessages.UNAUTHORIZED

    def teardown_method(self, method):
        with allure.step("Удаляем пользователя, если он был создан"):
            if self.access_token:
                headers = {"Authorization": self.access_token}
                requests.delete(Config.USER_DELETE_URL, headers=headers)