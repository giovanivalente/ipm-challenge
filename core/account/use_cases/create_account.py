import logging

from rest_framework import status

from core.account.entities import Account
from core.account.repository import AccountRepository
from core.shared.exceptions import CustomAPIException

logger = logging.getLogger(__name__)


class CreateAccount:
    def __init__(self, account_repository: AccountRepository):
        self._account_repository = account_repository

    def create_new_account(self, name: str, email: str, password: str) -> Account:
        self._validate_existing_account(email)

        account = self._account_repository.create(name=name, email=email, password=password)
        logger.info(f'Account [{account.id}] created successfully.')

        return account

    def _validate_existing_account(self, email: str) -> None:
        account_already_exists = self._account_repository.safe_get(email=email)

        if account_already_exists:
            logger.warning(f'An account with the email [{account_already_exists.email}] already exists.')
            raise CustomAPIException('An account with this email already exists.', status_code=status.HTTP_409_CONFLICT)
