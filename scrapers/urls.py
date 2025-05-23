from django.urls import path
from scrapers.views.arz_digital_views import ArzdigitalCryptoView
from scrapers.views.tgju_views import TGJUCoinView, TGJUGoldView, TGJUCurrencyView

urlpatterns = [
    path("tgju/coin/", TGJUCoinView.as_view(), name="tgju-coin"),
    path("tgju/gold/", TGJUGoldView.as_view(), name="tgju-gold"),
    path("tgju/currency/", TGJUCurrencyView.as_view(), name="tgju-currency"),
    path(
        "arzdigital/crypto/", ArzdigitalCryptoView.as_view(), name="arzdigital-crypto"
    ),
]
