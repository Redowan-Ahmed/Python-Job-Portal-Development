from ast import mod
from django.db import models
from base.model import BaseModel
from django.core.validators import RegexValidator
from django.conf import settings



class SupportContact(BaseModel):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(verbose_name='Email Address')
    phoneNumberRegex = RegexValidator(
        regex=r"^\+?1?\d{8,15}$", message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phoneNumberRegex], max_length=17, default=8801632398271
    )
    subject = models.CharField(max_length=300)
    message = models.TextField(max_length=5000, blank=True)


    def __str__(self):
        return self.full_name

class PostLike(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_posts',db_index=True)
    post = models.ForeignKey('BlogPost', related_name="likes",on_delete=models.CASCADE, db_index=True)

    def __str__(self):
        return f'{self.user.get_full_name} liked {self.post.title}'

class Category(BaseModel):
    name = models.CharField(max_length=100, db_index=True)
    slug  = models.SlugField(max_length=150, db_index=True)

    def __str__(self):
        return self.name

class Comment(BaseModel):
    title = models.CharField(max_length=200, db_index=True)
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comments', db_index=True)
    reply = models.ForeignKey('self', on_delete= models.CASCADE, related_name='parent_comments', db_index=True)
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments', db_index=True)

    def __str__(self):
        return f"Comment by: {self.user.username} on {self.post.title}"

class BlogPost(BaseModel):
    title = models.CharField(max_length=400, db_index=True)
    content = models.TextField(max_length=6000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='posts', db_index=True)
    thumbnail = models.ImageField(upload_to='blog-posts')
    tags = models.CharField(max_length=150, blank=True, default="unknown", db_index=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='posts', db_index=True)

    def __str__(self):
        return self.title