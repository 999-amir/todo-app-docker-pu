from django.urls import path, include
app_name = 'api_v1'

urlpatterns = [
    path('user/', include('accounts.api.v1.urls.user', namespace='user')),
    path('profile/', include('accounts.api.v1.urls.profile', namespace='profile'))
]
