
from datetime import datetime, timedelta
from django.shortcuts                   import get_object_or_404, render
from rest_framework.decorators          import api_view, permission_classes
from rest_framework.response            import Response
from rest_framework                     import status
from rest_framework.permissions         import IsAuthenticated
from rest_framework.authtoken.models    import Token
from django.contrib.auth.models         import User
from django.contrib.auth.hashers        import make_password
from django.contrib.auth                import authenticate
from django.core.mail                   import send_mail
from django.utils.crypto                import get_random_string

from accounts.serializers               import *
from accounts.models                    import *

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
    
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    # old data
    user = request.user
    # new data
    data = request.data
    # update old data to new data
    user.first_name = data['first_name']
    user.last_name  = data['last_name']
    user.username   = data['email']
    user.email      = data['email']
    
    if data['password'] != "":
        user.password = make_password( data['password'] )
    # save
    user.save()
    # convert all data to api 
    serializers = UserSerializer(user, many=False)
    
    return Response(serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    user = UserSerializer(request.user, many=False)
    return Response(user.data)

@api_view(['POST'])
def userLogin(request):
    data     = request.data 
    username = data.get('email')
    password = data.get('password')
    user     = authenticate(request, username=username, password=password)
    
    if user is not None:
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'token':token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error':'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
def get_current_host(request):
    # get protpcol (http - https) 
    protocol = request.is_secure() and 'https' or 'https'
    # get host
    host     = request.get_host()
    # return
    return "{protocol}://{host}/".format(protocol=protocol, host=host)

@api_view(['POST'])
def forgot_password(request):
    # get data
    data  = request.data
    user  = get_object_or_404(User, email=data['email'])
    # make a random token
    token       = get_random_string(40)
    # make a expire date
    expire_data = datetime.now() + timedelta(minutes=30)
    # take a data
    user.profile.reset_password_token  = token
    user.profile.reset_password_expire = expire_data
    user.profile.save()
    #
    host = get_current_host(request)
    link = "{host}api/reset_password/token/".format(host=host)
    body = "Your password reset link is : {link}".format(link=link)
    send_mail(
        "password reset",
        body,
        "yusif@gmail.com",
        [data['email']]
    )
    return Response({'details':'password reset sent to {email}'.format(email=data['email'])})
    
    
    
    
    