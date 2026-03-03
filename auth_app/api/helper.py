from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache

def check_token_is_valid(token):
    
    try:
        token = RefreshToken(token)
        return token
    except (TokenError, InvalidToken):
        return None



@lru_cache()
def logo_data():
    with open(finders.find('emails/logo.png'), 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data, _subtype="png")
    logo.add_header('Content-ID', '<logo>')
    return logo