import pytest
from django.db import IntegrityError

from core.account.models import AccountModel


class TestAccountModel:
    def setup_method(self):
        self.name = 'client name'
        self.email = 'test@email.com'
        self.password = 'Password@123'

    @pytest.mark.django_db
    def test_should_create_a_normal_user_account_successfully(self):
        account = AccountModel.objects.create(name=self.name, email=self.email, password=self.password)

        assert account.name == self.name
        assert account.email == self.email
        assert account.check_password(self.password)
        assert account.is_active
        assert not account.is_staff
        assert not account.is_superuser

    @pytest.mark.django_db
    def test_should_create_a_super_user_account_successfully(self):
        account = AccountModel.objects.create_superuser(name=self.name, email=self.email, password=self.password)

        assert account.is_staff
        assert account.is_superuser

    @pytest.mark.django_db
    def test_should_should_raise_error_when_email_is_not_provided(self):
        with pytest.raises(ValueError) as exc:
            AccountModel.objects.create(name=self.name, email=None, password=self.password)

        assert 'The email is required.' in str(exc.value)

    @pytest.mark.django_db
    def test_should_should_raise_error_when_password_is_not_provided(self):
        with pytest.raises(ValueError) as exc:
            AccountModel.objects.create(name=self.name, email=self.email, password=None)

        assert 'The password is required.' in str(exc.value)

    @pytest.mark.django_db
    def test_should_should_raise_error_when_email_is_not_unique(self):
        AccountModel.objects.create(name=self.name, email=self.email, password=self.password)

        with pytest.raises(IntegrityError):
            AccountModel.objects.create(name=self.name, email=self.email, password=self.password)

    @pytest.mark.django_db
    def test_str_representation(self):
        account = AccountModel.objects.create(name=self.name, email=self.email, password=self.password)

        assert str(account) == f'Account - {account.id}'

    @pytest.mark.django_db
    def test_repr_representation(self):
        account = AccountModel.objects.create(name=self.name, email=self.email, password=self.password)

        assert repr(account) == f'Account id={account.id} name={account.name} email={account.email}'
