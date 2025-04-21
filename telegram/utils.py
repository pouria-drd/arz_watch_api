from telegram.models import TelegramUser


def register_or_update_user(telegram_user):
    tg_user, created = TelegramUser.objects.get_or_create(
        user_id=telegram_user.id,
        defaults={
            "username": telegram_user.username,
            "first_name": telegram_user.first_name,
            "last_name": telegram_user.last_name,
            "is_bot": telegram_user.is_bot,
            "language_code": getattr(telegram_user, "language_code", None),
            "is_premium": getattr(telegram_user, "is_premium", False),
        },
    )
    if not created:
        tg_user.update_last_seen()
    return tg_user
