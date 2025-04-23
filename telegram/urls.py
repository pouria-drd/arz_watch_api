from django.urls import path
from telegram.views import TelegramUserCreateView, TelegramUserInfoView

urlpatterns = [
    path("create-user/", TelegramUserCreateView.as_view(), name="telegram-user-create"),
    path("user-info/", TelegramUserInfoView.as_view(), name="telegram-user-info"),
]
