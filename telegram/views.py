from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle

from telegram.models import TelegramUser
from arz_watch_api.utils import async_notify_superusers
from api_keys.authentication import APIKeyAuthentication


class TelegramUserCreateView(APIView):
    http_method_names = ["post"]
    authentication_classes = [APIKeyAuthentication]  # You can set your custom one here

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):

        user_id = request.data.get("user_id")

        if not user_id:
            return Response(
                {"error": "user_id is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Try to get existing user or create a new one
        user, created = TelegramUser.objects.update_or_create(
            user_id=user_id,
            defaults={
                "username": request.data.get("username", ""),
                "first_name": request.data.get("first_name", ""),
                "last_name": request.data.get("last_name", ""),
                "is_bot": request.data.get("is_bot", False),
                "language_code": request.data.get("language_code", ""),
                "last_seen": request.data.get("last_seen"),
            },
        )

        # Notify superusers after the user is created/updated
        message = f"Telegram user {'created' if created else 'updated'}\nusername: {user.username}, first name: {user.first_name}, last name: {user.last_name}"
        async_notify_superusers(message)

        return Response(
            {"message": "Created" if created else "Updated"},
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class TelegramUserInfoView(APIView):
    http_method_names = ["post"]
    authentication_classes = [APIKeyAuthentication]

    throttle_scope = "user"
    throttle_classes = [ScopedRateThrottle]

    def post(self, request: Request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            if not user_id:
                return Response(
                    {"error": "user_id is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = TelegramUser.objects.filter(user_id=user_id).first()
            if not user:
                return Response(
                    {"error": "User not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            return Response(
                {
                    "request_count": user.request_count,
                    "max_request_count": user.max_requests,
                    "created_at": user.created_at,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"Error retrieving user info"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
