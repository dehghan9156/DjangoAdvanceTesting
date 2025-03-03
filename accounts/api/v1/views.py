from http.client import responses

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from django.template.defaulttags import querystring

from .serialization import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainSerializer,
    ChangePasswordSerializer,
    CustomProfileSerializer,
)
from ...models import User, Profile
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from mail_templated import send_mail
from ..utils import EmailSenderThread
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
import jwt
from jwt.exceptions import ExpiredSignatureError


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            send_mail(
                template_name="email/active_user.tpl",
                context={"token": token},
                from_email="admin@admin.com",
                recipient_list=[email],
            )
            # EmailSenderThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class TokenLoginApiView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class TokenLogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainSerializer


class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    model = User

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"detail": "password changed successfully"}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = CustomProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.queryset
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class SendEmailView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        self.email = "dehghan9156@gmail.com"
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)
        send_mail(
            template_name="email/hello.tpl",
            context={"token": token},
            from_email="admin@admin.com",
            recipient_list=[self.email],
        )
        # EmailSenderThread(email_obj).start()
        return Response("email send")

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ConfirmUserView(APIView):
    # decode token jwt -> get id user -> get objects -> is_verified True
    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return Response({"detail": "token ExpiredSignatureError"})
        user_id = token.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        if user.is_verified:
            return Response({"detail": "user already is_verified"})
        user.is_verified = True
        user.save()
        return Response(token)
