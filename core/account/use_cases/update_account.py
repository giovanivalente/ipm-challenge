import logging
from uuid import UUID

from core.account.entities import Account
from core.account.exceptions import AccountNotFound
from core.account.repository import AccountRepository
from core.shared.exceptions import CustomAPIException

logger = logging.getLogger(__name__)


class UpdateAccount:
    def __init__(self, account_repository: AccountRepository):
        self._account_repository = account_repository

    def update(self, account_id: UUID, **kwargs) -> Account:
        current_password = kwargs.get('current_password', '')
        account = self._get_account_by_id(account_id)

        if current_password:
            self._validate_current_password(account=account, current_password=current_password)
            del kwargs['current_password']

        updated_account = self._account_repository.update_account(account, **kwargs)

        if updated_account != account:
            logger.info(f'Account [{account.id}] was successfully updated.')

        return updated_account

    def _get_account_by_id(self, account_id: UUID) -> Account:
        account = self._account_repository.safe_get(id=account_id)

        if not account:
            logger.warning(f'Account with id [{account_id}] was not found.')
            raise AccountNotFound()

        return account

    def _validate_current_password(self, account: Account, current_password: str) -> None:
        password_is_valid = self._account_repository.check_password(account=account, password=current_password)

        if not password_is_valid:
            logger.warning('The provided current password is invalid.')
            raise CustomAPIException('The provided current password is invalid.')
