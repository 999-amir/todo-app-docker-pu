from ..serializers.profile import ProfileSerializer
from accounts.models import ProfileModel
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView


class ProfileAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return get_object_or_404(ProfileModel, user=self.request.user)
