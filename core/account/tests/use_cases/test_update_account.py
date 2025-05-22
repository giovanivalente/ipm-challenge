import logging
from unittest.mock import Mock

import pytest

from core.account.exceptions import AccountNotFound
from core.account.factory import AccountFactory
from core.account.tests.factory import AccountModelFactory
from core.shared.exceptions import CustomAPIException


class TestUpdate:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_update_account()
        sut._get_account_by_id = Mock(return_value=self.account)
        sut._validate_current_password = Mock()
        sut._account_repository.update_account = Mock(return_value=self.updated_account)
        return sut

    def setup_method(self):
        self.account = AccountModelFactory.create(as_entity=True)
        self.updated_account = AccountModelFactory.create(as_entity=True)

    @pytest.mark.django_db
    def test_should_call_get_account_by_id_with_correct_params(self, sut):
        sut.update(account_id=self.account.id, name='name')

        sut._get_account_by_id.assert_called_once_with(self.account.id)

    @pytest.mark.django_db
    def test_should_call_validate_current_password_with_correct_params(self, sut):
        sut.update(account_id=self.account.id, current_password='current_password')

        sut._validate_current_password.assert_called_once_with(
            account=self.account, current_password='current_password'
        )

    @pytest.mark.django_db
    def test_should_call_update_account_with_correct_params(self, sut):
        sut.update(account_id=self.account.id, name='name')

        sut._account_repository.update_account.assert_called_once_with(self.account, name='name')

    @pytest.mark.django_db
    def test_should_call_log_info_when_update_at_least_one_field(self, sut, caplog):
        with caplog.at_level(logging.INFO):
            sut.update(account_id=self.account.id, name='name')

        assert f'Account [{self.account.id}] was successfully updated.' in caplog.text


class TestGetAccountById:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_update_account()
        sut._account_repository.safe_get = Mock(return_value=self.account)
        return sut

    def setup_method(self):
        self.account = AccountModelFactory.create(as_entity=True)

    @pytest.mark.django_db
    def test_should_call_safe_get_with_correct_params(self, sut):
        sut._get_account_by_id(account_id=self.account.id)

        sut._account_repository.safe_get.assert_called_once_with(id=self.account.id)

    @pytest.mark.django_db
    def test_should_raise_account_not_found(self, sut):
        sut._account_repository.safe_get.return_value = None

        with pytest.raises(AccountNotFound):
            sut._get_account_by_id(account_id=self.account.id)

    @pytest.mark.django_db
    def test_should_log_warning_when_account_not_found(self, sut, caplog):
        sut._account_repository.safe_get.return_value = None

        with pytest.raises(AccountNotFound):
            with caplog.at_level(logging.WARNING):
                sut._get_account_by_id(account_id=self.account.id)

        assert f'Account with id [{self.account.id}] was not found.' in caplog.text


class TestValidateCurrentPassword:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_update_account()
        sut._account_repository.check_password = Mock(return_value=True)
        return sut

    def setup_method(self):
        self.account = AccountModelFactory.create(as_entity=True)

    @pytest.mark.django_db
    def test_should_call_check_password_with_correct_params(self, sut):
        sut._validate_current_password(account=self.account, current_password='current_password')

        sut._account_repository.check_password.assert_called_once_with(
            account=self.account, password='current_password'
        )

    @pytest.mark.django_db
    def test_should_raise_invalid_password(self, sut):
        sut._account_repository.check_password.return_value = False

        with pytest.raises(CustomAPIException):
            sut._validate_current_password(account=self.account, current_password='current_password')

    @pytest.mark.django_db
    def test_should_log_warning_when_password_is_invalid(self, sut, caplog):
        sut._account_repository.check_password.return_value = False

        with pytest.raises(CustomAPIException):
            with caplog.at_level(logging.WARNING):
                sut._validate_current_password(account=self.account, current_password='current_password')

        assert 'The provided current password is invalid.' in caplog.text
