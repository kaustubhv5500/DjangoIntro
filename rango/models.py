from django.db import models
import uuid
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=125, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(blank= True,max_length=31,help_text="Category of Website")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Page(models.Model):
    category = models.ForeignKey(Category,on_delete = models.DO_NOTHING)
    title = models.CharField(max_length=125)
    url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete= models.DO_NOTHING)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to="profile_images",blank= True)

    def __str__(self):
        return self.user.username



# Create your models here.
