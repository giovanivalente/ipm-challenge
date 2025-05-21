from core.account.entities import Account
from core.account.models import AccountModel


def account_model_to_entity(model_object: AccountModel) -> Account:
    return Account(
        id=model_object.id,
        name=model_object.name,
        email=model_object.email,
        is_active=model_object.is_active,
        is_staff=model_object.is_staff,
        created_at=model_object.created_at,
        updated_at=model_object.updated_at,
    )
