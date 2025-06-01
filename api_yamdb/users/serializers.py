from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

ERROR_MESSAGE = "Username may contain only letters, digits and @.+-_"


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        error_messages={'invalid': ERROR_MESSAGE}
    )


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        error_messages={'invalid': ERROR_MESSAGE}
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)
