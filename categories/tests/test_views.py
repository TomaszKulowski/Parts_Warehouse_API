"""
This module contains unit test cases for testing the API views related to category management.
"""
import pytest

from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from .factories import SideCategoryFactory, MainCategoryFactory
from categories.models import Category
from categories.serializers import CategorySerializer
from categories.views import CategoriesList, CategoryDetails


class TestCategoriesList(APITestCase):
    """
    Test case class for testing the CategoriesList API view.
    """
    def setUp(self):
        """
        Set up necessary components for each test.
        """
        self.factory = APIRequestFactory()
        self.view = CategoriesList.as_view()

    def test_get_categories(self):
        """
        Test retrieving a list of categories.
        """
        SideCategoryFactory.create_batch(3)
        categories = Category.objects.all()

        request = self.factory.get('/categories/')
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 6
        assert response.data == CategorySerializer(categories, many=True).data

    def test_get_categories_no_results(self):
        """
        Test retrieving an empty list of categories.
        """
        request = self.factory.get('/categories/')
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_successfully_create_category_without_parent(self):
        """
        Test creating a category without a parent.
        """
        payload = {'name': 'Test Category'}
        request = self.factory.post('/categories/', payload, format='json')
        response = self.view(request)

        assert response.status_code == status.HTTP_201_CREATED

    def test_successfully_create_category_with_parent(self):
        """
        Test creating a category with a parent.
        """
        parent_category = Category.objects.create(name='Parent Category')

        payload = {'name': 'Test Category', 'parent_id': str(parent_category._id)}
        request = self.factory.post('/categories/', payload, format='json')
        response = self.view(request)

        assert response.status_code == status.HTTP_201_CREATED

    def test_unsuccessfully_create_category(self):
        """
        Test unsuccessfully creating a category due to invalid data.
        """
        payload = {'name': 'Test Category', 'parent_id': 'wrong_id'}
        request = self.factory.post('/categories/', payload, format='json')
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestCategoryDetails(APITestCase):
    """
    Test case class for testing the CategoryDetails API view.
    """
    def setUp(self):
        """
        Set up necessary components for each test.
        """
        self.factory = APIRequestFactory()
        self.view = CategoryDetails.as_view()
        self.category = MainCategoryFactory(name='Category_A')

    def test_get_category_details(self):
        """
        Test retrieving details of a category.
        """
        request = self.factory.get(f'categories/{self.category._id}/')
        response = self.view(request, object_id=self.category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.category._id)
        assert response.data.get('name') == self.category.name
        assert response.data.get('parent_id') == self.category.parent_id

    def test_update_name_category(self):
        """
        Test updating the name of a category.
        """
        payload = {'name': 'Category_B'}
        request = self.factory.put(f'categories/{self.category._id}/', payload, format='json')
        response = self.view(request, object_id=self.category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.category._id)
        assert response.data.get('name') == 'Category_B'
        assert response.data.get('parent_id') == self.category.parent_id

    def test_update_parent_id_category(self):
        """
        Test updating the parent ID of a category.
        """
        main_category = MainCategoryFactory(name='Category_B')
        payload = {'parent_id': str(main_category._id)}
        request = self.factory.put(f'categories/{self.category._id}/', payload, format='json')
        response = self.view(request, object_id=self.category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.category._id)
        assert response.data.get('name') == self.category.name
        assert response.data.get('parent_id') == str(main_category._id)

    def test_delete_category(self):
        """
        Test deleting a category.
        """
        request = self.factory.delete(f'categories/{self.category._id}/')
        response = self.view(request, object_id=self.category._id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(Category.DoesNotExist) as error:
            Category.objects.get(pk=self.category._id)

        assert error.type == Category.DoesNotExist
        assert str(error.value) == 'Category matching query does not exist.'
