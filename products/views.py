from decimal import Decimal
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer


class ProductListCreateView(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        search = self.request.query_params.get('search', None)
        price = self.request.query_params.get('price')
        if search:
            product = Product.objects.filter(Q(title__icontains=search) & Q(price__gte=price))
            if product is None:
                data = {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Topilmadi',
                }

                return ValidationError(data)
            serializer = self.get_serializer(product, many=True)
            data = {
                'status': status.HTTP_200_OK,
                'message': 'Products',
                "data": serializer.data
            }

            return Response(data)
        product = self.get_queryset()
        serializer = self.get_serializer(product, many=True)
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Products',
            "data": serializer.data
        }

        return Response(data)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': status.HTTP_201_CREATED,
                'message': 'Product',
                "data": serializer.data
            }
            return Response(data)

        data = {
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Eror',
            "desc": serializer.errors
        }

        return Response(data)


class ProductUpdateDetailDestroyView(GenericAPIView):
    serializer_class = ProductSerializer

    def get_object(self, pk):
        product = Product.objects.filter(pk=pk).first()
        return product

    def put(self, request, pk):
        product = self.get_object(pk)
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Product update',
            "data": serializer.data
        }
        return Response(data)

    def patch(self, request, pk):
        product = self.get_object(pk)
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'status': status.HTTP_200_OK,
            'message': 'Product update',
            "data": serializer.data
        }

        return Response(data)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = self.get_serializer(user)
        data = {
            'status': status.HTTP_200_OK,
            'massage': 'user',
            'data': serializer.data
        }
        return Response(data)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user is None:
            data = {
                'status': status.HTTP_404_NOT_FOUND,
                'massage': 'User topilmadi',
            }
            raise ValidationError(data)
        user.delete()
        data = {
            'status': status.HTTP_204_NO_CONTENT,
            'massage': 'user ochirlidi',
        }
        return Response(data)
