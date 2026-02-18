
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
from .seralizers import RegistrationSerializer, LoginSeralizer
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .helper import  check_token_is_valid

class RegistrationView(APIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        host = request.get_host()
        user.is_active = False
        user.save()
        mail = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        user_display = user.username if user.username else user.email

        message = render_to_string('account_active_email.html', {'user': user_display,'domain': host, 'uid': uid, 'token': token})

        email =EmailMultiAlternatives(
        subject='My email',
        body=message,
        from_email='noreply@example.com',
        to=[mail])
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)
        print('nmame')
        print(username)

        response = Response({"user":{'id': user.id, 'email':mail  },'token': 'activation_token'}, status=status.HTTP_200_OK)

        return response

class AccountActivatedView(APIView):

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
        serializer_class = LoginSeralizer


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
     
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        
        access_token = request.COOKIES.get('access_token') 
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