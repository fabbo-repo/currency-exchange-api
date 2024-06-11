import logging
import secrets

from django.core.management.base import BaseCommand

from src.api_key.models import APIKey, ApiUser

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Will be executed with:
    ~~~
    python manage.py apikey --usage <USAGE> --name <NAME>
    ~~~
    """

    help = "Create api key"

    def add_arguments(self, parser):
        parser.add_argument(
            "--usage",
            default=-1,
            required=False,
            type=int
        )
        parser.add_argument(
            "--name",
            required=True,
            type=str
        )
        parser.add_argument(
            "--key",
            required=False,
            type=str
        )

    def handle(self, *args, **options):
        try:
            if options["usage"] and options["name"]:
                key = options["key"] if options["key"] else secrets.token_urlsafe(30)
                if not APIKey.objects.filter(key=key).exists():
                    api_user, _ = ApiUser.objects.get_or_create(username=options["name"])
                    APIKey.objects.create(
                        key=key,
                        user=api_user,
                        usage_left=options["usage"],
                        is_active=True
                    )
                print("#" * 40)
                print("API key: " + str(key))
                print("#" * 40)
            else:
                if not options["usage"]:
                    print("Usage not provided")
                if not options["name"]:
                    print("Key name not provided")
        except Exception as ex:
            print(ex)
