import logging
from unittest.mock import Mock

import pytest
from rest_framework import status

from core.account.entities import Account
from core.account.factory import AccountFactory
from core.account.mapper import account_model_to_entity
from core.account.tests.factory import AccountModelFactory
from core.shared.exceptions import CustomAPIException


class TestCreateNewAccount:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_create_account()
        sut._validate_existing_account = Mock()
        sut._account_repository.create = Mock(return_value=self.account)
        return sut

    def setup_method(self):
        self.password = 'Password@123'
        self.account_model = AccountModelFactory.create(password=self.password)
        self.account = account_model_to_entity(self.account_model)

    @pytest.mark.django_db
    def test_should_call_validate_existing_account_with_correct_params(self, sut):
        sut.create_new_account(name=self.account.name, email=self.account.email, password=self.password)

        sut._validate_existing_account.assert_called_once_with(self.account.email)

    @pytest.mark.django_db
    def test_should_call_account_repository_create_with_correct_params(self, sut):
        sut.create_new_account(name=self.account.name, email=self.account.email, password=self.password)

        sut._account_repository.create.assert_called_once_with(
            name=self.account.name, email=self.account.email, password=self.password
        )

    @pytest.mark.django_db
    def test_should_log_when_account_is_created(self, sut, caplog):
        with caplog.at_level(logging.INFO):
            sut.create_new_account(name=self.account.name, email=self.account.email, password=self.password)

        assert f'Account [{self.account.id}] created successfully.' in caplog.text

    @pytest.mark.django_db
    def test_should_return_created_account(self, sut):
        account = sut.create_new_account(name=self.account.name, email=self.account.email, password=self.password)

        assert account.email == self.account.email
        assert isinstance(account, Account)


class TestValidateExistingAccount:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_create_account()
        sut._account_repository.safe_get = Mock(return_value=None)
        return sut

    def setup_method(self):
        self.account = AccountModelFactory.create()

    @pytest.mark.django_db
    def test_should_call_safe_get_with_correct_params(self, sut):
        sut._validate_existing_account(email=self.account.email)

        sut._account_repository.safe_get.assert_called_once_with(email=self.account.email)

    @pytest.mark.django_db
    def test_should_raise_error_when_account_already_exists(self, sut):
        sut._account_repository.safe_get.return_value = self.account

        with pytest.raises(CustomAPIException) as exc_info:
            sut._validate_existing_account(email=self.account.email)

        assert exc_info.value.status_code == status.HTTP_409_CONFLICT
        assert 'An account with this email already exists.' == str(exc_info.value)

    @pytest.mark.django_db
    def test_should_log_when_raise_exception(self, sut, caplog):
        sut._account_repository.safe_get.return_value = self.account

        with pytest.raises(CustomAPIException):
            with caplog.at_level(logging.WARNING):
                sut._validate_existing_account(email=self.account.email)

        assert f'An account with the email [{self.account.email}] already exists.' in caplog.text
