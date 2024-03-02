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
from parts.tests.factories import PartFactory


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
        # we create 6 objects because for each side category we create new main category
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
        self.main_category = MainCategoryFactory(name='MainCategory')
        self.side_category = SideCategoryFactory(name='SideCategory')

    def test_get_category_details(self):
        """
        Test retrieving details of a category.
        """
        request = self.factory.get(f'categories/{self.side_category._id}/')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.side_category._id)
        assert response.data.get('name') == self.side_category.name
        assert response.data.get('parent_id') == str(self.side_category.parent_id._id)

    def test_update_name_category(self):
        """
        Test updating the name of a category.
        """
        payload = {'name': 'Category_B'}
        request = self.factory.put(f'categories/{self.side_category._id}/', payload, format='json')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.side_category._id)
        assert response.data.get('name') == 'Category_B'
        assert response.data.get('parent_id') == str(self.side_category.parent_id._id)

    def test_update_main_category_to_side_category(self):
        """
        Test updating a main category to a side category.
        """
        new_main_category = MainCategoryFactory(name='new_main_category')
        payload = {'parent_id': str(new_main_category._id)}
        request = self.factory.put(f'categories/{self.main_category._id}/', payload, format='json')
        response = self.view(request, object_id=self.main_category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.main_category._id)
        assert response.data.get('name') == self.main_category.name
        assert response.data.get('parent_id') == str(new_main_category._id)

    def test_update_parent_id_category_without_parts_to_side_category(self):
        """
        Test updating a category without parts to a side category.
        """
        new_main_category = MainCategoryFactory(name='new_main_category')
        payload = {'parent_id': str(new_main_category._id)}
        request = self.factory.put(f'categories/{self.side_category._id}/', payload, format='json')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.side_category._id)
        assert response.data.get('name') == self.side_category.name
        assert response.data.get('parent_id') == str(new_main_category._id)

    def test_update_parent_id_category_with_parts_to_side_category(self):
        """
        Test updating a category with parts to a side category.
        """
        new_main_category = MainCategoryFactory(name='new_main_category')
        PartFactory(category_id=self.side_category)
        payload = {'parent_id': str(new_main_category._id)}
        request = self.factory.put(f'categories/{self.side_category._id}/', payload, format='json')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.side_category._id)
        assert response.data.get('name') == self.side_category.name
        assert response.data.get('parent_id') == str(new_main_category._id)

    def test_update_parent_id_category_without_parts_to_main(self):
        """
        Test updating a category without parts to a main category.
        """
        payload = {'parent_id': None}
        request = self.factory.put(f'categories/{self.side_category._id}/', payload, format='json')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('_id') == str(self.side_category._id)
        assert response.data.get('name') == self.side_category.name
        assert response.data.get('parent_id') is None

    def test_update_parent_id_category_with_parts_to_main(self):
        """
        Test updating a category with parts to a main category.
        """
        PartFactory(category_id=self.side_category)
        payload = {'parent_id': None}
        request = self.factory.put(f'categories/{self.side_category._id}/', payload, format='json')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['error'] == 'Cannot change category with assigned products to a base category.'

    def test_delete_main_category_without_side_category(self):
        """
        Test deleting a main category without side categories.
        """
        request = self.factory.delete(f'categories/{self.main_category._id}/')
        response = self.view(request, object_id=self.main_category._id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(Category.DoesNotExist) as error:
            Category.objects.get(pk=self.main_category._id)

        assert error.type == Category.DoesNotExist
        assert str(error.value) == 'Category matching query does not exist.'

    def test_delete_main_category_with_side_category(self):
        """
        Test deleting a main category with associated side categories.
        """
        parent_category = self.side_category.parent_id
        request = self.factory.delete(f'categories/{parent_category._id}/')
        response = self.view(request, object_id=parent_category._id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        category = Category.objects.get(pk=parent_category._id)

        assert category == parent_category

    def test_delete_side_category_without_side_category(self):
        """
        Test deleting a side category without child categories.
        """
        request = self.factory.delete(f'categories/{self.side_category._id}/')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_204_NO_CONTENT

        with pytest.raises(Category.DoesNotExist) as error:
            Category.objects.get(pk=self.side_category._id)

        assert error.type == Category.DoesNotExist
        assert str(error.value) == 'Category matching query does not exist.'

    def test_delete_side_category_with_side_category(self):
        """
        Test deleting a side category with child categories.
        """
        new_side_category = SideCategoryFactory(parent_id=self.side_category)
        request = self.factory.delete(f'categories/{self.side_category._id}/')
        response = self.view(request, object_id=self.side_category._id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        category = Category.objects.get(pk=new_side_category._id)

        assert category == new_side_category
