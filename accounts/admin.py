from django.contrib import admin
from .models import HrProfile, CandidateProfile, User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


admin.site.register(model_or_iterable=HrProfile)
admin.site.register(model_or_iterable=CandidateProfile)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email','phone_number' ,'profile_picture', 'password')}),
        ('Permissions and Security', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'email_verified', 'otp', 'email_token', 'is_hr', 'is_candidate')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')})
    )
    list_display = ('email','phone_number', 'is_active',
                    'is_staff', 'is_superuser', 'last_login','is_hr', 'is_candidate')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'is_hr', 'is_candidate')}
         ),
    )
    ordering = []


admin.site.register(User, CustomUserAdmin)
