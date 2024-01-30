"""
This module defines a Django model 'Category' representing categories.
"""
from djongo import models as djongo_models
from django.db import models


class Category(models.Model):
    """
    The 'Category' model represents a category in the system.

    Fields:
    - _id (ObjectId): The primary key of the category.
    - name (CharField): The name of the category.
    - parent_id (ForeignKey): The foreign key reference to the parent category, allowing for hierarchical structure.

    Meta:
        db_table (str): The database table name for the 'Category' model.
    """
    _id = djongo_models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=25)
    parent_id = models.ForeignKey('self', on_delete=models.PROTECT,
                                  null=True, blank=True, db_column='parent_id')

    class Meta:
        db_table = 'categories'
