from django.utils import timezone

from rest_framework import serializers


class VideoSerializerMixin(metaclass=serializers.SerializerMetaclass):
    published_ago = serializers.SerializerMethodField()

    @staticmethod
    def get_published_ago(obj):
        time_passed = timezone.now() - obj.created_at
        days = time_passed.days
        seconds = time_passed.seconds
        if days >= 365:
            return f"{days // 365} г. назад"

        if days >= 30:
            return f"{days // 30} мес. назад"

        if days >= 1:
            return f"{days} д. назад"

        if seconds >= 3600:
            return f"{seconds // 3600} ч. назад"

        return f"{seconds // 60} мин. назад"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        views_placeholder = ""
        if data["views_count"] >= 1_000_000:
            views_placeholder = "млн."
            data["views_count"] //= 1_000_000
        elif data["views_count"] >= 1_000:
            views_placeholder = "тыс."
            data["views_count"] //= 1_000

        data["views_count"] = f'{data["views_count"]} {views_placeholder}'
        return data
