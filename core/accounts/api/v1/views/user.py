import jwt
from rest_framework.generics import GenericAPIView
from ..serializers.user import (CustomUserSerializer, CustomAuthTokenSerializer, CustomTokenObtainPairSerializer, ActivationResendSerializer,
                                ForgetPasswordSerializer, ConfirmFrogetPasswordSerializer)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import CostumeUser
from rest_framework_simplejwt.tokens import RefreshToken
# from ..utils import send_threading_email
from ..tasks import send_email_task
from django.conf import settings
from django.shortcuts import get_object_or_404


class RegistrationAPIView(GenericAPIView):
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = CostumeUser.objects.create_user(email=serializer.validated_data['email'],
                                               password=serializer.validated_data['password'])
        token = self.get_token_for_user(user)
        # send_threading_email('email/activation.tpl', {'token': token}, user.email)
        send_email_task.delay('email/activation.tpl', {'token': token}, user.email)
        return Response('email send')

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ActivationAPIView(APIView):
    def get(self, request, token):
        try:
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = decoded_token.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({'detail': 'token is not vallid'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'detail': 'token is not vallid'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CostumeUser, pk=user_id)
        if user.is_verify:
            return Response('your account has already been verified and activated')
        user.is_verify = True
        user.save()
        return Response('your account activated and verified successfully')


class ActivationResendAPIView(GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = self.get_token_for_user(user)
        # send_threading_email('email/activation.tpl', {'token': token}, user.email)
        send_email_task.delay('email/activation.tpl', {'token': token}, user.email)
        return Response('email resend')

    def get_token_for_user(self, user):
            refresh = RefreshToken.for_user(user)
            return str(refresh.access_token)


class ForgetPasswordAPIView(GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = self.get_token_for_user(user)
        # send_threading_email('email/forget_password.tpl', {'token': token}, user.email)
        send_email_task.delay('email/forget_password.tpl', {'token': token}, user.email)
        return Response('email send')

    def get_token_for_user(self, user):
            refresh = RefreshToken.for_user(user)
            return str(refresh.access_token)


class ConfirmForgetPasswordAPIView(GenericAPIView):
    serializer_class = ConfirmFrogetPasswordSerializer

    def post(self, request, token):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = token.get('user_id')
        except jwt.ExpiredSignatureError:
            return Response({'detail': 'token has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidSignatureError:
            return Response({'detail': 'token is not vallid'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.DecodeError:
            return Response({'detail': 'token is not vallid'}, status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(CostumeUser, pk=user_id)
        if not user.is_verify:
            user.is_verify = True
        user.set_password(serializer.validated_data['pass1'])
        user.save()
        return Response('password changed successfully')




# TOKEN
class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email
        })


class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
