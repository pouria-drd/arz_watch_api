import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.throttling import ScopedRateThrottle

from api_keys.authentication import APIKeyAuthentication
from scrapers.serializers import TGJUDataSerializer
from scrapers.tgju import TGJUCoinScraper, TGJUCurrencyScraper, TGJUGoldScraper

# Loads the variables from the .env file into the environment
load_dotenv()

coin_scraper = TGJUCoinScraper()
gold_scraper = TGJUGoldScraper()
currency_scraper = TGJUCurrencyScraper()

# Cache response for 5 minutes by default
response_cache_time = 60 * int(os.getenv("RESPONSE_CACHE_TIME", "5"))


class TGJUGoldView(RetrieveAPIView):
    """Retrieve TGJU gold data as a read-only endpoint."""

    http_method_names = ["get"]
    serializer_class = TGJUDataSerializer
    # authentication_classes = [APIKeyAuthentication]  # You can set your custom one here

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    @method_decorator(cache_page(response_cache_time))
    def get(self, request: Request, *args, **kwargs):
        """Retrieve TGJU gold data as a read-only endpoint."""
        try:
            gold_data = gold_scraper.fetch_data()

            if not gold_data:
                return Response(
                    {"message": "No gold data found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.get_serializer(gold_data, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "retrievedAt": datetime.now(timezone.utc).isoformat(),
                    "message": "TGJU gold data retrieved successfully.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Error retrieving TGJU gold data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TGJUCoinView(RetrieveAPIView):
    """Retrieve TGJU coin data as a read-only endpoint."""

    http_method_names = ["get"]
    serializer_class = TGJUDataSerializer
    authentication_classes = [APIKeyAuthentication]  # You can set your custom one here

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    @method_decorator(cache_page(response_cache_time))
    def get(self, request: Request, *args, **kwargs):
        """Retrieve TGJU coin data as a read-only endpoint."""
        try:
            coin_data = coin_scraper.fetch_data()

            if not coin_data:
                return Response(
                    {"message": "No coin data found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.get_serializer(coin_data, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "retrievedAt": datetime.now(timezone.utc).isoformat(),
                    "message": "TGJU coin data retrieved successfully.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Error retrieving TGJU coin data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TGJUCurrencyView(RetrieveAPIView):
    """Retrieve TGJU currency data as a read-only endpoint."""

    http_method_names = ["get"]
    serializer_class = TGJUDataSerializer
    authentication_classes = [APIKeyAuthentication]  # You can set your custom one here

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    @method_decorator(cache_page(response_cache_time))
    def get(self, request: Request, *args, **kwargs):
        """Retrieve TGJU currency data as a read-only endpoint."""
        try:
            currency_data = currency_scraper.fetch_data()

            if not currency_data:
                return Response(
                    {"message": "No currency data found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = self.get_serializer(currency_data, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "retrievedAt": datetime.now(timezone.utc).isoformat(),
                    "message": "TGJU currency data retrieved successfully.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Error retrieving TGJU currency data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
