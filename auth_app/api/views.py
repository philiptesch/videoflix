
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.views import APIView
from django.utils.http import base36_to_int, int_to_base36
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template import Context, Template
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives
from .seralizers import RegistrationSerializer, LoginSeralizer, PasswordResetSeralizer, ConfirmResetPasswordSeralizer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import  AllowAny
from .helper import  check_token_is_valid, sendRegistrationMail, sendPasswordResetMail
from django.contrib.auth.models import User
from django.conf import settings

class RegistrationView(APIView):
    """
    API endpoint for user registration.

    Behavior:
        - Accepts POST requests with user registration data.
        - Creates an inactive user and sends an account activation email.
        - Returns user id, email, and an activation token placeholder.
    """
    permission_classes = [AllowAny]
    authentication_classes = [] 

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        host = request.get_host()
        user.is_active = False
        user.save()
        mail = serializer.validated_data.get('email')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        user_display = user.username if user.username else user.email

        message = render_to_string('account_active_email.html', {'user': user_display,'domain': host, 'uid': uid, 'token': token, "FRONTEND_URL": settings.FRONTEND_URL,})
        
        if sendRegistrationMail(message, mail): 
            response = Response({"user":{'id': user.id, 'email':mail  },'token': 'activation_token'}, status=status.HTTP_200_OK)
            return response
        else: 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class AccountActivatedView(APIView):
    """
    API endpoint to activate a user account via an activation token.

    Behavior:
        - Accepts GET requests with uidb64 and token from activation link.
        - Verifies token and sets user.is_active to True.
        - Returns success message if activation is successful.
    """
    permission_classes = [AllowAny]
    authentication_classes = [] 

    def get(self, request, *args, **kwargs):
        User = get_user_model()
        uid_from_url = self.kwargs['uidb64']
        token = self.kwargs['token']

        try:
            uid =  force_str(urlsafe_base64_decode(uid_from_url))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
              return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()

        response = Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)

        return response


class LoginView(TokenObtainPairView):
        """
        API endpoint for user login with JWT authentication.

        Behavior:
            - Accepts POST requests with email and password.
            - Returns access and refresh tokens as cookies and login success info.
        """
        permission_classes = [AllowAny]
        serializer_class = LoginSeralizer
        authentication_classes = [] 

        def post(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
            
            refresh = serializer.validated_data['refresh']
            access = serializer.validated_data['access']
            response = Response({"detail": "Login successfully!","user": {'id': serializer.user.id,'username': serializer.user.username}},status=status.HTTP_200_OK)

            response.set_cookie(
                key="access_token", value=access, httponly=True, secure=True, samesite="Lax")
        
            response.set_cookie(
                key="refresh_token", value=refresh, httponly=True, secure=True, samesite="Lax")
            return response
        
class LogoutView(APIView):
    """
    API endpoint to log out a user by invalidating refresh token and deleting cookies.

    Behavior:
        - Accepts POST requests.
        - Deletes access_token and refresh_token cookies.
        - Blacklists the refresh token.
    """
     
    permission_classes = [AllowAny]
    authentication_classes = [] 
    def post(self, request, *args, **kwargs):
    
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None: 
            return Response({"detail": "refresh_token not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()

        return response

class RefreshTokenView(TokenRefreshView):
    """
    API endpoint to refresh access token using a valid refresh token cookie.

    Behavior:
        - Accepts POST requests.
        - Returns new access token in secure, httponly cookie if refresh token is valid.
     """
    
    permission_classes = [AllowAny]
    authentication_classes = [] 
    def post(self, request, *args, **kwargs):  
          
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response({"detail": "Refresh-Token is Missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        token = check_token_is_valid(refresh_token)

        if token is None:
            return Response({"detail": "Refresh token invalid"},status=status.HTTP_401_UNAUTHORIZED)

        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        response = Response({"detail": "Token refreshed", "access_token": access_token }, status=status.HTTP_200_OK)

        response.set_cookie(
                key="access_token", value=access_token, httponly=True, secure=True, samesite="Lax")

        return response
     

class PasswordResetView(APIView):
    """
    API endpoint to initiate password reset via email.

    Behavior:
        - Accepts POST requests with an email address.
        - Sends a password reset email if the email exists.
        - Returns a success message.
    """

    permission_classes = [AllowAny]
    authentication_classes = [] 
    serializer_class = PasswordResetSeralizer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            if User.objects.filter(email=email).exists():
                user= User.objects.get(email=email)
                host = request.get_host()

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                user_display = user.username if user.username else user.email

                message = render_to_string('reset_password.html', {'user': user_display,'domain': host, 'uid': uid, 'token': token, "FRONTEND_URL": settings.FRONTEND_URL})

                if sendPasswordResetMail(message,email ):
                    return Response({"detail": "An email has been sent to reset your password."}, status=status.HTTP_200_OK)
          
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ConfirmNewPasswordView(APIView):
    """
    API endpoint to confirm a new password after password reset.

    Behavior:
        - Accepts POST requests with new_password and confirm_password.
        - Validates UID and token from password reset email.
        - Sets the new password if token is valid.
        - Returns success message.
    """

    permission_classes = [AllowAny]
    authentication_classes = [] 
    serializer_class = ConfirmResetPasswordSeralizer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            uid_from_url = self.kwargs['uidb64']
            token = self.kwargs['token']
            new_password = serializer.validated_data.get('new_password').strip()

            try:
                uid =  force_str(urlsafe_base64_decode(uid_from_url))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError):
                return Response({"detail": "invalid UID"}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            if user is not None and account_activation_token.check_token(user, token):
                user.set_password(new_password)
                user.save()
                 
            response = Response({"detail": "Your Password has been successfully reset."}, status=status.HTTP_200_OK)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)