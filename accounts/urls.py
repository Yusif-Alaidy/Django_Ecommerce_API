from django.urls    import path
from accounts       import views
urlpatterns = [
    path('register/',                  views.register,        name='register'),
    path('login/',                     views.userLogin,       name='login'),
    path('userinfo/',                  views.current_user,    name='userinfo'),
    path('update/user/',               views.update_user,     name='update_user'),
    path('forgot_password/',           views.forgot_password, name='forgot_password'),
    path('reset_password/<str:token>', views.reset_password,  name='reset_password'), 
    
]
