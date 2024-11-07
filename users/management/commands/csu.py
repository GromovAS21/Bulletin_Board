from IPython.core.release import author
from django.core.management import BaseCommand

from baskets.models import Basket
from users.models import User


class Command(BaseCommand):
    """
    Команда для создания базовых правил
    """

    def handle(self, *args, **options):
        user = User.objects.create(
            email="admin@test.ru",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password("Qwerty")
        user.save()
        Basket.objects.create(author=user)
