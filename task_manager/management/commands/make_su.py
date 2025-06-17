from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ModuleNotFoundError:
            pass

        SU_USERNAME = os.getenv("SU_USERNAME")
        SU_PASSWORD = os.getenv("SU_PASSWORD")
        
        User = get_user_model()

        if not User.objects.filter(username=SU_USERNAME).exists():

            User.objects.create_superuser(
                username=SU_USERNAME,
                email='coder108@gmail.com',
                password=SU_PASSWORD
                )
            self.stdout.write(self.style.SUCCESS('create su - ok'))
        else:
            self.stdout.write(self.style.WARNING('create su - exists'))