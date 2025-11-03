import pytest
from pydantic import ValidationError
from models import BaseUser, User, AdminUser


@pytest.mark.base_user
class TestBaseUser:
    """
    Класс с тестовыми случаями для модели BaseUser
    """

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
        """
        Проверка валидных email-адресов
        """
        user = base_user_factory(email=email)
        assert isinstance(user, BaseUser)  # проверяем, что объект создался
        assert user.email == email

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
        """
        Проверка, что невалидные email вызывают ValidationError
        """
        with pytest.raises(ValidationError):
            base_user_factory(email=invalid_email)

    @pytest.mark.parametrize("first_name", [
        "иван", "ИВАН", "иВаН", "Ivan", "IVAN", "ИvaH",
    ])
    def test_first_name_capitalized(self, base_user_factory, first_name):
        """
        Проверка того, что все имена начинаются с заглавной буквы
        """
        user = base_user_factory(first_name=first_name)
        assert user.first_name[0].isupper()  # Первая буква заглавная
        assert user.first_name[1:].islower()  # Остальные строчные

    @pytest.mark.parametrize("invalid_first_name", ["", None])
    def test_invalid_first_name_raises(
        self, base_user_factory, invalid_first_name
    ):
        """
        Проверка, что пустое или None имя вызывает ValidationError
        """
        with pytest.raises(ValidationError):
            base_user_factory(first_name=invalid_first_name)

    @pytest.mark.parametrize("last_name", [
        "Иванов", "иванов", "ИВАНОВ", "иВаНоВ", "Ivanov", "IVANOV", "ИvanoV"
    ])
    def test_last_name_capitalized(self, base_user_factory, last_name):
        """
        Проверка того, что все фамилии начинаются с заглавной буквы
        """
        user = base_user_factory(last_name=last_name)
        assert user.last_name[0].isupper()  # Первая буква заглавная
        assert user.last_name[1:].islower()  # Остальные строчные

    @pytest.mark.parametrize("invalid_last_name", ["", None])
    def test_invalid_last_name_raises(
        self, base_user_factory, invalid_last_name
    ):
        """
        Проверка, что пустая или None фамилия вызывает ValidationError
        """
        with pytest.raises(ValidationError):
            base_user_factory(last_name=invalid_last_name)


@pytest.mark.user
class TestUser:
    """
    Класс с тестовыми случаями для модели User
    """

    def test_user_inherits(self, user_factory):
        """
        Проверка наследования атрибутов от базовой модели и добавления
        своих полей
        """
        user = user_factory()
        assert hasattr(user, 'first_name')
        assert hasattr(user, 'last_name')
        assert hasattr(user, 'email')
        assert hasattr(user, 'password')
        assert hasattr(user, 'age')

    @pytest.mark.parametrize("password", [
        "abc123!@",  # длина 8, есть цифры и спецсимволы "!", "@"
        "Qwerty9#",  # длина 8, есть цифра и спецсимвол "#"
        "Hello@123",  # длина 9, есть цифры и спецсимвол "@"
        "MyPassw0rd$",  # длина 11, есть цифра и спецсимвол "$"
        "S3cur3!t",  # длина 8, цифры, спецсимвол "!"
        "!Qaz2Wsx",  # длина 8, спецсимвол "!", цифра
        "Passw0rd!",  # длина 9, есть цифра и спецсимвол !
        "Passw0rd*",  # длина 9, есть цифра и спецсимвол "*"
        "Passw0rd%",  # длина 9, есть цифра и спецсимвол "%"
        "Passw0rd^",  # длина 9, есть цифра и спецсимвол "^"
        "Passw0rd&"  # длина 9, есть цифра и спецсимвол "&"
    ])
    def test_valid_password(self, user_factory, password):
        """
        Проверка валидных паролей
        """
        user = user_factory(password=password)
        assert isinstance(user, User)  # проверяем, что объект создался
        assert user.password == password

    @pytest.mark.parametrize("invalid_password", [
        "Ab1!",  # 4 символа, верхний и нижний регистр, есть цифра и спецсимвол
        "123!abc",  # 7 символов, нижний регистр, спецсимволы, цифры
        "abcdefgh!",  # только нижний регистр, спецсимвол есть, цифр нет
        "Abcdefg1",  # верхний и нижний регистр, цифра есть, спецсимволов нет
        "PASSWORD2",  # верхний регистр, есть цифра, нет спецсимволов
        "Password",  # верхний и нижний регистр, только буквы
        "",  # пустое значение
        "!@#$%^&*",  # только спецсимволы, 8 символов
    ])
    def test_invalid_password(self, user_factory, invalid_password):
        """
        Проверка, что невалидные пароли вызывают ValidationError
        """
        with pytest.raises(ValidationError):
            user_factory(password=invalid_password)

    @pytest.mark.parametrize("age", [
        18, 19, 49, 120
    ])
    def test_valid_age(self, user_factory, age):
        """
        Проверка валидного возраста пользователя
        """
        user = user_factory(age=age)
        assert isinstance(user, User)  # проверяем, что объект создался
        assert isinstance(user.age, int)
        assert 18 <= user.age <= 120

    @pytest.mark.parametrize("invalid_age", [
        0, 1, 17, 17.999, 18.001, 121, 999, 21.5, "", "Пять", None, -1
    ])
    def test_invalid_age(self, user_factory, invalid_age):
        """
        Проверка, что невалидный возраст вызывает ValidationError
        """
        with pytest.raises(ValidationError):
            user_factory(age=invalid_age)


@pytest.mark.admin_user
class TestAdminUser:
    """
    Класс с тестовыми случаями для модели AdminUser
    """

    def test_admin_user_inherits(self, admin_user_factory):
        """
        Проверка наследования атрибутов от родительских моделей
        и наличия своих полей
        """
        admin = admin_user_factory()
        assert hasattr(admin, 'first_name')
        assert hasattr(admin, 'password')
        assert hasattr(admin, 'role')
        assert hasattr(admin, 'has_permission')

    @pytest.mark.parametrize("role", ["admin", "superadmin"])
    def test_valid_admin_role(self, admin_user_factory, role):
        """
        Проверка валидных ролей администратора
        """
        admin_user = admin_user_factory(role=role)
        assert isinstance(admin_user, AdminUser)
        assert admin_user.role in ["admin", "superadmin"]

    @pytest.mark.parametrize("invalid_role", [
        "user", "base_user", "админ", "administrator", "Admin", "super_admin",
        "adm1n", None, "super admin"
    ])
    def test_invalid_admin_role(self, admin_user_factory, invalid_role):
        """
        Проверка, что невалидные роли вызывают ValidationError
        """
        with pytest.raises(ValidationError):
            admin_user_factory(role=invalid_role)

    @pytest.mark.parametrize("permission", [
        "read", "write", "delete"
    ])
    def test_admin_has_permission(self, admin_user_factory, permission):
        """
        Проверка прав доступа обычного администратора
        """
        admin_user = admin_user_factory()
        assert admin_user.has_permission(permission)

    @pytest.mark.parametrize("permission", [
        "read", "write", "delete", "manage_users", "manage_admins"
    ])
    def test_superadmin_has_permission(self, admin_user_factory, permission):
        """
        Проверка прав доступа суперадминистратора
        """
        admin_user = admin_user_factory(role="superadmin")
        assert admin_user.has_permission(permission)

    @pytest.mark.parametrize("permission", [
        "manage_users", "manage_admins", None, "", 0, 1,
        "READ", "WRITE", "DELETE"
    ])
    def test_admin_has_no_permission(self, admin_user_factory, permission):
        """
        Проверка отсутствия прав доступа у обычного администратора 
        в т.ч. невалидные значения
        """
        admin_user = admin_user_factory()
        assert not admin_user.has_permission(permission)

    @pytest.mark.parametrize("permission", [
        "READ", "WRITE", "DELETE", 0, 1, "", None
    ])
    def test_superadmin_has_no_permission(
        self, admin_user_factory, permission
    ):
        """
        Проверка отсутствия прав доступа у суперадминистратора
        для невалидных значений
        """
        admin_user = admin_user_factory(role="superadmin")
        assert not admin_user.has_permission(permission)
