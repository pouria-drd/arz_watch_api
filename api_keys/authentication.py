from api_keys.models import APIKey
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication


class APIKeyAuthentication(BaseAuthentication):
    keyword = "Api-Key"

    def authenticate(self, request):
        key = request.headers.get(self.keyword)

        if not key:
            raise AuthenticationFailed("API Key required.")

        try:
            api_key = APIKey.objects.get(key=key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API Key.")

        if not api_key.is_valid():
            raise AuthenticationFailed("API Key expired, inactive or exceeded limit.")

        api_key.increment_usage()
        return (None, None)  # No associated user
