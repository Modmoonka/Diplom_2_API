import requests
import allure
from config.config import Config
from config.message import ErrorMessages


@allure.epic("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с ингредиентами (авторизованный пользователь)")
    def test_create_order_with_ingredients_auth(self, auth_user_and_ingredients):
        access_token, ingredients = auth_user_and_ingredients
        headers = {"Authorization": access_token}
        payload = {"ingredients": ingredients[:2]}

        response = requests.post(Config.ORDER_URL, headers=headers, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Создание заказа с ингредиентами (неавторизованный пользователь)")
    def test_create_order_with_ingredients_no_auth(self, auth_user_and_ingredients):
        _, ingredients = auth_user_and_ingredients
        payload = {"ingredients": ingredients[:2]}

        response = requests.post(Config.ORDER_URL, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Создание заказа без ингредиентов (авторизованный пользователь)")
    def test_create_order_no_ingredients_auth(self, auth_user_and_ingredients):
        access_token, _ = auth_user_and_ingredients
        headers = {"Authorization": access_token}
        payload = {"ingredients": []}

        response = requests.post(Config.ORDER_URL, headers=headers, json=payload)
        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с неверными ингредиентами (авторизованный пользователь)")
    def test_create_order_with_invalid_ingredients(self, auth_user_and_ingredients):
        access_token, _ = auth_user_and_ingredients
        headers = {"Authorization": access_token}
        payload = {"ingredients": ["invalid_id_123", "fake_ingredient_456"]}
        response = requests.post(Config.ORDER_URL, headers=headers, json=payload)
        assert response.status_code == 500