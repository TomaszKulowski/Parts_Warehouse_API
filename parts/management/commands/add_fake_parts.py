"""
This management command adds fake parts and categories to the database using the PartFactory.

Usage:
    python manage.py add_fake_parts_and_categories -n <number>

Arguments:
    -n, --number: Number of parts and categories to create.

Example:
    python manage.py add_fake_parts_and_categories -n 10

This command creates a specified number of fake parts and categories using the PartFactory.
"""
from sys import stdout

from django.core.management import BaseCommand

from parts.factories import PartFactory


class Command(BaseCommand):
    help = 'Add fake parts and categories.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of parts and categories to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        PartFactory.create_batch(n)
        stdout.write(f'Successfully created {n} parts and categories.')
