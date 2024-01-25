from django.db import models
from base.model import BaseModel
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

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


    def __str__(self) -> str:
        return self.full_name

class PostLike(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_posts',db_index=True)
    post = models.ForeignKey('BlogPost', related_name="likes",on_delete=models.CASCADE, db_index=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} liked {self.post.title}'

class Category(BaseModel):
    name = models.CharField(max_length=100, db_index=True)
    slug  = models.SlugField(max_length=150, db_index=True)

    def __str__(self) -> str:
        return self.name

class Comment(BaseModel):
    comment = RichTextField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_comments', db_index=True)
    reply = models.ForeignKey('self', on_delete= models.CASCADE, related_name='replies', db_index=True, blank=True, null=True)
    post = models.ForeignKey('BlogPost', on_delete=models.CASCADE, related_name='comments', db_index=True)

    def __str__(self) -> str:
        if not self.reply:
            return f"Comment by: {self.user.get_full_name()} on blog post( {self.post.title} )"
        else:
            return f"{self.reply.user.get_full_name()} replied to {self.reply.comment} "

class BlogPost(BaseModel):
    title = models.CharField(max_length=400, db_index=True)
    content = RichTextUploadingField(max_length=6000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name ='posts', db_index=True)
    thumbnail = models.ImageField(upload_to='blog-posts')
    tags = models.CharField(max_length=150, blank=True, default="unknown", db_index=True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE, related_name='posts', db_index=True)
    slug = models.SlugField(max_length=500, unique=True, db_index=True, blank=True)
    STATUS_CHOICES = (('Published', 'Published'), ('Draft', "Draft"))
    status = models.CharField(max_length=100, choices= STATUS_CHOICES, default='Published')

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            slug = slugify(value=self.title)
            exists: bool = BlogPost.objects.filter(slug=slug).exists()
            if exists:
                self.slug = slugify(value=f"{slug} { str(object=self.pk).split(sep='-')[0] }")
            else:
                self.slug = slug
        super(BlogPost, self).save(*args, **kwargs)