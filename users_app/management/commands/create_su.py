from django.core.management import BaseCommand

from users_app.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='m@sster.ru',
            first_name='Romka',
            last_name='T',
            is_staff=True,
            is_superuser=True,
            telegram ='Tagrom',
        )

        user.set_password('Aa12345!')
        user.save()
