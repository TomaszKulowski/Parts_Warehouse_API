"""
This module defines a Django model 'Part' representing parts.
"""
from djongo import models as djongo_models
from django.core.exceptions import ValidationError
from django.db import models

from categories.models import Category


class Part(models.Model):
    """
    The 'Part' model represents a part in the system.

    Fields:
    - _id (ObjectId): The primary key of the part.
    - serial_number (CharField): The unique serial number assigned to the part.
    - name (CharField): The name of the part.
    - description (TextField): A detailed description of the part.
    - category_id (ForeignKey): The foreign key reference to the associated category.
    - quantity (PositiveIntegerField): The quantity of the part available.
    - price (FloatField): The price of the part.
    - location (JSONField): A JSON field representing the location details of the part.

    Location Fields (Allowed Fields):
    - room (str): The room where the part is located.
    - bookcase (str): The bookcase where the part is stored.
    - shelf (str): The shelf on which the part is placed.
    - cuvette (str): The cuvette in which the part is kept.
    - column (str): The column where the part is positioned.
    - row (str): The row where the part is placed.

    Meta:
        db_table (str): The database table name for the 'Part' model.
    """
    _id = djongo_models.ObjectIdField(primary_key=True)
    serial_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category_id = models.ForeignKey(Category, on_delete=models.PROTECT, db_column='category_id')
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    location = djongo_models.JSONField()

    class Meta:
        db_table = 'parts'

    def save(self, *args, **kwargs):
        allowed_fields = ['room', 'bookcase', 'shelf', 'cuvette', 'column', 'row', ]

        for key in self.location.keys():
            if key not in allowed_fields:
                raise ValidationError(f'Invalid field: {key}')

        super().save(*args, **kwargs)
