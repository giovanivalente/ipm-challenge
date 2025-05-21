# import logging
# from uuid import UUID
#
# from core.account.entities import Account
# from core.account.exceptions import AccountNotFound
# from core.account.mapper import account_entity_to_model
# from core.account.repository import AccountRepository
# from core.shared.exceptions import CustomAPIException
#
# logger = logging.getLogger(__name__)
#
#
# class UpdateAccount:
#     def __init__(self, account_repository: AccountRepository):
#         self._account_repository = account_repository
#
#     def update(self, account_id: UUID, **kwargs) -> Account:
#         account = self._get_account_by_id(account_id)
#
#         if kwargs.get('current_password'):
#             self._validate_current_password(current_password=kwargs['current_password'])
#
#     def _get_account_by_id(self, account_id: UUID) -> Account:
#         account = self._account_repository.safe_get(id=account_id)
#
#         if not account:
#             logger.warning(f'Account with id [{account_id}] was not found.')
#             raise AccountNotFound()
#
#         return account
#
#     def _validate_current_password(self, account: Account, current_password: str) -> None:
#         account_model = account_entity_to_model(account)
#
#         if not account_model.check_password(current_password):
#             raise CustomAPIException('Invalid ')
