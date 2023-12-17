from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='davydov.viktor.andreevich@gmail.com',
            first_name='Viktor',
            last_name='Davydov',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('Jhfkrfvijn2022')
        user.save()
