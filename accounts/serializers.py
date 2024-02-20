from rest_framework             import serializers
from django.contrib.auth.models import User


class signUpSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('first_name','last_name','email','password')
        
        extra_kwargs = {
            'first_name' : {'required':True, 'allow':False},
            'last_name'  : {'required':True, 'allow':False},
            'email'      : {'required':True, 'allow':False},
            'password'   : {'required':True, 'allow':False, 'min_length':8},
        }
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('first_name','last_name','email','password')
        