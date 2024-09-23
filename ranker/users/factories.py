import factory
from django.contrib.auth.hashers import (
    make_password,
)
from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker("email")
    username = factory.Faker("user_name")
    name = factory.Faker("name")
    gender = User.Gender.MALE
    plain_password = "password"
    password = factory.LazyAttribute(lambda o: make_password(o.plain_password))

    class Meta:
        model = User
        exclude = ("plain_password",)

    class Params:
        admin = factory.Trait(is_superuser=True)
        staff = factory.Trait(is_staff=True)
        has_phone_number = factory.Trait(
            phone_number=factory.Faker("phone_number")
        )
