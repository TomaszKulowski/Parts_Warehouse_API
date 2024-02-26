"""
This module contains unit tests for testing the URL patterns related to category management.
"""
from django.urls import resolve, reverse

from categories.views import CategoriesList, CategoryDetails


def test_list():
    """
    Test case for resolving and reversing URLs related to category listing.
    """
    found = resolve(reverse('categories:categories_list'))

    assert found.func.view_class == CategoriesList
    assert reverse('categories:categories_list') == '/categories/'
    assert resolve('/categories/').view_name == 'categories:categories_list'


def test_details():
    """
    Test case for resolving and reversing URLs related to category details.
    """
    found = resolve(reverse('categories:category_details', kwargs={'object_id': '1'}))

    assert found.func.view_class == CategoryDetails
    assert reverse('categories:category_details',  kwargs={'object_id': 'a1'}) == '/categories/a1/'
    assert resolve('/categories/1/').view_name == 'categories:category_details'
