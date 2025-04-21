from django.urls import path
from .views import TGJUCoinView, TGJUGoldView, TGJUCurrencyView

urlpatterns = [
    path("tgju/coin/", TGJUCoinView.as_view(), name="tgju_coin"),
    path("tgju/gold/", TGJUGoldView.as_view(), name="tgju_gold"),
    path("tgju/currency/", TGJUCurrencyView.as_view(), name="tgju_currency"),
]
