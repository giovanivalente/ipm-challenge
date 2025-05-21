import logging
from unittest.mock import Mock
from uuid import uuid4

import pytest
from rest_framework import status

from core.account.exceptions import AccountNotFound
from core.account.factory import AccountFactory
from core.account.tests.factory import AccountModelFactory


class TestGetById:
    @pytest.fixture
    def sut(self):
        sut = AccountFactory.make_db_get_account()
        sut._account_repository.safe_get = Mock(return_value=self.account)
        return sut

    def setup_method(self):
        self.account = AccountModelFactory.create(as_entity=True)

    @pytest.mark.django_db
    def test_should_call_safe_get_with_correct_params(self, sut):
        sut.get_by_id(account_id=self.account.id)

        sut._account_repository.safe_get.assert_called_once_with(id=self.account.id)

    @pytest.mark.django_db
    def test_should_raise_error_when_account_is_not_found(self, sut):
        sut._account_repository.safe_get.return_value = None

        with pytest.raises(AccountNotFound) as exc_info:
            sut.get_by_id(account_id=uuid4())

        assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
        assert 'Account not found.' == str(exc_info.value)

    @pytest.mark.django_db
    def test_should_log_when_raise_exception(self, sut, caplog):
        sut._account_repository.safe_get.return_value = None
        account_id = uuid4()

        with pytest.raises(AccountNotFound):
            with caplog.at_level(logging.WARNING):
                sut.get_by_id(account_id=account_id)

        assert f'Account with id [{account_id}] was not found.' in caplog.text
