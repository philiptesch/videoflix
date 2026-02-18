from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


def check_token_is_valid(token):
    
    try:
        token = RefreshToken(token)
        return token
    except (TokenError, InvalidToken):
        return None

