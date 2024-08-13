from django.urls import path
from .. import views

app_name = 'profile'

urlpatterns = [
    path('', views.ProfileAPIView.as_view(), name='profile')
]
