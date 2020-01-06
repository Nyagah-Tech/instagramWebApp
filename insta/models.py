from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Users(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10,blank= True)

class Images(models.Model):
    name = models.CharField(max_length=255)
    caption = HTMLField()
    image = models.ImageField(upload_to = 'images/',blank = True)
    post_date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User,blank= True,related_name='post_likes')
    posted_by = models.ForeignKey(User,on_delete = models.CASCADE)
    

    @classmethod
    def get_all_images(cls):
        images = cls.objects.all()

        return images

    @classmethod
    def get_images_by_name(cls,name):
        images = cls.objects.filter(posted_by= name)

        return images

class Comment(models.Model):
    comment = HTMLField()
    posted_by = models.ForeignKey(User, on_delete = models.CASCADE)
    posted_on = models.DateField(auto_now_add=True)
    image_id = models.ForeignKey(Images,on_delete= models.CASCADE)
