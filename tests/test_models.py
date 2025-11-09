import pytest
from pydantic import ValidationError
from models import BaseUser, User, AdminUser


@pytest.mark.base_user
class TestBaseUser:

    @pytest.mark.parametrize("email", [
        "ivanivanov@gmail.com",
        "IVANIVANOV@gmail.com",
        "IvanIvanov2008@gmail.com",
        "ivan-ivanov@gmail.com",
        "ivanivanov@test-mail.com",
        "ivan.ivanov@gmail.com",
        "ivan_ivanov@mail.ru",
        "ivanivanov@test.mail.com",
        "иван_иванов@почта.ру",
        "ivan_ivanov123@test-domain.co.uk",
        "ivan+ivanov@gmail.com"
    ])
    def test_valid_email(self, base_user_factory, email):
        user = base_user_factory(email=email)
        assert isinstance(user, BaseUser), \
            f"Пользователь с email '{email}' не был создан"
        assert user.email == email, \
            f"Email не совпадает: '{user.email}' вместо '{email}'"

    @pytest.mark.parametrize("invalid_email", [
        "",
        "ivanivanov@mail",
        "ivanivanov.mail.com",
        "ivan ivanov@mail.com",
        "ivanivanov@test mail.com",
        "@mail.com",
        "ivanivanov@",
        "ivanivanov@@mail.com",
        "ivan@ivanov@mail.com",
        "ivanivanov@.com",
    ])
    def test_invalid_email_raises(self, base_user_factory, invalid_email):
        with pytest.raises(ValidationError):
            base_user_factory(email=invalid_email)

    @pytest.mark.parametrize("first_name", [
        "иван", "ИВАН", "иВаН", "Ivan", "IVAN", "ИvaH",
    ])
    def test_first_name_capitalized(self, base_user_factory, first_name):
        user = base_user_factory(first_name=first_name)
        assert user.first_name[0].isupper(), \
            "Первая буква имени должна быть заглавной"
        assert user.first_name[1:].islower(), \
            "Все буквы кроме первой в имени должны быть строчными"

    @pytest.mark.parametrize("invalid_first_name", ["", None])
    def test_invalid_first_name_raises(
        self, base_user_factory, invalid_first_name
    ):
        with pytest.raises(ValidationError):
            base_user_factory(first_name=invalid_first_name)

    @pytest.mark.parametrize("last_name", [
        "Иванов", "иванов", "ИВАНОВ", "иВаНоВ", "Ivanov", "IVANOV", "ИvanoV"
    ])
    def test_last_name_capitalized(self, base_user_factory, last_name):
        user = base_user_factory(last_name=last_name)
        assert user.last_name[0].isupper(), \
            "Первая буква фамилии должна быть заглавной"
        assert user.last_name[1:].islower(), \
            "Все буквы кроме первой в имени должны быть строчными!"

    @pytest.mark.parametrize("invalid_last_name", ["", None])
    def test_invalid_last_name_raises(
        self, base_user_factory, invalid_last_name
    ):
        with pytest.raises(ValidationError):
            base_user_factory(last_name=invalid_last_name)


@pytest.mark.user
class TestUser:

    def test_user_inherits(self, user_factory):
        user = user_factory()
        assert hasattr(user, 'first_name'), \
            "Объект user должен иметь атрибут 'first_name'"
        assert hasattr(user, 'last_name'), \
            "Объект user должен иметь атрибут 'last_name'"
        assert hasattr(user, 'email'), \
            "Объект user должен иметь атрибут 'email'"
        assert hasattr(user, 'password'), \
            "Объект user должен иметь атрибут 'password'"
        assert hasattr(user, 'age'), \
            "Объект user должен иметь атрибут 'age'"

    @pytest.mark.parametrize("password", [
        "abc123!@",
        "Qwerty9#",
        "Hello@123",
        "MyPassw0rd$",
        "S3cur3!t",
        "!Qaz2Wsx",
        "Passw0rd!",
        "Passw0rd*",
        "Passw0rd%",
        "Passw0rd^",
        "Passw0rd&"
    ])
    def test_valid_password(self, user_factory, password):
        user = user_factory(password=password)
        assert isinstance(user, User), \
            "Объект с таким паролем не является экземпляром User"
        assert user.password == password, \
            "Пароль пользователя не совпадает с ожидаемым"

    @pytest.mark.parametrize("invalid_password", [
        "Ab1!",
        "123!abc",
        "abcdefgh!",
        "Abcdefg1",
        "PASSWORD2",
        "Password",
        "",
        "!@#$%^&*",
    ])
    def test_invalid_password(self, user_factory, invalid_password):
        with pytest.raises(ValidationError):
            user_factory(password=invalid_password)

    @pytest.mark.parametrize("age", [
        18, 19, 49, 120
    ])
    def test_valid_age(self, user_factory, age):
        user = user_factory(age=age)
        assert isinstance(user, User), \
            "Объект не является экземпляром User"
        assert isinstance(user.age, int), \
            "Возраст пользователя не является целым числом"
        assert 18 <= user.age <= 120, \
            "Возраст пользователя вне допустимого диапазона 18-120"

    @pytest.mark.parametrize("invalid_age", [
        0, 1, 17, 17.999, 18.001, 121, 999, 21.5, "", "Пять", None, -1
    ])
    def test_invalid_age(self, user_factory, invalid_age):
        with pytest.raises(ValidationError):
            user_factory(age=invalid_age)


@pytest.mark.admin_user
class TestAdminUser:

    def test_admin_user_inherits(self, admin_user_factory):
        admin = admin_user_factory()
        assert hasattr(admin, 'first_name'), \
            "Объект admin должен иметь атрибут 'first_name'"
        assert hasattr(admin, 'password'), \
            "Объект admin должен иметь атрибут 'password'"
        assert hasattr(admin, 'role'), \
            "Объект admin должен иметь атрибут 'role'"
        assert hasattr(admin, 'has_permission'), \
            "Объект admin должен иметь метод 'has_permission'"

    @pytest.mark.parametrize("role", ["admin", "superadmin"])
    def test_valid_admin_role(self, admin_user_factory, role):
        admin_user = admin_user_factory(role=role)
        assert isinstance(admin_user, AdminUser), \
            "Объект не является экземпляром AdminUser"
        assert admin_user.role in ["admin", "superadmin"], \
            "Роль пользователя не входит в допустимый список"

    @pytest.mark.parametrize("invalid_role", [
        "user", "base_user", "админ", "administrator", "Admin", "super_admin",
        "adm1n", None, "super admin"
    ])
    def test_invalid_admin_role(self, admin_user_factory, invalid_role):
        with pytest.raises(ValidationError):
            admin_user_factory(role=invalid_role)

    @pytest.mark.parametrize("permission", [
        "read", "write", "delete"
    ])
    def test_admin_has_permission(self, admin_user_factory, permission):
        admin_user = admin_user_factory()
        assert admin_user.has_permission(permission), \
            "Админ не имеет разрешения на это действие"

    @pytest.mark.parametrize("permission", [
        "read", "write", "delete", "manage_users", "manage_admins"
    ])
    def test_superadmin_has_permission(self, admin_user_factory, permission):
        admin_user = admin_user_factory(role="superadmin")
        assert admin_user.has_permission(permission), \
            "Суперадмин не имеет разрешения на это действие"

    @pytest.mark.parametrize("permission", [
        "manage_users", "manage_admins", None, "", 0, 1,
        "READ", "WRITE", "DELETE"
    ])
    def test_admin_has_no_permission(self, admin_user_factory, permission):
        admin_user = admin_user_factory()
        assert not admin_user.has_permission(permission), \
            "Админ получил недопустимое разрешение"

    @pytest.mark.parametrize("permission", [
        "READ", "WRITE", "DELETE", 0, 1, "", None
    ])
    def test_superadmin_has_no_permission(
        self, admin_user_factory, permission
    ):
        admin_user = admin_user_factory(role="superadmin")
        assert not admin_user.has_permission(permission),  \
            "Супердмин получил недопустимое разрешение"
