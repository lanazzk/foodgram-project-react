from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from rest_framework import serializers

from recipe.models import Follow

User = get_user_model()


class CurrentUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return (Follow.objects.filter(user=user,
                                      following=obj).exists())


class UserPostSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]',
            message='Invalid character in username.')
        ])
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'password')
