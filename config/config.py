class Config:

    BASE_URL = 'https://stellarburgers.education-services.ru/api'

    USER_CREATE_URL = f'{BASE_URL}/auth/register'
    USER_LOGIN_URL = f'{BASE_URL}/auth/login'
    UPDATE_USER = f'{BASE_URL}/auth/user'
    USER_DELETE_URL = f'{BASE_URL}/auth/user'
    ORDER_URL = f'{BASE_URL}/orders'
    INGREDIENTS = f'{BASE_URL}/ingredients'