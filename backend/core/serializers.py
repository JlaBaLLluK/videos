from typing import Dict, Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework_simplejwt import serializers as jwt_serializer

from core import models as core_models
from core import serializers_fields

User = get_user_model()


class TokenObtainPairSerializer(jwt_serializer.TokenObtainPairSerializer):
    username_or_email = serializers.CharField(write_only=True, required=True)
    default_error_messages = {"no_active_account": "Учетная запись не найдена."}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username")

    @staticmethod
    def validate_username_or_email(value):
        if "@" in value:
            try:
                user = User.objects.get(email=value)
            except ObjectDoesNotExist:
                pass
            else:
                value = user.get_username()
        else:
            value = value

        return value

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        username = self.validate_username_or_email(attrs["username_or_email"])
        attrs["username"] = username
        data = super().validate(attrs)
        return data


class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].validators.append(
            RegexValidator(
                regex=r"^[a-zA-Z][a-zA-Z0-9_]*$",
                message="Имя пользователя может содержать буквы латинского алфавита, цифры и символ нижнего подчеркивания.",
            )
        )

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        if not data.get("profile_photo"):
            data["profile_photo"] = ""

        return data


class UserCreateSerializer(BaseUserSerializer):
    password = serializers_fields.PasswordField()
    password_confirm = serializers_fields.PasswordField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("password", "password_confirm")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Пароли не совпадают."}
            )

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = core_models.User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("profile_photo", "description")


class UserDetailSerializer(UserUpdateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserUpdateSerializer.Meta):
        fields = UserUpdateSerializer.Meta.fields + (
            "created_at",
            "channel_name",
            "subscribers_count",
            "subscriptions_count",
            "is_subscribed",
        )

    def get_is_subscribed(self, instance):
        user = self.context["request"].user
        return user.is_authenticated and user in instance.subscribers.all()


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers_fields.PasswordField()
    new_password = serializers_fields.PasswordField()
    new_password_confirm = serializers_fields.PasswordField()

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Текущий пароль неверный.")

        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError("Пароли не совпадают.")

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
