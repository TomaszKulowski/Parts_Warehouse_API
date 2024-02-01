"""
URL patterns for the Django Parts_Warehouse_API project.

These patterns include the following endpoints:

- 'categories/':
    - Include the URL patterns for the 'categories' app.

- 'parts/':
    - Include the URL patterns for the 'parts' app.
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('categories/', include('categories.urls')),
    path('parts/', include('parts.urls')),
]
