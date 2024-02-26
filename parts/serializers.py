"""
This module defines a Django Serializer.
"""
from json import loads
from rest_framework.exceptions import ValidationError

from .models import Part
from categories.models import Category

from rest_framework import serializers
from Parts_Warehouse_API.validators import valid_object_id


class PartSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Part' model.

    Methods:
        validate(data): Perform additional validation on the input data before saving.
        to_representation(instance): Convert the model instance to a JSON-compatible representation.
    """
    class Meta:
        model = Part
        fields = '__all__'

    def validate(self, data: dict) -> dict:
        """
        Validate the input data before saving.

        This method performs additional validation on the input data, checking if the specified
        'category_id' belongs to a base category. If so, a ValidationError is raised.

        Args:
            data (dict): The input data to be validated.

        Raises:
            ValidationError: If the 'category_id' belongs to a base category.

        Returns:
            dict: The validated data
        """
        category_id = data.get('category_id')
        if category_id:
            if Category.objects.filter(pk=valid_object_id(category_id._id)).first().parent_id is None:
                raise ValidationError({'error': 'Cannot add data to a base category.'})
        return data

    def to_representation(self, instance: Part) -> dict:
        """
        Convert the model instance to a JSON-compatible representation.

        This method overrides the default behavior to handle special cases like converting
        ObjectId fields to strings and transforming the 'location' field from a string to a dictionary.

        Args:
            instance (Part): The 'Part' model instance to be converted.

        Returns:
            dict: The JSON-compatible representation of the model instance.
        """
        rep = super().to_representation(instance)

        if instance._id:
            rep['_id'] = str(instance._id)
        if instance.category_id:
            rep['category_id'] = str(instance.category_id._id)
        if instance.location:
            if isinstance(instance.location, str):
                rep['location'] = loads(instance.location)
            else:
                rep['location'] = dict(instance.location)
        return rep
