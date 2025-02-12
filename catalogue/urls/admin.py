from rest_framework.routers import SimpleRouter
from catalogue.views.admin import CategoryViewSet


router = SimpleRouter()
router.register('categories', CategoryViewSet, basename='Category')

urlpatterns = [] + router.urls