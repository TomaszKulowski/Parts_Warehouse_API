"""
This module defines factory classes for creating instances of the Category model.
"""
import random

import factory

from .models import Category


CATEGORIES = [
    "Resistors",
    "Capacitors",
    "Inductors",
    "Diodes",
    "Transistors",
    "Integrated Circuits",
    "Connectors",
    "Sensors",
    "Microcontrollers",
    "Power Supplies",
]


class MainCategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating instances of the main category.
    """
    class Meta:
        model = Category

    name = factory.Sequence(lambda x: f'{random.choice(CATEGORIES)}_{x}')


class SideCategoryFactory(factory.django.DjangoModelFactory):
    """
    Factory class for creating instances of the side category.
    """
    class Meta:
        model = Category

    name = factory.Sequence(lambda x: f'{random.choice(CATEGORIES)}_{x}')
    parent_id = factory.SubFactory(MainCategoryFactory)
