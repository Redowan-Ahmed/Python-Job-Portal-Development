from django.contrib import admin
from .models import HrProfile, CandidateProfile, User
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


admin.site.register(HrProfile)
admin.site.register(CandidateProfile)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'email_verified', 'otp', 'email_token', 'is_hr', 'is_candidate')}),
        ('Important dates', {'fields': ('date_joined', 'last_login')})
    )
    list_display = ('email','phone_number', 'is_active',
                    'is_staff', 'is_superuser', 'last_login','is_hr', 'is_candidate')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'is_hr', 'is_candidate')}
         ),
    )


admin.site.register(User, CustomUserAdmin)
