from typing import Dict, Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializer

from core import models as core_models


User = get_user_model()


class PasswordField(serializers.CharField):
    def __init__(self):
        super().__init__(max_length=128, required=True, write_only=True)


class TokenObtainPairSerializer(jwt_serializer.TokenObtainPairSerializer):
    username_or_email = serializers.CharField(write_only=True, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username")

    def validate_username_or_email(self, value):
        if "@" in value:
            try:
                user = User.objects.get(email=value)
            except ObjectDoesNotExist:
                raise serializers.ValidationError("User with this email doesn't exist")

            value = user.get_username()
        else:
            value = value

        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        attrs["username"] = self.validate_username_or_email(attrs["username_or_email"])
        return super().validate(attrs)


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = core_models.User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "profile_photo",
        )


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
