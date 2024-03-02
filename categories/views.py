from django.db.models.deletion import ProtectedError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer
from Parts_Warehouse_API.validators import valid_object_id


class CategoriesList(APIView):
    """
    API view for listing and creating categories.

    GET:
    List all categories.

    POST:
    Create a new category.

    If the request includes 'parent_id', it associates the new category with the specified parent category.
    The 'parent_id' is used to determine the parent category, and it should be a valid ObjectId.
    If the 'parent_id' is not provided or invalid, the new category will be created as a top-level category.
    """
    def get(self, request: HttpRequest) -> Response:
        """
        Retrieve a list of all categories.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: Response with the serialized category data.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        """
        Create a new category.

        If 'parent_id' is provided, associate the new category with the specified parent category.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: Response with the serialized category data or error messages.
        """
        parent_id = request.data.get('parent_id')
        data = request.data.copy()
        if parent_id:
            parent_category = get_object_or_404(Category, pk=valid_object_id(parent_id))
            data['parent_id'] = parent_category._id

        serializer = CategorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetails(APIView):
    """
    API view for retrieving, updating, and deleting a specific category.

    GET:
    Retrieve details of a specific category.

    PUT:
    Update details of a specific category.

    DELETE:
    Delete a specific category.

    If the request includes 'parent_id' in the PUT method, it associates the updated category with the specified parent category.
    The 'parent_id' is used to determine the parent category, and it should be a valid ObjectId.

    If the DELETE operation fails due to references by other objects, a 400 Bad Request response is returned
    with an error message indicating that the category cannot be deleted because it is referenced by other objects.
    """
    def get(self, request: HttpRequest, object_id: str) -> Response:
        """
        Retrieve details of a specific category.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The ID of the category.

        Returns:
            Response: Response with the serialized category data.
        """
        category = get_object_or_404(Category, pk=valid_object_id(object_id))
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request: HttpRequest, object_id: str) -> Response:
        """
        Update details of a specific category.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The ID of the category.

        Returns:
            Response: Response with the serialized updated category data.
        """
        parent_id = request.data.get('parent_id')
        data = request.data.copy()
        category = get_object_or_404(Category, pk=valid_object_id(object_id))

        if parent_id:
            parent_category = get_object_or_404(Category, pk=valid_object_id(parent_id))
            data['parent_id'] = parent_category._id
        else:
            parts = category.part_set.all()
            if parts:
                return Response(
                    {'error': 'Cannot change category with assigned products to a base category.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = CategorySerializer(category, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, object_id: str) -> Response:
        """
        Delete a specific category.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The ID of the category.

        Returns:
            Response: Response with the status of the delete operation.
        """
        category = get_object_or_404(Category, pk=valid_object_id(object_id))
        try:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProtectedError:
            return Response(
                {'error': 'This category cannot be deleted because it is referenced by other objects.'},
                status=status.HTTP_400_BAD_REQUEST
            )
