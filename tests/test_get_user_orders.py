import requests
import allure
from config.config import *
from config.message import ErrorMessages


@allure.epic("Получение заказа")
class TestGetOrder:

    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_authorized_user(self, authorized_user_with_order):
        headers = {"Authorization": authorized_user_with_order}
        response = requests.get(Config.ORDER_URL, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "orders" in response.json()
        assert isinstance(response.json()["orders"], list)
        assert len(response.json()["orders"]) >= 1

    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_unauthorized_user(self):
        response = requests.get(Config.ORDER_URL)
        assert response.status_code == 401
        assert response.json()["success"] is False
        assert response.json()["message"] == ErrorMessages.UNAUTHORIZED