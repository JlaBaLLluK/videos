from django.utils import timezone


def get_text_preview(text, words_count):
    text_parts = text.split()
    text_preview_parts = text_parts[:words_count]
    if len(text_preview_parts) < len(text_parts):
        text_preview_parts[-1] += "..."

    return " ".join(text_preview_parts)


def get_number_representation(number):
    number_placeholder = ""
    if number >= 1_000_000:
        number_placeholder = "млн."
        number //= 1_000_000
    elif number >= 1_000:
        number_placeholder = "тыс."
        number //= 1_000

    return f"{number} {number_placeholder}"


def get_creation_date_representation(date):
    time_passed = timezone.now() - date
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
