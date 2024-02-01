"""
URL patterns for the 'categories' app.

These patterns define the endpoints for handling category-related operations.

- '' (empty path):
    - GET: List all categories.
    - POST: Add a new category.
- '<str:object_id>/':
    - GET: Retrieve a specific category by its object_id.
    - PUT: Update a specific category by its object_id.
    - DELETE: Delete a specific category by its object_id.
"""
from django.urls import path

from .views import CategoriesList, CategoryDetails


app_name = 'categories'

urlpatterns = [
    path('', CategoriesList.as_view(), name='categories_list'),
    path('<str:object_id>/', CategoryDetails.as_view(), name='category_details'),
]
