import requests
import allure

from config.config import *
from config.users import get_valid_user
from config.message import ErrorMessages


@allure.epic("Создание заказа")
class TestCreateOrder:

    def setup_method(self, method):
        with allure.step("Создаём уникального пользователя"):
            self.access_token = None
            self.user = get_valid_user()
            user_resp = requests.post(Config.USER_CREATE_URL, json=self.user)
            if user_resp.status_code == 200:
                self.access_token = user_resp.json().get("accessToken")

        with allure.step("Получаем список ингредиентов"):
            ing_resp = requests.get(Config.INGREDIENTS)
            self.ingredients = []
            if ing_resp.status_code == 200:
                self.ingredients = [i["_id"] for i in ing_resp.json().get("data", [])]

    @allure.title("Создание заказа с ингредиентами (авторизованный пользователь)")
    def test_create_order_with_ingredients_auth(self):
        headers = {"Authorization": self.access_token}
        payload = {"ingredients": self.ingredients[:2]}

        response = requests.post(Config.ORDER_URL, headers=headers, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Создание заказа с ингредиентами (неавторизованный пользователь)")
    def test_create_order_with_ingredients_no_auth(self):
        payload = {"ingredients": self.ingredients[:2]}

        response = requests.post(Config.ORDER_URL, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "order" in response.json()

    @allure.title("Создание заказа без ингредиентов (авторизованный пользователь)")
    def test_create_order_no_ingredients_auth(self):
        headers = {"Authorization": self.access_token}
        payload = {"ingredients": []}

        response = requests.post(Config.ORDER_URL, headers=headers, json=payload)

        assert response.status_code == 400
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.INGREDIENTS_REQUIRED

    @allure.title("Создание заказа с неверными ингредиентами (авторизованный пользователь)")
    def test_create_order_with_invalid_ingredients(self):
        headers = {"Authorization": self.access_token}
        payload = {"ingredients": ["invalid_id_123", "fake_ingredient_456"]}

        response = requests.post(Config.ORDER_URL, headers=headers, json=payload)

        assert response.status_code == 500

    def teardown_method(self, method):
        with allure.step("Удаляем пользователя, если он был создан"):
            if self.access_token:
                headers = {"Authorization": self.access_token}
                requests.delete(Config.USER_DELETE_URL, headers=headers)