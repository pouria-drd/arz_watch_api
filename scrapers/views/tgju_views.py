import os
import json
from django.conf import settings

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.throttling import ScopedRateThrottle

from scrapers.serializers import TGJUDataSerializer
from api_keys.authentication import APIKeyAuthentication


class TGJUGoldView(RetrieveAPIView):
    """Retrieve TGJU gold data as a read-only endpoint."""

    http_method_names = ["get"]
    serializer_class = TGJUDataSerializer
    authentication_classes = [APIKeyAuthentication]  # You can set your custom one here

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def get(self, request: Request, *args, **kwargs):
        """Retrieve TGJU gold data as a read-only endpoint."""
        try:
            # Read the JSON file
            json_file_path = os.path.join(
                settings.BASE_DIR, "scrapers/output/scrapers/tgju_gold_data.json"
            )

            if not os.path.exists(json_file_path):
                return Response(
                    {"message": "Gold data file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            gold_data = []

            with open(json_file_path, "r", encoding="utf-8") as file:
                gold_data = json.load(file)

            serializer = self.get_serializer(gold_data, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "retrievedAt": gold_data[0].get("last_update"),
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

    def get(self, request: Request, *args, **kwargs):
        """Retrieve TGJU coin data as a read-only endpoint."""
        try:
            json_file_path = os.path.join(
                settings.BASE_DIR, "scrapers/output/scrapers/tgju_coin_data.json"
            )

            if not os.path.exists(json_file_path):
                return Response(
                    {"message": "Coin data file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            coin_data = []

            with open(json_file_path, "r", encoding="utf-8") as file:
                coin_data = json.load(file)

            serializer = self.get_serializer(coin_data, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "retrievedAt": coin_data[0].get("last_update"),
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

    def get(self, request: Request, *args, **kwargs):
        """Retrieve TGJU currency data as a read-only endpoint."""
        try:
            json_file_path = os.path.join(
                settings.BASE_DIR, "scrapers/output/scrapers/tgju_currency_data.json"
            )

            if not os.path.exists(json_file_path):
                return Response(
                    {"message": "Currency data file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            currency_data = []

            with open(json_file_path, "r", encoding="utf-8") as file:
                currency_data = json.load(file)

            serializer = self.get_serializer(currency_data, many=True)

            return Response(
                {
                    "data": serializer.data,
                    "retrievedAt": currency_data[0].get("last_update"),
                    "message": "TGJU currency data retrieved successfully.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Error retrieving TGJU currency data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
