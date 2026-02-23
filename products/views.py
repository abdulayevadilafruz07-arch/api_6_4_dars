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
