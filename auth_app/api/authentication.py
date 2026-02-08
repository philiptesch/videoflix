from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework_simplejwt.exceptions import TokenError

class CookieJWTAuthentication(JWTAuthentication):
 
 def authenticate(self, request):

        access_token = request.COOKIES.get("access_token")

        if access_token is None:
            return None

        try:
            validated_token = self.get_validated_token(access_token,  raise_exception=True)
        except TokenError:
            return None

        return self.get_user(validated_token), validated_token
