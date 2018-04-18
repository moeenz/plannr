from rest_framework import serializers

from django.contrib.auth import get_user_model

User = get_user_model()


class UserCreationSerializer(serializers.ModelSerializer):
    """Serialzier for auth user model used in user registration process.
    """

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
