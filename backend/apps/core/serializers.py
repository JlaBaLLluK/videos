from typing import Dict, Any

import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from rest_framework import serializers
from rest_framework.settings import api_settings
from rest_framework_simplejwt import serializers as jwt_serializer

from . import serializers_fields
from . import mixins

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
        return super().validate(attrs)


class UserListSerializer(mixins.UserSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "channel_name",
            "username",
            "profile_photo",
            "description_preview",
            "is_request_user_subscribed",
        )


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers_fields.PasswordField()
    password_confirm = serializers_fields.PasswordField()

    class Meta:
        model = User
        fields = ("username", "email", "password", "password_confirm")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Пароли не совпадают."}
            )

        return super().validate(attrs)

    def send_email(self):
        confirmation_code = random.randint(100_000, 999_999)
        self.context["request"].session["confirmation_code"] = str(confirmation_code)
        self.context["request"].session["user"] = self.instance
        send_mail(
            subject="Подтверждение аккаунта",
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=f"Код для подтверждения регистрации - {confirmation_code}",
            recipient_list=[self.instance.email,],
            fail_silently=False
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.is_active = False
        user.set_password(password)
        user.save()
        self.instance = user
        self.send_email()
        return user


class UserRegistrationConfirmSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField()

    def validate_confirmation_code(self, value):
        if self.context["request"].session["confirmation_code"] != value:
            raise serializers.ValidationError("Неверный код.")

        return value

    def save(self, **kwargs):
        user = self.context["request"].session["user"]
        user.is_active = True
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "description",
            "profile_photo",
        )


class UserDetailSerializer(mixins.UserSerializerMixin, UserUpdateSerializer):
    created_at = serializers.DateTimeField(format=api_settings.DATE_FORMAT)

    class Meta(UserUpdateSerializer.Meta):
        fields = UserUpdateSerializer.Meta.fields + (
            "created_at",
            "channel_name",
            "subscribers_count",
            "subscriptions_count",
            "videos_count",
            "description_preview",
            "is_request_user_subscribed",
        )


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers_fields.PasswordField()
    new_password = serializers_fields.PasswordField()
    new_password_confirm = serializers_fields.PasswordField()

    def validate_current_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Текущий пароль неверный.")

        return value

    def validate(self, attrs):
        if attrs["new_password"] == attrs["current_password"]:
            raise serializers.ValidationError(
                {"new_password": "Новый пароль не может совпадать со старым."}
            )

        if attrs["new_password"] != attrs["new_password_confirm"]:
            raise serializers.ValidationError(
                {"new_password_confirm": "Пароли не совпадают."}
            )

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
