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
        password = validated_data.pop('password', None)  # Достаем пароль из входных данных
        instance = User.objects.create(**validated_data)  # Создаем новый экземпляр пользователя
        if password is not None:
            instance.set_password(password)  # Устанавливаем хэшированный пароль
            instance.save()
            return instance
        