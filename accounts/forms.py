from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from allauth.account.forms import SignupForm
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = '__all__'

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=100, required=True, label='Enter First Name')
    last_name = forms.CharField(max_length=100, required=True, label='Enter Last Name')
    phoneNumberRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$", message="Phone number must be entered in the format: '+999999999'.")
    phone_number = forms.CharField(
        validators=[phoneNumberRegex], max_length=16, required=True, label='Enter Phone Number'
    )

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.save()
        return user