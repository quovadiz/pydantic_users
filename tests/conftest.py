import pytest

from models import BaseUser, User, AdminUser


@pytest.fixture(scope="class")
def base_user_factory():
    """Возвращает функцию для создания объекта BaseUser"""
    def _create(**kwargs):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "ivanivanov@test.com",
        }
        data.update(kwargs)
        return BaseUser(**data)
    return _create


@pytest.fixture(scope="class")
def user_factory():
    """Возвращает функцию для создания объекта User"""
    def _create(**kwargs):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "ivanivanov@test.com",
            "password": "Pass123!",
            "age": 22
        }
        data.update(kwargs)
        return User(**data)
    return _create


@pytest.fixture(scope="class")
def admin_user_factory():
    """Возвращает функцию для создания объекта AdminUser"""
    def _create(**kwargs):
        data = {
            "first_name": "Иван",
            "last_name": "Иванов",
            "email": "ivanivanov@test.com",
            "password": "Pass123!",
            "age": 22,
            "role": "admin"
        }
        data.update(kwargs)
        return AdminUser(**data)
    return _create
