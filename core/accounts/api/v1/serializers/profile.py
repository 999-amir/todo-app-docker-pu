from accounts.models import ProfileModel
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ["user", "f_name", "l_name", "description"]
        read_only_fields = ["user"]
