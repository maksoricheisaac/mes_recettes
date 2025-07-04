from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Profile

class Command(BaseCommand):
    help = 'Crée les profils manquants pour tous les utilisateurs.'

    def handle(self, *args, **options):
        User = get_user_model()
        created_count = 0
        for user in User.objects.all():
            profile, created = Profile.objects.get_or_create(user=user)
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'{created_count} profils créés.'))
