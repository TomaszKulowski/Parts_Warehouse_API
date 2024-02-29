"""
This module contains unit test cases for testing the API views related to part management.
"""
import json

from bson import ObjectId

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APIRequestFactory, APITestCase

from .factories import PartFactory
from categories.tests.factories import SideCategoryFactory, MainCategoryFactory
from parts.models import Part
from parts.serializers import PartSerializer
from parts.views import PartsList, PartDetails, PartSearch


class TestPartsList(APITestCase):
    """
    Test case class for testing the PartsList API view.
    """
    def setUp(self):
        """
        Set up necessary components for each test.
        """
        self.factory = APIRequestFactory()
        self.view = PartsList.as_view()

    def test_get_parts(self):
        """
        Test retrieving a list of parts.
        """
        PartFactory.create_batch(10)
        parts = Part.objects.all()

        request = self.factory.get('/parts/')
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 10
        assert response.data == PartSerializer(parts, many=True).data

    def get_parts_no_results(self):
        """
        Test retrieving an empty list of parts.
        """
        request = self.factory.get('/parts/')
        response = self.view(request)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 0

    def test_successfully_create_part(self):
        """
        Test successfully creating a part.
        """
        category = SideCategoryFactory()
        payload = {
            'serial_number': '123123a',
            'name': 'part_A',
            'description': 'test descrption',
            'category_id': str(category._id),
            'quantity': 222,
            'price': 10.82,
            'location': {
                'room': '99',
                'bookcase': 'a19',
                'shelf': 'zy',
                'cuvette': '211',
                'column': 'c3z',
                'row': '211',
            }
        }

        request = self.factory.post('parts/', payload, format='json')
        response = self.view(request)

        assert response.status_code == status.HTTP_201_CREATED

    def test_unsuccessfully_create_part_with_main_category(self):
        """
        Test unsuccessfully creating a part with a main category.
        """
        category = MainCategoryFactory()
        payload = {
            'category_id': str(category._id),
            'serial_number': '123123a',
            'name': 'part_A',
            'description': 'test descrption',
            'quantity': 222,
            'price': 10.82,
            'room': '99',
            'bookcase': 'a19',
            'shelf': 'zy',
            'cuvette': '211',
            'column': 'c3z',
            'row': '211',
        }

        request = self.factory.post('/parts/', payload, format='json')
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_unsuccessfully_create_part_with_wrong_location(self):
        """
        Test unsuccessfully creating a part with a wrong location.
        """
        category = SideCategoryFactory()
        payload = {
            'category_id': str(category._id),
            'serial_number': '123123a',
            'name': 'part_A',
            'description': 'test descrption',
            'quantity': 222,
            'price': 10.82,
            'room': '99',
            'bookcase': 'a19',
            'shelf': 'zy',
            'cuvette': '211',
            'column': 'c3z',
            'wrong_location': '211',
        }

        request = self.factory.post('/parts/', payload, format='json')
        response = self.view(request)

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestPartDetails(APITestCase):
    """
    Test case class for testing the PartDetails API view.
    """
    def setUp(self):
        """
        Set up necessary components for each test.
        """
        self.factory = APIRequestFactory()
        self.view = PartDetails.as_view()
        self.category = SideCategoryFactory()
        self.part_attrs = {
            '_id': ObjectId('5fc6e6ba9f84e500c7f3b89c'),
            'serial_number': '123123a',
            'name': 'part_A',
            'description': 'test descrption',
            'category_id': self.category,
            'quantity': 222,
            'price': 10.82,
            'location': {
                'room': '99',
                'bookcase': 'a19',
                'shelf': 'zy',
                'cuvette': '211',
                'column': 'c3z',
                'row': '211',
            }
        }
        self.part = Part.objects.create(**self.part_attrs)

    def test_get_part_details(self):
        """
        Test retrieving details of a part.
        """
        request = self.factory.get(f'parts/{self.part._id}/')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('serial_number') == self.part.serial_number
        assert response.data.get('name') == self.part.name
        assert response.data.get('description') == self.part.description
        assert response.data.get('category_id') == str(self.part.category_id._id)
        assert response.data.get('quantity') == self.part.quantity
        assert response.data.get('price') == self.part.price
        assert response.data.get('location') == self.part.location

    def test_get_non_existent_part_details(self):
        """
        Test retrieving details of a non-existent part.
        """
        non_existent_part_id = '5fc6e6ba9f84e500c7f3b123'
        request = self.factory.get(f'parts/{non_existent_part_id}/')
        response = self.view(request, object_id=non_existent_part_id)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.data == {'detail': ErrorDetail(string='Not found.', code='not_found')}

    def test_update_serial_number(self):
        """
        Test updating the serial number of a part.
        """
        payload = {'serial_number': 'new_serial_number'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['serial_number'] == payload['serial_number']

    def test_update_name(self):
        """
        Test updating the name of a part.
        """
        payload = {'name': 'new_name'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == payload['name']

    def test_update_description(self):
        """
        Test updating the description of a part.
        """
        payload = {'description': 'new description'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['description'] == payload['description']

    def test_update_category_id_to_side_category(self):
        """
        Test updating the category_id of a part to side category.
        """
        new_category = SideCategoryFactory()
        payload = {'category_id': str(new_category._id)}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['category_id'] == payload['category_id']

    def test_update_category_id_to_main_category(self):
        """
        Test updating the category_id of a part to main category.
        """
        new_category = MainCategoryFactory()
        payload = {'category_id': str(new_category._id)}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"error": ["Cannot add data to a base category."]}

    def test_update_quantity(self):
        """
        Test updating the quantity of a part.
        """
        payload = {'quantity': 122}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['quantity'] == payload['quantity']

    def test_update_price(self):
        """
        Test updating the price of a part.
        """
        payload = {'price': 00.01}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['price'] == payload['price']

    def test_update_location_room(self):
        """
        Test updating the room location of a part.
        """
        payload = {'room': '1a'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['location']['room'] == payload['room']

    def test_update_location_bookcase(self):
        """
        Test updating the bookcase location of a part.
        """
        payload = {'bookcase': 'b1'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['location']['bookcase'] == payload['bookcase']

    def test_update_location_shelf(self):
        """
        Test updating the shelf location of a part.
        """
        payload = {'shelf': 'A'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['location']['shelf'] == payload['shelf']

    def test_update_location_cuvette(self):
        """
        Test updating the cuvette location of a part.
        """
        payload = {'cuvette': '1'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['location']['cuvette'] == payload['cuvette']

    def test_update_location_column(self):
        """
        Test updating the column location of a part.
        """
        payload = {'column': '9'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['location']['column'] == payload['column']

    def test_update_location_row(self):
        """
        Test updating the row location of a part.
        """
        payload = {'row': '1a'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['location']['row'] == payload['row']

    def test_update_non_existent_field(self):
        """
        Test attempting to update a non-existent field of a part.
        """
        payload = {'wrong_field': '1a'}

        request = self.factory.put(f'/parts/{self.part._id}', payload, format='json')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_part(self):
        """
        Test deleting a part.
        """
        request = self.factory.delete(f'/parts/{self.part._id}')
        response = self.view(request, object_id=self.part._id)

        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestPartSearch(APITestCase):
    """
    Test case class for testing the PartSearch API view.
    """
    def setUp(self):
        """
        Set up necessary components for each test.
        """
        self.factory = APIRequestFactory()
        self.view = PartSearch.as_view()
        self.category = SideCategoryFactory()
        self.part_attrs = {
            '_id': ObjectId('5fc6e6ba9f84e500c7f3b89c'),
            'serial_number': '123123a',
            'name': 'part_A',
            'description': 'test descrption',
            'category_id': self.category,
            'quantity': 222,
            'price': 10.82,
            'location': {
                'room': '99',
                'bookcase': 'a19',
                'shelf': 'zy',
                'cuvette': '211',
                'column': 'c3z',
                'row': '211',
            }
        }
        self.expected_result = {
            '_id': str('5fc6e6ba9f84e500c7f3b89c'),
            'serial_number': '123123a',
            'name': 'part_A',
            'description': 'test descrption',
            'category_id': str(self.category._id),
            'quantity': 222,
            'price': 10.82,
            'location': {
                'room': '99',
                'bookcase': 'a19',
                'shelf': 'zy',
                'cuvette': '211',
                'column': 'c3z',
                'row': '211',
            }
        }
        self.part = Part.objects.create(**self.part_attrs)

    def test_search_by_serial_number(self):
        """
        Test searching for a part by serial number.
        """
        payload = {'serial_number': self.part_attrs['serial_number']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_by_name(self):
        """
        Test searching for a part by name.
        """
        payload = {'name': self.part_attrs['name']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_by_description(self):
        """
        Test searching for a part by description.
        """
        payload = {'description': self.part_attrs['description']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_by_category_id(self):
        """
        Test searching for a part by category_id.
        """
        payload = {'category_id': str(self.category._id)}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_by_quantity(self):
        """
        Test searching for a part by quantity.
        """
        payload = {'quantity': self.part_attrs['quantity']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_by_price(self):
        """
        Test searching for a part by price.
        """
        payload = {'price': self.part_attrs['price']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_in_location_by_room(self):
        """
        Test searching for a part by room location.
        """
        payload = {'room': self.part_attrs['location']['room']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_in_location_by_bookcase(self):
        """
        Test searching for a part by bookcase location.
        """
        payload = {'bookcase': self.part_attrs['location']['bookcase']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_in_location_by_shelf(self):
        """
        Test searching for a part by shelf location.
        """
        payload = {'shelf': self.part_attrs['location']['shelf']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_in_location_by_cuvette(self):
        """
        Test searching for a part by cuvette location.
        """
        payload = {'cuvette': self.part_attrs['location']['cuvette']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_in_location_by_column(self):
        """
        Test searching for a part by column location.
        """
        payload = {'column': self.part_attrs['location']['column']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_in_location_by_row(self):
        """
        Test searching for a part by row location.
        """
        payload = {'row': self.part_attrs['location']['row']}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == [self.expected_result]

    def test_search_by_non_existent_name(self):
        """
        Test searching for a non-existent part by name.
        """
        payload = {'name': 'non_existent_part'}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == []

    def test_search_by_non_existent_field(self):
        """
        Test searching for a part using a non-existent field.
        """
        payload = {'non_existent_field': 'value'}

        request = self.factory.get('/parts/search/', payload, format='json')
        response = self.view(request)
        result = json.loads(response.content.decode('utf-8'))

        assert response.status_code == status.HTTP_200_OK
        assert result == []
