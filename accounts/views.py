from django.shortcuts                   import render
from rest_framework.decorators          import api_view, permission_classes
from rest_framework.response            import Response
from rest_framework                     import status
from rest_framework.permissions         import IsAuthenticated
from rest_framework.authtoken.models    import Token
from django.contrib.auth.models         import User
from django.contrib.auth.hashers        import make_password
from django.contrib.auth                import authenticate, login

from accounts.serializers               import *

# Create your views here.

@api_view(['POST'])
def register(request):
    RegisterData = request.data
    Register     = SignUpSerializer(data = RegisterData)
    
    if Register.is_valid():
        if not User.objects.filter(username=RegisterData['email']).exists():
            Register = User.objects.create(
                first_name = RegisterData['first_name'],
                last_name  = RegisterData['last_name'],
                email      = RegisterData['email'],
                username   = RegisterData['email'],
                password   = make_password(RegisterData['password']),
            )
            context = {
                'details':'Your Account Registerd Successfully',
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':'This Email Already Exists!'},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(Register.errors)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = SignUpSerializer(request.user)
    return Response(user.data)

@api_view(['POST'])
def userLogin(request):
    data     = request.data 
    username = data.get('email')
    password = data.get('password')
    user     = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'token':token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
