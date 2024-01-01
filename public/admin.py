from django.contrib import admin
from .models import SupportContact, BlogPost, Category, Comment, PostLike


admin.site.register(SupportContact)
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(PostLike)
