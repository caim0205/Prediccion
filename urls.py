from django.contrib import admin
from django.urls import path, include
from my_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Para incluir las URLs de autenticación
    path('', views.inicio, name='inicio'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('gestionar_usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('registration/recuperar_contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path('inicio/ayuda/', views.ayuda, name='ayuda'),
]
