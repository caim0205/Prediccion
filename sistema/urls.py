"""
URL configuration for sistema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio, name='inicio'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('registration/signup.html/', views.signup, name='signup'),
    path('inicio/ayuda/', views.ayuda, name='ayuda'),
    path('registration/recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('registration/gestionar_usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    #path('registration/register.html/', views.register, name='register'),
    path('accounts/login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='login'), name='logout'),
]



''''
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login,logout_then_login


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('accounts/login',login,{'template_name':'.html'},name='login'),
    #path('logout/', logout_then_login, name='logout'),  
]
'''