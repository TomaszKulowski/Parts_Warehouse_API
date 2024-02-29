"""
This module contains unit tests for testing the PartSerializer class.
"""
import pytest

from django.test import TestCase
from rest_framework.exceptions import ValidationError

from .factories import PartFactory
from categories.tests.factories import SideCategoryFactory, MainCategoryFactory
from parts.serializers import PartSerializer


class TestPartSerializer(TestCase):
    """
    Test case for the PartSerializer.
    """
    def setUp(self):
        """
        Set up necessary components for each test.
        """
        category = SideCategoryFactory()
        self.part_attributes = {
            '_id': '123123123123',
            'serial_number': 'abc123',
            'name': 'part_1',
            'description': 'test descrption',
            'category_id': category,
            'quantity': 12,
            'price': 00.82,
            'location': {
                'room': '12',
                'bookcase': 'a1',
                'shelf': 'z',
                'cuvette': '2',
                'column': 'c3',
                'row': '2',
            }
        }
        self.part = PartFactory(**self.part_attributes)

        self.serializer_data = {
            'serial_number': '123123a',
            'name': 'part_A',
            'description': 'test descrption',
            'category_id': category,
            'quantity': 222,
            'price': 10.82,
            'location': {
                'room': '99',
                'bookcase': 'a19',
                'shelf': 'zy',
                'cuvette': '211',
                'column': 'c3z',
                'row': '211',
            }
        }
        self.serializer = PartSerializer(instance=self.part)

    def test_contains_expected_fields(self):
        """
        Test whether the serialized data contains all expected fields.
        """
        data = self.serializer.data
        assert set(data.keys()) == set(self.part_attributes.keys())

    def test_fields_content(self):
        """
        Test whether the serialized data contains correct field content.
        """
        data = self.serializer.data
        assert data['_id'] == self.part_attributes['_id']
        assert data['serial_number'] == self.part_attributes['serial_number']
        assert data['name'] == self.part_attributes['name']
        assert data['description'] == self.part_attributes['description']
        assert data['category_id'] == str(self.part_attributes['category_id']._id)
        assert data['quantity'] == self.part_attributes['quantity']
        assert data['price'] == self.part_attributes['price']
        assert data['location'] == self.part_attributes['location']

    def test_to_representation(self):
        """
        Test the representation of the serialized data.
        """
        representation = self.serializer.to_representation(self.part)

        assert set(self.part_attributes) == set(representation.keys())
        assert len(representation) == 8

    def test_validate_add_part_to_side_category(self):
        """
        Test validation for adding a part to a side category.
        """
        validated_attrs = self.serializer.validate(self.part_attributes)

        assert validated_attrs == self.part_attributes

    def test_validate_add_part_to_main_category(self):
        """
        Test validation for adding a part to a main category.
        """
        main_category = MainCategoryFactory()
        part_attrs_with_main_category = self.part_attributes.copy()
        part_attrs_with_main_category['category_id'] = main_category

        with pytest.raises(ValidationError) as error:
            self.serializer.validate(part_attrs_with_main_category)

        assert error.type == ValidationError
