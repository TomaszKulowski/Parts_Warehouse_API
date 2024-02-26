"""
This module contains unit tests for testing the CategorySerializer class.
"""
import pytest

from rest_framework.serializers import ValidationError
from django.test import TestCase

from .factories import MainCategoryFactory, SideCategoryFactory
from categories.serializers import CategorySerializer


class TestCategorySerializer(TestCase):
    """
    Test case class for testing the CategorySerializer.
    """
    def setUp(self):
        """
        Set up necessary components for each test.
        """
        self.main_category_attributes = {
            'name': 'Category_A',
        }
        self.main_category = MainCategoryFactory(**self.main_category_attributes)

        self.side_category_attributes = {
            'name': 'Category_B',
            'parent_id': self.main_category,
        }
        self.side_category = SideCategoryFactory(**self.side_category_attributes)

        self.serializer_data = {
            'name': 'Category_1',
            'parent_id': self.main_category,
        }
        self.serializer = CategorySerializer(instance=self.side_category)

    def test_contains_expected_fields(self):
        """
        Test whether serializer data contains expected fields.
        """
        data = self.serializer.data
        assert set(data.keys()) == {'_id', 'name', 'parent_id'}

    def test_name_field_content(self):
        """
        Test the content of the 'name' field in the serializer data.
        """
        data = self.serializer.data
        assert data['name'] == self.side_category_attributes['name']

    def test_to_representation(self):
        """
        Test the to_representation method of the serializer.
        """
        representation = self.serializer.to_representation(self.side_category)

        assert '_id' in representation
        assert representation['_id'] == str(self.side_category._id)
        assert 'name' in representation
        assert representation['name'] == str(self.side_category.name)
        assert 'parent_id' in representation
        assert representation['parent_id'] == str(self.side_category.parent_id._id)

        assert len(representation) == 3

    def test_validate_unique_category(self):
        """
        Test validation of unique category attributes.
        """
        unique_attrs = {
            'name': 'Unique_Category',
        }
        validated_attrs = self.serializer.validate(unique_attrs)

        assert validated_attrs == unique_attrs

    def test_validate_duplicate_category(self):
        """
        Test validation of duplicate category attributes.
        """
        with pytest.raises(ValidationError) as main_category_error:
            self.serializer.validate(self.main_category_attributes)

        with pytest.raises(ValidationError) as side_category_error:
            self.serializer.validate(self.side_category_attributes)

        error_type = ValidationError
        error_message = 'Category with the same name and parent_id already exists.'

        assert main_category_error.type == error_type
        assert main_category_error.value.detail[0] == error_message
        assert side_category_error.type == error_type
        assert side_category_error.value.detail[0] == error_message
