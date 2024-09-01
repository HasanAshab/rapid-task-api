from django.core.management.base import (
    BaseCommand,
)
from ranker.users.factories import (
    UserFactory,
)


class Command(BaseCommand):
    help = "Create a user and obtain auth token for testing"

    def handle(self, *args, **options):
        user = UserFactory()
        self.stdout.write("Email: " + user.email)
        self.stdout.write("Username: " + user.username)
        self.stdout.write("Password: " + UserFactory.plain_password)
