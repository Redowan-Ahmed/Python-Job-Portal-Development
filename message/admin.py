from django.contrib import admin
from .models import Message, TestModel
# Register your models here.

admin.site.register(model_or_iterable=Message)
admin.site.register(model_or_iterable=TestModel)