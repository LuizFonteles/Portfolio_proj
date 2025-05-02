from django.contrib import admin
from django.urls import path, include
from proj import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('register/', views.register_user ,name = 'register'),
    path('api/', include('api.urls'), name ='api'),
]
