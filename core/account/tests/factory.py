from uuid import uuid4

import factory
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from factory.django import DjangoModelFactory

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
