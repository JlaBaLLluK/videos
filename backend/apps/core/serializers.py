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
    confirmation_code = serializers.CharField(read_only=True)
    _confirmation_code = None

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "password_confirm",
            "confirmation_code",
        )

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        password = attrs.get("password")
        password_confirm = attrs.pop("password_confirm")
        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Пароли не совпадают."}
            )

        attrs["confirmation_code"] = str(random.randint(100_000, 999_999))
        return super().validate(attrs)

    def send_email(self, code):
        send_mail(
            subject="Подтверждение регистрации",
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=f"Код для подтверждения регистрации - {code}",
            recipient_list=[
                self.instance.email,
            ],
            fail_silently=False,
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        code = validated_data.pop("confirmation_code")
        user = User(**validated_data)
        self._confirmation_code = code
        user.is_active = False
        user.set_password(password)
        user.save()
        self.instance = user
        self.send_email(code)
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["confirmation_code"] = self._confirmation_code
        return data


class UserRegistrationConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()

    def save(self, **kwargs):
        user = User.objects.get(username=self.validated_data["username"])
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


class UserDeleteSerializer(serializers.Serializer):
    password = serializers_fields.PasswordField()

    def validate_password(self, value):
        if not self.context["request"].user.check_password(value):
            raise serializers.ValidationError("Неверный пароль.")

        return value
