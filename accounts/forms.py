from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'

