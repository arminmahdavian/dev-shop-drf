from rest_framework import viewsets

from catalogue.models import Category
from catalogue.serializers.front import CategorySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.public()
    serializer_class = CategorySerializer



