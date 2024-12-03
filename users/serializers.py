from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """ Класс-сериализатор для модели User """

    class Meta:
        model = User
        fields = ('email', 'password')
