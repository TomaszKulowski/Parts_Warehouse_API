from bson import ObjectId

from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Part
from .serializers import PartSerializer
from categories.models import Category
from Parts_Warehouse_API.validators import valid_object_id


class PartsList(APIView):
    """
    API view for listing all parts or creating a new part.

    GET:
    List all parts.

    POST:
    Create a new part.

    Additionally, any extra fields in the request data that are not part of the 'Part' model
    will be treated as part of the 'location' field in the new part.
    """
    def get(self, request: HttpRequest) -> Response:
        """
        Retrieve a list of all parts.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: Response with the serialized data of all parts.
        """
        parts = Part.objects.all()
        serializer = PartSerializer(parts, many=True)
        return Response(serializer.data)

    def post(self, request: HttpRequest) -> Response:
        """
        Create a new part.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: Response with the serialized data of the created part,
            or error response if the creation fails.
        """
        category_id = request.data.get('category_id')
        data = request.data.copy()

        location = {}
        for key, value in request.data.items():
            if key not in [field.name for field in Part._meta.get_fields()]:
                location[key] = value
                del data[key]
        if location:
            data['location'] = location

        if category_id:
            category = get_object_or_404(Category, pk=valid_object_id(category_id))
            data['category_id'] = category._id

        serializer = PartSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PartDetails(APIView):
    """
    API view for retrieving, updating, or deleting a specific part instance.

    GET:
    Retrieve details of a specific part by its object_id.

    PUT:
    Update details of a specific part by its object_id.

    DELETE:
    Delete a specific part by its object_id.
    """
    def get(self, request: HttpRequest, object_id: str) -> Response:
        """
        Retrieve details of a specific part.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The ID of the part.

        Returns:
            Response: Response with the serialized part data.
        """
        part = get_object_or_404(Part, pk=valid_object_id(object_id))
        serializer = PartSerializer(part)
        return Response(serializer.data)

    def put(self, request: HttpRequest, object_id: str) -> Response:
        """
         Update details of a specific part.

         Args:
             request (HttpRequest): The HTTP request object.
             object_id (str): The ID of the part.

         Returns:
             Response: Response with the serialized updated part data.
         """
        part = get_object_or_404(Part, pk=valid_object_id(object_id))
        category_id = request.data.get('category_id')
        data = request.data.copy()

        location = part.location
        for key, value in request.data.items():
            if key not in [field.name for field in Part._meta.get_fields()]:
                location[key] = value
                del data[key]
        if location:
            data['location'] = location

        if category_id:
            category = get_object_or_404(Category, pk=valid_object_id(category_id))
            data['category_id'] = category._id

        serializer = PartSerializer(part, data=data, partial=True)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data)
            except ValidationError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: HttpRequest, object_id: str) -> Response:
        """
        Delete a specific part.

        Args:
            request (HttpRequest): The HTTP request object.
            object_id (str): The ID of the part.

        Returns:
            Response: Response with the status of the delete operation.
        """
        category = get_object_or_404(Part, pk=valid_object_id(object_id))
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PartSearch(APIView):
    """
    API view for searching parts based on specified filters.

    GET:
    Retrieve a list of parts based on query parameters provided in the request.
    Supports filtering by various fields, including 'location' fields.

    The response includes the serialized data of matching parts.
    """

    def get_queryset(self):
        """
        Get the queryset based on request filters.

        Returns:
            QuerySet: The filtered queryset of parts.
        """
        queryset = Part.objects.all()
        queryset_filters = self.request.GET.copy()
        if 'category_id' in queryset_filters:
            queryset_filters['category_id'] = ObjectId(queryset_filters['category_id'])

        fields_name = [field.name for field in Part._meta.get_fields()]
        for key, value in queryset_filters.items():
            if key not in fields_name:
                queryset = queryset.filter(location__exact={key: value})
            else:
                queryset = queryset.filter(**{key: value})
        return queryset

    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        """
        Retrieve a list of parts based on specified filters.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable-length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse: Response with the serialized data of matching parts.
        """
        queryset = self.get_queryset().distinct()
        serializer = PartSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
