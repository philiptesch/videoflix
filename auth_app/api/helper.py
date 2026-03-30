from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from email.mime.image import MIMEImage
from django.contrib.staticfiles import finders
from functools import lru_cache
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def check_token_is_valid(token):
    """
    Checks whether a given Refresh Token is valid.

    Args:
        token (str): JWT Refresh Token as a string.

    Returns:
        RefreshToken | None:
            - Returns a RefreshToken object if the token is valid.
            - Returns None if the token is invalid or expired.
    """
    
    try:
        token = RefreshToken(token)
        return token
    except (TokenError, InvalidToken):
        return None



@lru_cache()
def logo_data():
    """
    Loads the email logo and returns it as a MIMEImage object.

    Behavior:
        - Finds the file 'emails/logo.png' using Django staticfiles.
        - Reads the file bytes and converts it to a MIMEImage object.
        - Adds a 'Content-ID' header so the logo can be referenced in HTML emails.
        - Uses lru_cache to load the logo only once.

    Returns:
        MIMEImage: The logo image as a MIMEImage object.
    """
    with open(finders.find('emails/logo.png'), 'rb') as f:
        logo_data = f.read()
    logo = MIMEImage(logo_data, _subtype="png")
    logo.add_header('Content-ID', '<logo>')
    return logo



def sendRegistrationMail(message,content, mail):
    """
    Sends a registration confirmation email to a user.

    Behavior:
        - Creates an HTML-capable email using EmailMultiAlternatives.
        - Attaches the logo image.
        - Sends the email via Django's email backend.
        - Returns True if the email is sent successfully, otherwise False.

    Args:
        message (str): The HTML content of the email.
        mail (str): The recipient's email address.

    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """   
        
    email =EmailMultiAlternatives(
        subject='Confirm your email',
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[mail])

    email.attach_alternative(content, "text/html")
    email.attach(logo_data())

    try:  
        return True
    except: return False




def sendPasswordResetMail(message,content, mail):
        """
        Sends a password reset email to a user.

        Behavior:
        - Creates an HTML-capable email using EmailMultiAlternatives.
        - Attaches the logo image.
        - Sends the email via Django's email backend.
        - Returns True if the email is sent successfully, otherwise False.

        Args:
        message (str): The HTML content of the email.
        mail (str): The recipient's email address.

        Returns:
        bool: True if the email was sent successfully, False otherwise.
        """
     
        email =EmailMultiAlternatives(
                subject='Reset your Password',
                body=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[mail])
        
        email.attach_alternative(content, "text/html")
        email.attach(logo_data())

        try:  
             email.send(fail_silently=False)
             return True
        except: return False