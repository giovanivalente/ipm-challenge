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

    @abstractmethod
    def update_account(self, account: Account, /, **kwargs) -> Account:
        pass  # pragma: no cover

    @abstractmethod
    def check_password(self, account: Account, password: str) -> Account:
        pass  # pragma: no cover

    @abstractmethod
    def delete_account(self, account: Account) -> None:
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

    def update_account(self, account: Account, /, **kwargs) -> Account:
        account_model = AccountModel.objects.get(id=account.id)

        has_changes = False

        for key, value in kwargs.items():
            if key == 'password':
                account_model.set_password(value)
                has_changes = True
            else:
                current_value = getattr(account_model, key)
                if value != current_value:
                    setattr(account_model, key, value)
                    has_changes = True

        if has_changes:
            account_model.save()

        return account_model_to_entity(account_model)

    def check_password(self, account: Account, password: str) -> bool:
        account_model = AccountModel.objects.get(id=account.id)

        return account_model.check_password(password)

    def delete_account(self, account: Account) -> None:
        account_model = AccountModel.objects.get(id=account.id)
        account_model.delete()
