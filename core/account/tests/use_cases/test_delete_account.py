import logging
from unittest.mock import Mock

import pytest
from rest_framework import status

from core.account.entities import Account
from core.account.exceptions import AccountNotFound
from core.account.factory import AccountFactory
from core.account.mapper import account_model_to_entity
from core.account.tests.factory import AccountModelFactory
from core.shared.exceptions import CustomAPIException


class TestDeleteAccount:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_delete_account()
        sut._get_account_by_id = Mock(return_value=self.account)
        sut._account_repository.delete_account = Mock()
        return sut

    def setup_method(self):
        self.account = AccountModelFactory.create(as_entity=True)

    @pytest.mark.django_db
    def test_should_call_get_account_by_id_with_correct_params(self, sut):
        sut.delete(account_id=self.account.id)

        sut._get_account_by_id.assert_called_once_with(self.account.id)

    @pytest.mark.django_db
    def test_should_call_delete_account_with_correct_params(self, sut):
        sut.delete(account_id=self.account.id)

        sut._account_repository.delete_account.assert_called_once_with(self.account)

    @pytest.mark.django_db
    def test_should_log_when_account_is_deleted(self, sut, caplog):
        with caplog.at_level(logging.INFO):
            sut.delete(account_id=self.account.id)

        assert f'Account [{self.account.id}] deleted successfully.' in caplog.text


class TestGetAccountById:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_delete_account()
        sut._account_repository.safe_get = Mock(return_value=self.account)
        return sut

    def setup_method(self):
        self.account = AccountModelFactory.create(as_entity=True)

    @pytest.mark.django_db
    def test_should_call_safe_get_with_correct_params(self, sut):
        sut._get_account_by_id(account_id=self.account.id)

        sut._account_repository.safe_get.assert_called_once_with(id=self.account.id)

    @pytest.mark.django_db
    def test_should_raise_error_when_account_not_found(self, sut):
        sut._account_repository.safe_get.return_value = None

        with pytest.raises(AccountNotFound) as exc_info:
            sut._get_account_by_id(account_id=self.account.id)

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert 'Account not found.' == str(exc_info.value)

    @pytest.mark.django_db
    def test_should_log_when_account_not_found(self, sut, caplog):
        sut._account_repository.safe_get.return_value = None

        with pytest.raises(AccountNotFound):
            with caplog.at_level(logging.WARNING):
                sut._get_account_by_id(account_id=self.account.id)

        assert f'Account with id [{self.account.id}] was not found.' in caplog.text
