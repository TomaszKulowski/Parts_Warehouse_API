"""
This module contains a unit test for Category model.
"""
import pytest

from categories.models import Category


@pytest.mark.django_db
def test_category_creation():
    """
    Test case for creating categories in the database.
    """
    category_a = Category.objects.create(name='Category_A')
    category_b = Category.objects.create(name='Category_B', parent_id=category_a)
    categories = Category.objects.all()

    assert categories[0] == category_a
    assert categories[1] == category_b
    assert len(categories) == 2
