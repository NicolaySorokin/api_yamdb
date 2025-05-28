import jwt
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SignupSerializer, TokenSerializer, UserSerializer
from .permissions import IsAdmin

User = get_user_model()


class SignupView(APIView):
    """POST /api/v1/auth/signup/"""
    permission_classes = []

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
        )
        # Generate confirmation code
        code = default_token_generator.make_token(user)
        user.confirmation_code = code
        user.save()

        send_mail(
            subject='Your YaMDb confirmation code',
            message=f'Hello {username}, your confirmation code is: {code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK,
        )


class TokenView(APIView):
    """POST /api/v1/auth/token/"""
    permission_classes = []

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        code = serializer.validated_data['confirmation_code']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'detail': 'User not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        if user.confirmation_code != code:
            return Response(
                {'confirmation_code': 'Invalid code.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Create JWT
        payload = {
            'username': user.username,
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return Response({'token': token}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']
