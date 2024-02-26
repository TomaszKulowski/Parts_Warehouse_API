from rest_framework import serializers

from bson import ObjectId


def valid_object_id(value: str) -> ObjectId:
    """
    Validate if the provided value is a valid ObjectId.

    Args:
        value (str): The value to be validated.

    Returns:
        ObjectId: The validated ObjectId.

    Raises:
        serializers.ValidationError: If the value is not a valid ObjectId.
    """
    try:
        return ObjectId(value)
    except Exception as error:
        raise serializers.ValidationError({'error': error})
