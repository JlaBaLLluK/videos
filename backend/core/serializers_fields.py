from rest_framework import serializers


class PasswordField(serializers.CharField):
    def __init__(self):
        super().__init__(max_length=128, required=True, write_only=True)


class UserReadOnlyField(serializers.PrimaryKeyRelatedField):
    def __init__(self):
        super().__init__(read_only=True)
