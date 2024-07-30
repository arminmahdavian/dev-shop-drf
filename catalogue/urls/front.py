from django.urls import path
from rest_framework.routers import SimpleRouter

from catalogue.views.front import CategoryViewSet

router = SimpleRouter()
router.register('categories', CategoryViewSet)

urlpatterns = [] + router.urls