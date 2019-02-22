from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    contact = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.CharField(max_length=100, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name


class Post(models.Model):
    post_title = models.CharField(max_length=400)
    post_body = models.TextField()
    keywords = models.TextField()
    slug = models.CharField(max_length=100, default="", unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, default=47)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_published = models.DateTimeField(default=None, blank=True, null=True)
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    name = models.CharField(max_length=200)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return self.comment
