import requests
import allure

from config.config import *
from config.users import get_valid_user
from config.message import ErrorMessages


@allure.epic("Получение заказа")
class TestGetOrder:

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

        with allure.step("Создаём заказ для пользователя"):
            if self.access_token and self.ingredients:
                headers = {"Authorization": self.access_token}
                payload = {"ingredients": self.ingredients[:2]}
                requests.post(Config.ORDER_URL, headers=headers, json=payload)

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized_user(self):
        headers = {"Authorization": self.access_token}
        response = requests.get(Config.ORDER_URL, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized_user(self):
        response = requests.get(Config.ORDER_URL)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.UNAUTHORIZED

    def teardown_method(self, method):
        with allure.step("Удаляем пользователя, если он был создан"):
            if self.access_token:
                headers = {"Authorization": self.access_token}
                requests.delete(Config.USER_DELETE_URL, headers=headers)