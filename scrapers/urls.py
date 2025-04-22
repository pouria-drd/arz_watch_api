from django.urls import path
from .views import TGJUCoinView, TGJUGoldView, TGJUCurrencyView

urlpatterns = [
    path("tgju/coin/", TGJUCoinView.as_view(), name="tgju-coin"),
    path("tgju/gold/", TGJUGoldView.as_view(), name="tgju-gold"),
    path("tgju/currency/", TGJUCurrencyView.as_view(), name="tgju-currency"),
]
