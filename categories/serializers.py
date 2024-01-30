"""
This module defines a Django Serializer.
"""
from typing import Any

from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Category' model.

    Methods:
        to_representation(instance): Converts the model instance to a Python dictionary for serialization.
        validate(attrs): Performs validation checks on the provided attributes before saving.
    """
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance: Any) -> dict:
        """
        Convert the given model instance to a dictionary representation for serialization.

        Overrides the default behavior to include string representations of the '_id'
        and 'parent_id' fields in the serialized data for improved readability.

        Args:
            instance: The model instance to be serialized.

        Returns:
            dict: A dictionary representing the serialized data.
        """
        rep = super().to_representation(instance)

        if instance._id:
            rep['_id'] = str(instance._id)
        if instance.parent_id:
            rep['parent_id'] = str(instance.parent_id)
        return rep

    def validate(self, attrs: Any) -> dict:
        """
        Validate the attributes before creating or updating an instance.

        Checks if a Category with the same 'name' and 'parent_id' already exists in the database.
        If a duplicate is found, raises a ValidationError.

        Args:
            attrs (Dict[str, Any]): The attributes to be validated.

        Returns:
            Dict[str, Any]: The validated attributes.

        Raises:
            serializers.ValidationError: If a Category with the same 'name' and 'parent_id' already exists.
        """
        name = attrs.get('name')
        parent_id = attrs.get('parent_id')
        if Category.objects.filter(name=name, parent_id=parent_id).exists():
            raise serializers.ValidationError('Category with the same name and parent_id already exists.')
        return attrs
