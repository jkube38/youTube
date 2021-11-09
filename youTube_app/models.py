from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class DownloadUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    download_path = models.CharField(max_length=180)
    downloads = models.ManyToManyField('VidData', symmetrical=False)
    user_pic = models.FileField(blank=True, null=True, upload_to='images')

    def __str__(self):
        return self.username


class VidData(models.Model):
    thumb = models.URLField(max_length=200)
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.title


class TemporaryUrl(models.Model):
    snippet = models.CharField(max_length=16)
    user = models.CharField(max_length=30)

    def __str__(self):
        return self.user
