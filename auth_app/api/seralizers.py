from rest_framework import serializers
from django.contrib.auth.models import User, AbstractUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



class RegistrationSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only=True)
    confirmed_password = serializers.CharField(write_only=True)
    username = serializers.CharField(read_only=True)
     

    def validate(self, attrs):
        password = attrs.get("password")
        confirmed_password = attrs.get("confirmed_password")

    
        if confirmed_password != password:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs
    
    
    def create(self, validated_data):
        validated_data.pop('confirmed_password', None)
        email = validated_data.get('email')
        validated_data['username'] = email

        password = validated_data.pop('password')

        # User erstellen
        user = User(**validated_data)
        user.set_password(password) 
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'password', 'confirmed_password', 'email', 'username' ]


class LoginSeralizer(serializers.ModelSerializer):

    
    

       class Meta:
        model = User
        fields = ['id', 'password', 'confirmed_password', 'email', 'username' ]