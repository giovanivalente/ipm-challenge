from abc import ABC, abstractmethod

from django.core.exceptions import ObjectDoesNotExist

from core.account.entities import Account
from core.account.mapper import account_model_to_entity
from core.account.models import AccountModel


class AccountRepository(ABC):
    @abstractmethod
    def create(self, **kwargs) -> Account:
        pass  # pragma: no cover

    @abstractmethod
    def safe_get(self, **kwargs) -> Account | None:
        pass  # pragma: no cover


class AccountRepositoryDB(AccountRepository):
    model = AccountModel

    def create(self, **kwargs) -> Account:
        account: AccountModel = self.model.objects.create(**kwargs)
        return account_model_to_entity(account)

    def safe_get(self, **kwargs) -> Account | None:
        try:
            account: AccountModel = self.model.objects.get(**kwargs)
            return account_model_to_entity(account)
        except ObjectDoesNotExist:
            return None
