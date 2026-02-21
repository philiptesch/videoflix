from django.urls import path
from .views import RegistrationView, AccountActivatedView, LoginView, LogoutView, RefreshTokenView, PasswordResetView

urlpatterns = [
   path('register/', RegistrationView.as_view(), name='registration'),
  path('activate/<str:uidb64>/<str:token>/', AccountActivatedView.as_view(), name='activate'),
  path('login/', LoginView.as_view(), name='login'),
  path('logout/', LogoutView.as_view(), name='logout'),
  path('token/refresh/', RefreshTokenView.as_view(), name='refresh'),
  path('password_reset/', PasswordResetView.as_view(), name='reset_Password')
]