from api_keys.models import APIKey
from rest_framework.request import Request
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication


class APIKeyAuthentication(BaseAuthentication):
    """
    Custom Authentication class to authenticate API requests using an API Key.
    """

    def authenticate(self, request: Request):
        # Step 1: Check if the API Key is present in the Authorization header
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise AuthenticationFailed(
                "API Key required in the 'Authorization' header."
            )

        # Step 2: Extract API key from the header
        if not auth_header.startswith("Api-Key "):
            raise AuthenticationFailed(
                "Invalid header format. Expected 'Api-Key <key>'."
            )

        api_key = auth_header[len("Api-Key ") :]  # Extract the key part from the header

        # Step 3: Retrieve and validate API Key in the database
        try:
            api_key_obj = APIKey.objects.get(key=api_key)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid API Key.")

        # Step 4: Check if the API key is valid (check for expiration, usage limits, etc.)
        if not api_key_obj.is_valid():
            raise AuthenticationFailed(
                "API Key expired, inactive, or exceeded usage limits."
            )

        # Step 5: Increment usage counter to track the API key's usage
        api_key_obj.increment_usage()

        return (
            None,
            None,
        )  # No user attached to this request, since this is API key-based.
