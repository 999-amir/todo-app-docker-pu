from django.urls import path, include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile-description', views.ProfileDescription.as_view(), name='profile_description'),
    # api
    path('api/v1/', include('accounts.api.v1.urls', namespace='api_v1')),
]
