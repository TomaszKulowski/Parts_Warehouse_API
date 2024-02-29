"""
URL patterns for the 'parts' app.

These patterns define the endpoints for handling part-related operations.

- '' (empty path):
    - GET: List all parts.
    - POST: Add a new part.
- 'search/':
    - GET: Search for parts based on specified criteria.
- '<str:object_id>/':
    - GET: Retrieve a specific part by its object_id.
    - PUT: Update a specific part by its object_id.
    - DELETE: Delete a specific part by its object_id.
"""
from django.urls import path

from .views import PartsList, PartDetails, PartSearch


app_name = 'parts'

urlpatterns = [
    path('', PartsList.as_view(), name='parts_list'),
    path('search/', PartSearch.as_view(), name='parts_search'),
    path('<str:object_id>/', PartDetails.as_view(), name='part_details'),
]
