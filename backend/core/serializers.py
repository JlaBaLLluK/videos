from rest_framework import serializers

from core import models as core_models


class PasswordField(serializers.CharField):
    def __init__(self):
        super().__init__(max_length=128, required=True, write_only=True)


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.User
        fields = ("username", "email", "first_name", "last_name")


class UserSerializer(BaseUserSerializer):
    password = PasswordField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("password",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = core_models.User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserDetailSerializer(BaseUserSerializer):
    pass


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = PasswordField()
    new_password = PasswordField()
    new_password_confirm = PasswordField()

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Current password is wrong")

        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("Passwords aren't the same")

        return attrs
