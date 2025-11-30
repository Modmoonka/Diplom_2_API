import pytest
import requests
from config.config import Config
from config.users import get_valid_user


def delete_user(access_token: str):
    if not access_token:
        return
    headers = {"Authorization": access_token}
    try:
        requests.delete(Config.USER_DELETE_URL, headers=headers)
    except Exception:
        pass


@pytest.fixture
def authorized_user():
    user_data = get_valid_user()
    resp = requests.post(Config.USER_CREATE_URL, json=user_data)
    access_token = resp.json().get("accessToken")
    user_from_resp = resp.json().get("user", {})
    user_data.update(user_from_resp)
    yield {"user": user_data, "access_token": access_token}
    delete_user(access_token)


@pytest.fixture
def auth_user_and_ingredients():
    user_data = get_valid_user()
    user_resp = requests.post(Config.USER_CREATE_URL, json=user_data)
    access_token = user_resp.json().get("accessToken")
    ing_resp = requests.get(Config.INGREDIENTS, timeout=10)
    ingredients = [i["_id"] for i in ing_resp.json().get("data", [])]
    yield access_token, ingredients
    delete_user(access_token)


@pytest.fixture
def authorized_user_with_order():
    #Пользователь
    user_data = get_valid_user()
    user_resp = requests.post(Config.USER_CREATE_URL, json=user_data)
    access_token = user_resp.json().get("accessToken")

    # Ингредиенты
    ing_resp = requests.get(Config.INGREDIENTS, timeout=10)
    ingredients = [i["_id"] for i in ing_resp.json().get("data", [])]
    assert len(ingredients) >= 2

    # Заказ
    headers = {"Authorization": access_token}
    order_resp = requests.post(Config.ORDER_URL, headers=headers, json={"ingredients": ingredients[:2]})
    yield access_token
    delete_user(access_token)


@pytest.fixture
def registered_user():
    user_data = get_valid_user()
    resp = requests.post(Config.USER_CREATE_URL, json=user_data, timeout=10)
    access_token = resp.json().get("accessToken")
    yield user_data
    delete_user(access_token)


@pytest.fixture
def existing_user(registered_user):
    return registered_user