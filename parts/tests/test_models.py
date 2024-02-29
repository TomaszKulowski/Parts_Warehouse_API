"""
This module contains a unit test for Part model.
"""
import pytest

from django.core.exceptions import ValidationError

from categories.tests.factories import SideCategoryFactory
from parts.models import Part


@pytest.mark.django_db
def test_successfully_create_part():
    """
    Test case for creating parts in the database.
    """
    part_1 = Part.objects.create(
        serial_number='abc123',
        name='part_1',
        description='test descrption',
        category_id=SideCategoryFactory(),
        quantity=12,
        price=00.82,
        location={
            'room': '12',
            'bookcase': 'a1',
            'shelf': 'z',
            'cuvette': '2',
            'column': 'c3',
            'row': '2',
        }
    )
    part_2 = Part.objects.create(
        serial_number='abc123q',
        name='part_2',
        description='test descrption',
        category_id=SideCategoryFactory(),
        quantity=1211,
        price=10.82,
        location={
            'room': '12',
            'bookcase': 'a1',
            'shelf': 'z',
            'cuvette': '2',
            'column': 'c3',
            'row': '2',
        }
    )

    parts = Part.objects.all()

    assert parts[0] == part_1
    assert parts[1] == part_2
    assert len(parts) == 2


@pytest.mark.django_db
def test_wrong_location_field():
    """
    Test case for validating the creation of a Part instance with an invalid 'location' field.
    """
    with pytest.raises(ValidationError) as error:
        Part.objects.create(
            serial_number='abc123',
            name='part_1',
            description='test descrption',
            category_id=SideCategoryFactory(),
            quantity=12,
            price=00.82,
            location={
                'rooms': '12',
            }
        )

    assert error.type == ValidationError
    assert str(error.value) == "['Invalid field: rooms']"
