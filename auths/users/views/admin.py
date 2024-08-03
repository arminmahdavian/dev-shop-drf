from rest_framework.authtoken.views import ObtainAuthToken

from auths.users.serializers.admin import AdminLoginSerializer


class AdminLoginView(ObtainAuthToken):
    serializer_class = AdminLoginSerializer