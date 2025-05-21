from uuid import uuid4

import factory
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory.django import DjangoModelFactory

from core.account.mapper import account_model_to_entity
from core.account.models import AccountModel


class AccountModelFactory(DjangoModelFactory):
    class Meta:
        model = AccountModel
        django_get_or_create = ('email',)

    id = factory.LazyFunction(uuid4)
    name = factory.Faker('name')
    email = factory.Sequence(lambda n: f'user{n}@test.com')
    is_active = True
    is_staff = False
    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
    password = factory.LazyFunction(lambda: make_password('Password@123'))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        as_entity = kwargs.pop('as_entity', False)
        obj = super()._create(model_class, *args, **kwargs)

        if as_entity:
            return account_model_to_entity(obj)
        return obj
