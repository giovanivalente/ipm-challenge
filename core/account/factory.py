from core.account.repository import AccountRepository, AccountRepositoryDB
from core.account.use_cases.create_account import CreateAccount
from core.account.use_cases.db_get_account import DbGetAccount


class AccountFactory:
    @classmethod
    def make_account_repository(cls) -> AccountRepository:
        return AccountRepositoryDB()

    @classmethod
    def make_create_account(cls) -> CreateAccount:
        return CreateAccount(account_repository=cls.make_account_repository())

    @classmethod
    def make_db_get_account(cls) -> DbGetAccount:
        return DbGetAccount(account_repository=cls.make_account_repository())
