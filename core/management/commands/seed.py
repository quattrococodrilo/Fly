import importlib

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run seeder"

    def add_arguments(self, parser):
        parser.add_argument(
            "--seeder", help="One or more seeder modules separated by comma."
        )

    def handle(self, *args, **options):
        if not options["seeder"]:
            self.stdout.write("No seeder specified", self.style.ERROR)
            return

        self.stdout.write("Running seeder...")
        self.stdout.write()

        seeder_list = options["seeder"].split(",")

        for seeder in seeder_list:
            module, fn = seeder.rsplit(".")
            
            full_path_module = f"apps.{module}.seeder.seeders"
            
            self.stdout.write(f'{full_path_module}... OK', self.style.SUCCESS)
            self.stdout.write()
            
            seeder_module = importlib.import_module(full_path_module)
            
            seeder_function = getattr(seeder_module, fn)
            
            seeder_function()

        self.stdout.write(self.style.SUCCESS("Done!"))