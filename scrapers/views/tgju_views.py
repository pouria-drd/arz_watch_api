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
from telegram.models import TelegramCommand, TelegramUser

SCRAPERS_OUTPUT_DIR = settings.BASE_DIR / "scrapers_output" / "tgju"

coin_json_file_path = os.path.join(SCRAPERS_OUTPUT_DIR, "coin.json")
gold_json_file_path = os.path.join(SCRAPERS_OUTPUT_DIR, "gold.json")
currency_json_file_path = os.path.join(SCRAPERS_OUTPUT_DIR, "currency.json")


class TGJUCoinView(RetrieveAPIView):
    """Retrieve TGJU coin data as a read-only endpoint."""

    http_method_names = ["post"]
    serializer_class = TGJUDataSerializer
    authentication_classes = [APIKeyAuthentication]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        """Retrieve TGJU coin data as a read-only endpoint."""
        try:
            # Check if the user is allowed to make a request
            tg_user_id = request.data.get("user_id")
            if not tg_user_id:
                return Response(
                    {"message": "TG user ID not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            tg_user = TelegramUser.objects.filter(user_id=tg_user_id).first()
            if not tg_user:
                return Response(
                    {"message": "TG user not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not tg_user.can_make_request():
                return Response(
                    {"message": "TG user cannot make a request."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Read the JSON file
            if not os.path.exists(coin_json_file_path):
                return Response(
                    {"message": "Coin data file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            coin_data = []

            with open(coin_json_file_path, "r", encoding="utf-8") as file:
                coin_data = json.load(file)

            serializer = self.get_serializer(coin_data, many=True)

            # Create a command for the user
            TelegramCommand.objects.create(
                tg_user=tg_user,
                command_type="coin",
            )

            # Update the last seen time
            tg_user.update_last_seen()

            # Increment the request count
            tg_user.increment_request_count()

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


class TGJUGoldView(RetrieveAPIView):
    """Retrieve TGJU gold data as a read-only endpoint."""

    http_method_names = ["post"]
    serializer_class = TGJUDataSerializer
    authentication_classes = [APIKeyAuthentication]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        """Retrieve TGJU gold data as a read-only endpoint."""
        try:
            # Check if the user is allowed to make a request
            tg_user_id = request.data.get("user_id")
            if not tg_user_id:
                return Response(
                    {"message": "TG user ID not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            tg_user = TelegramUser.objects.filter(user_id=tg_user_id).first()
            if not tg_user:
                return Response(
                    {"message": "TG user not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not tg_user.can_make_request():
                return Response(
                    {"message": "TG user cannot make a request."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Read the JSON file
            if not os.path.exists(gold_json_file_path):
                return Response(
                    {"message": "Gold data file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            gold_data = []

            with open(gold_json_file_path, "r", encoding="utf-8") as file:
                gold_data = json.load(file)

            serializer = self.get_serializer(gold_data, many=True)

            # Create a command for the user
            TelegramCommand.objects.create(
                tg_user=tg_user,
                command_type="gold",
            )

            # Update the last seen time
            tg_user.update_last_seen()

            # Increment the request count
            tg_user.increment_request_count()

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


class TGJUCurrencyView(RetrieveAPIView):
    """Retrieve TGJU currency data as a read-only endpoint."""

    http_method_names = ["post"]
    serializer_class = TGJUDataSerializer
    authentication_classes = [APIKeyAuthentication]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        """Retrieve TGJU currency data as a read-only endpoint."""
        try:
            # Check if the user is allowed to make a request
            tg_user_id = request.data.get("user_id")
            if not tg_user_id:
                return Response(
                    {"message": "TG user ID not provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            tg_user = TelegramUser.objects.filter(user_id=tg_user_id).first()
            if not tg_user:
                return Response(
                    {"message": "TG user not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if not tg_user.can_make_request():
                return Response(
                    {"message": "TG user cannot make a request."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Read the JSON file
            if not os.path.exists(currency_json_file_path):
                return Response(
                    {"message": "Currency data file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            currency_data = []

            with open(currency_json_file_path, "r", encoding="utf-8") as file:
                currency_data = json.load(file)

            serializer = self.get_serializer(currency_data, many=True)

            # Create a command for the user
            TelegramCommand.objects.create(
                tg_user=tg_user,
                command_type="currency",
            )

            # Update the last seen time
            tg_user.update_last_seen()

            # Increment the request count
            tg_user.increment_request_count()

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
