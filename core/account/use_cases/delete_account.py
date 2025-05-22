import logging
from uuid import UUID

from core.account.entities import Account
from core.account.exceptions import AccountNotFound
from core.account.repository import AccountRepository

logger = logging.getLogger(__name__)


class DeleteAccount:
    def __init__(self, account_repository: AccountRepository):
        self._account_repository = account_repository

    def delete(self, account_id: UUID) -> None:
        account = self._get_account_by_id(account_id)

        self._account_repository.delete_account(account)


    def _get_account_by_id(self, account_id: UUID) -> Account:
        account = self._account_repository.safe_get(id=account_id)

        if not account:
            logger.warning(f'Account with id [{account_id}] was not found.')
            raise AccountNotFound()

        return account
