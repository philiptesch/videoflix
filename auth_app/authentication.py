from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that reads the access token from a cookie.

    Behavior:
        - Overrides the default JWTAuthentication to allow tokens to be sent via cookies.
        - Checks for an 'access_token' cookie in the incoming request.
        - Validates the token using the standard JWT validation.
        - Returns the authenticated user and validated token if successful.
        - Returns None if no cookie is found or token is invalid/expired.
    """

    def authenticate(self, request):
        """
        Authenticate the user based on the JWT access token stored in cookies.

        Args:
            request (HttpRequest): The incoming Django REST Framework request.

        Returns:
            tuple(User, validated_token) | None:
                - Returns a tuple of the authenticated User and validated JWT token if successful.
                - Returns None if the access token is missing or invalid.
        """

        access_token = request.COOKIES.get("access_token")

        if access_token is None:
            return None

        try:
            validated_token = self.get_validated_token(access_token)
        except TokenError:
            return None

        return self.get_user(validated_token), validated_token