import os
import json
from django.conf import settings

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.throttling import ScopedRateThrottle

from scrapers.serializers import CoinexDataSerializer
from api_keys.authentication import APIKeyAuthentication
from telegram.models import TelegramCommand, TelegramUser

SCRAPERS_OUTPUT_DIR = settings.BASE_DIR / "scrapers_output" / "coinex"

crypto_json_file_path = os.path.join(SCRAPERS_OUTPUT_DIR, "crypto.json")


class CoinexCryptoView(RetrieveAPIView):
    http_method_names = ["post"]
    serializer_class = CoinexDataSerializer
    authentication_classes = [APIKeyAuthentication]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
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
            if not os.path.exists(crypto_json_file_path):
                return Response(
                    {"message": "crypto data file not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            crypto_data = []

            with open(crypto_json_file_path, "r", encoding="utf-8") as file:
                crypto_data = json.load(file)

            serializer = self.get_serializer(crypto_data, many=True)

            # Create a command for the user
            TelegramCommand.objects.create(
                tg_user=tg_user,
                command_type="crypto",
            )

            # Update the last seen time
            tg_user.update_last_seen()

            # Increment the request count
            tg_user.increment_request_count()

            return Response(
                {
                    "data": serializer.data,
                    "retrieved_at": crypto_data[0].get("last_update"),
                    "message": "Coinex crypto data retrieved successfully.",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"message": f"Error retrieving Coinex crypto data"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
