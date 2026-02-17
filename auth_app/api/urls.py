from django.urls import path
from .views import RegistrationView, AccountActivatedView, LoginView

urlpatterns = [
   path('register/', RegistrationView.as_view(), name='registration'),
  path('activate/<str:uidb64>/<str:token>/', AccountActivatedView.as_view(), name='activate'),
  path('login/', LoginView.as_view(), name='login')
]