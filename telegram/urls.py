from django.urls import path
from telegram.views import TelegramUserCreateView

urlpatterns = [
    path("create/", TelegramUserCreateView.as_view(), name="telegram-user-create"),
]
