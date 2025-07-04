from django.contrib import admin
from django.urls import path, include
from proj import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('admin/', admin.site.urls),
    path('register/', include('register.urls')),
    path('login/', views.login_user, name= 'login'),
    path('logout/', views.logout_user, name= 'logout'),
    path('api/', include('api.urls')),
    path('portfolio/', include('portfolio.urls')),
]
