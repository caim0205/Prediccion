from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Cuenta, Rol

class SignUpForm(UserCreationForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all(), required=True)

    class Meta:
        model = Cuenta
        fields = ('email', 'rol', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

class CSVUploadForm(forms.Form):
    archivo = forms.FileField()
