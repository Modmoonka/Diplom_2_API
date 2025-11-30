import pytest
import requests
import allure
from config.config import Config
from config.users import get_random_name, get_random_email
from config.message import ErrorMessages


@allure.epic("Обновление данных пользователя")
class TestUserUpdate:

    @pytest.mark.parametrize(
        "update_field, value_func, title",
        [
            ("name", get_random_name, "Обновление имени"),
            ("email", get_random_email, "Обновление email")
        ],
        ids=["Имя", "Email"]
    )
    @allure.title("Авторизованный: {title}")
    def test_update_user_data_authorized(self, authorized_user, update_field, value_func, title):
        new_value = value_func()
        headers = {"Authorization": authorized_user["access_token"]}

        with allure.step(f"Обновляем поле '{update_field}' на '{new_value}'"):
            response = requests.patch(Config.UPDATE_USER, headers=headers, json={update_field: new_value})

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"][update_field] == new_value

        original = authorized_user["user"]
        updated = response.json()["user"]
        for field in ["name", "email"]:
            if field != update_field:
                assert updated.get(field) == original.get(field), f"Поле {field} изменилось неожиданно"

    @pytest.mark.parametrize(
        "update_field, value_func, title",
        [
            ("name", get_random_name, "Обновление имени без авторизации"),
            ("email", get_random_email, "Обновление email без авторизации")
        ],
        ids=["Имя (неавторизован)", "Email (неавторизован)"]
    )
    @allure.title("Неавторизованный: {title}")
    def test_update_user_data_unauthorized(self, update_field, value_func, title):
        new_value = value_func()

        with allure.step(f"Попытка обновить '{update_field}' без токена"):
            response = requests.patch(Config.UPDATE_USER, json={update_field: new_value})

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.UNAUTHORIZED