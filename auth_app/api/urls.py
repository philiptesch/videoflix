from django.urls import path
from .views import RegistrationView, AccountActivatedView

urlpatterns = [
   path('register/', RegistrationView.as_view(), name='registration'),
  path('activate/<str:uidb64>/<str:token>/', AccountActivatedView.as_view(), name='activate')
]