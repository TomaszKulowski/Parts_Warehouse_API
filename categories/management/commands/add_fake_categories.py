"""
This management command adds fake categories to the database using the SideCategoryFactory.

Usage:
    python manage.py add_fake_categories -n <number>

Arguments:
    -n, --number: Number of categories to create.

Example:
    python manage.py add_fake_categories -n 10

This command creates a specified number of fake main and side categories using the SideCategoryFactory.
"""
from sys import stdout

from django.core.management import BaseCommand

from categories.tests.factories import SideCategoryFactory


class Command(BaseCommand):
    help = 'Add fake categories.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n',
            '--number',
            help='Number of categories to create',
            type=int,
            dest='number',
        )

    def handle(self, *args, **options):
        n = options.get('number')
        SideCategoryFactory.create_batch(n)
        stdout.write(f'Successfully created {n} main and side categories.')
