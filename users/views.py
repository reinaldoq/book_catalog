from rest_framework import viewsets

from users.models import CustomUser
from users.permissions import IsAdminOrSelfDelete
from users.serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = "uuid"
    permission_classes = [IsAdminOrSelfDelete]
