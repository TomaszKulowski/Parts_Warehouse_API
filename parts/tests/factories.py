"""
This module defines factory classes for creating instances of the Part and Categories models.
"""
import random
import string

import factory

from faker import Factory as FakerFactory

from parts.models import Part
from categories.tests.factories import SideCategoryFactory


PARTS = [
    "Resistor",
    "Capacitor",
    "Inductor",
    "Diode",
    "Transistor",
    "Integrated Circuit",
    "Connector",
    "Sensor",
    "Microcontroller",
    "Power Supply",
]
CHARS = list(string.ascii_letters) + list(string.digits)

faker_factory = FakerFactory.create()


class PartFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating instances of the Part class.
    """
    class Meta:
        model = Part

    serial_number = factory.LazyAttribute(lambda x: ''.join(random.choices(string.ascii_letters, k=10)))
    name = factory.LazyAttribute(lambda x: random.choice(PARTS))
    description = factory.LazyAttribute(lambda x: faker_factory.sentence(10))
    category_id = factory.SubFactory(SideCategoryFactory)
    quantity = factory.LazyAttribute(lambda x: random.randint(0, 100))
    price = factory.LazyAttribute(lambda x: round(random.uniform(1.0, 100.0), 2))
    location = factory.LazyAttribute(lambda x: {
        'room': random.choice(CHARS),
        'bookcase': random.choice(CHARS),
        'shelf': random.choice(CHARS),
        'cuvette': random.choice(CHARS),
        'column': random.choice(CHARS),
        'row': random.choice(CHARS),
    })
