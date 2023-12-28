from rest_framework import serializers

from users_app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        """
        Метод создания нового пользователя.
        """
        # Достаем пароль из входных данных
        password = validated_data.pop('password', None)
        # Создаем новый экземпляр пользователя
        instance = User.objects.create(**validated_data)
        # Устанавливаем хэшированный пароль
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance
