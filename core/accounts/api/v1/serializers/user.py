from accounts.models import CostumeUser
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import get_object_or_404


class CustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=250, write_only=True)

    class Meta:
        model = CostumeUser
        fields = ['email', 'password', 'confirm_password', 'is_active', 'is_admin']
        read_only_fields = ['is_active', 'is_admin']

    # hide password in get http method
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.pop('password', None)
        return rep

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'detail': "passwords doesn't match"})
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        return CostumeUser.objects.create_user(**validated_data)


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = get_object_or_404(CostumeUser, email=email)
        except CostumeUser.DoesNotExist:
            raise serializers.ValidationError('user does not exist')
        if user.is_verify:
            raise serializers.ValidationError('user is already verified and activated')
        attrs['user'] = user
        return super().validate(attrs)


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = get_object_or_404(CostumeUser, email=email)
        except CostumeUser.DoesNotExist:
            raise serializers.ValidationError('user does not exist')
        attrs['user'] = user
        return super().validate(attrs)


class ConfirmFrogetPasswordSerializer(serializers.Serializer):
    pass1 = serializers.CharField(required=True)
    pass2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get('pass1') != attrs.get('pass2'):
            raise serializers.ValidationError({'detail': 'passwords doesnt match'})
        try:
            validate_password(attrs.get('pass1'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)



# TOKEN
class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verify:
                raise serializers.ValidationError({'detail': 'account still not verified'})
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


# JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verify:
            raise serializers.ValidationError({'detail': 'account still not verified'})
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data
