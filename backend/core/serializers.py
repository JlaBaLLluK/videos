from rest_framework import serializers

from core import models as core_models

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, required=True, write_only=True)

    class Meta:
        model = core_models.User
        fields = ("username", "email", "password", "first_name", "last_name")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = core_models.User(**validated_data)
        user.set_password(password)
        user.save()
        return user
