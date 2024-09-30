import os
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = (
        "Generates the OpenAPI schema and saves it to static/docs/schema.yml"
    )

    def handle(self, *args, **options):
        output_dir = os.path.join("static", "docs")
        output_file = os.path.join(output_dir, "schema.yml")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        self.stdout.write("Generating OpenAPI schema...")
        call_command("spectacular", "--file", output_file)
        self.stdout.write(f"Schema generated and saved to {output_file}")
