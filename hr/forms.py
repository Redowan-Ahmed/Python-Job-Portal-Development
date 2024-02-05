from django import forms
from .models import Company
# from django.utils.translation import gettext_lazy as _


# class AuthorForm(ModelForm):
#     class Meta:
#         model = Author
#         fields = ["name", "title", "birth_date"]
        # widgets = {
        #             "name": Textarea(attrs={"cols": 80, "rows": 20}),
        #         }
#         labels = {
#             "name": _("Writer"),
#         }
#         help_texts = {
#             "name": _("Some useful help text."),
#         }
#         error_messages = {
#             "name": {
#                 "max_length": _("This writer's name is too long."),
#             },
#         }

class CompanyForm(forms.ModelForm):
        class Meta:
                model=Company
                fields = '__all__'
                exclude = ['user','status']
                labels = {
                        'company_name': 'Name',
                }
                widgets = {
                        'company_name': forms.TextInput(attrs={
                                'class':'form-control',
                                }),
                        'company_logo': forms.FileInput(attrs={
                                'class':'form-control form-control-lg',
                                }),
                        'location': forms.TextInput(attrs={
                                'class':'form-control',
                                }),
                        'website': forms.URLInput(attrs={
                                'class':'form-control',
                                }),
                        'email': forms.EmailInput(attrs={
                                'class':'form-control',
                                }),
                        'employ_volume_average': forms.Select(attrs={
                                'class':'form-select form-control',
                                }),
                        'phone_number': forms.TextInput(attrs={
                                'class':'form-control',
                                })
                }
class CompanyFormEdit(forms.ModelForm):
        class Meta:
                model=Company
                fields = '__all__'
                exclude = ['user']
                labels = {
                        'company_name': 'Name',
                }
                widgets = {
                        'company_name': forms.TextInput(attrs={
                                'class':'form-control',
                                }),
                        'company_logo': forms.FileInput(attrs={
                                'class':'form-control form-control-lg',
                                }),
                        'location': forms.TextInput(attrs={
                                'class':'form-control',
                                }),
                        'website': forms.URLInput(attrs={
                                'class':'form-control',
                                }),
                        'email': forms.EmailInput(attrs={
                                'class':'form-control',
                                }),
                        'employ_volume_average': forms.Select(attrs={
                                'class':'form-select form-control',
                                }),
                        'phone_number': forms.TextInput(attrs={
                                'class':'form-control',
                                }),
                        'status': forms.Select(attrs={
                                'class':'form-control',
                                })
                }