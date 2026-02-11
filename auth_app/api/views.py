
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.views import APIView
from django.utils.http import base36_to_int, int_to_base36
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template import Context, Template
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives
from .seralizers import RegistrationSerializer
from django.template.loader import get_template

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

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        try:
            get_template('auth_app/account_active_email.html')
            print("Template gefunden ✅")
        except Exception as e:
            print("Template nicht gefunden ❌", e)

        message = render_to_string('account_active_email.html', {'user': user,'domain': host, 'uid': uid, 'token': token})

        email =EmailMultiAlternatives(
        subject='My email',
        body=message,
        from_email='noreply@example.com',
        to=[mail])
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=False)


        response = Response({"user":{'id': user.id, 'email':mail  },'token': 'activation_token' }, status=status.HTTP_200_OK)

        return response