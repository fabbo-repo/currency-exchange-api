from django.core.management.base import BaseCommand
from django.conf import settings
import logging
from api_key.models import APIKey, ApiUser
import secrets

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py apikey --usage <USAGE> --username <USERNAME>
    ~~~
    """

    help = "Create api key"

    def add_arguments(self, parser):
        parser.add_argument(
            "--usage",
            default=-1,
            type=int
        )
        parser.add_argument(
            "--username",
            type=str
        )

    def handle(self, *args, **options):
        try:
            if options["usage"] and options["username"]:
                api_key = APIKey.objects.create(
                    key=secrets.token_urlsafe(30),
                    user=ApiUser.objects.create(username=options["username"]),
                    usage_left=options["usage"],
                    is_active=True
                )
                print("#"*40)
                print("API key: " + str(api_key))
                print("#"*40)
            else:
                if not options["usage"]:
                    print("Usage not provided")
                if not options["username"]:
                    print("Username not provided")
        except Exception as ex:
            print(ex)
