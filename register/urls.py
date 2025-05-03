from django.urls import path
from register.views import register_user

urlpatterns = [
    path('', register_user, name='register'),
]