"""
This module contains unit tests for testing the URL patterns related to part management.
"""
from django.urls import resolve, reverse

from parts.views import PartsList, PartSearch, PartDetails


def test_list():
    """
    Test resolving URLs for the parts list view.
    """
    found = resolve(reverse('parts:parts_list'))

    assert found.func.view_class == PartsList
    assert reverse('parts:parts_list') == '/parts/'
    assert resolve('/parts/').view_name == 'parts:parts_list'


def test_search():
    """
    Test resolving URLs for the part search view.
    """
    found = resolve(reverse('parts:parts_search'))

    assert found.func.view_class == PartSearch
    assert reverse('parts:parts_search') == '/parts/search/'
    assert resolve('/parts/search/').view_name == 'parts:parts_search'


def test_details():
    """
    Test resolving URLs for the part details view.
    """
    found = resolve(reverse('parts:part_details', kwargs={'object_id': '1'}))

    assert found.func.view_class == PartDetails
    assert reverse('parts:part_details', kwargs={'object_id': '1'}) == '/parts/1/'
    assert resolve('/parts/1/').view_name == 'parts:part_details'
