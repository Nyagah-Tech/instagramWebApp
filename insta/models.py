from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.

class Users(models.Model):
    '''
    this is a model class that defines how users will be created
    '''
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10,blank= True)

class Images(models.Model):
    '''
    this is a model class that gives a bluepprint on how an image will be created
    '''
    name = models.CharField(max_length=255)
    caption = HTMLField()
    image = models.ImageField(upload_to = 'images/',blank = True)
    post_date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User,blank= True,related_name='post_likes')
    posted_by = models.ForeignKey(User,on_delete = models.CASCADE)
    

    @classmethod
    def get_all_images(cls):
        '''
        this is a class method that retrieves all images from the database
        '''
        images = cls.objects.all()

        return images

    @classmethod
    def get_images_by_name(cls,name):
        '''
        this is an image class method that gets images according to the user who posted it
        '''
        images = cls.objects.filter(posted_by= name)

        return images

class Profile(models.Model):
    '''
    this is a model class that defines how a user profile will be created
    '''
    user  = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to = 'images/', default='default.jpg')
    bio = HTMLField()
    followers = models.ManyToManyField(User,blank = True,related_name='followers')
    following = models.ManyToManyField(User,blank = True,related_name='following')
    updated_on = models.DateTimeField(auto_now_add=True)


    
    @classmethod
    def get_profile_by_name(cls,name):
        '''
        this is a class method that gets a profile by name
        '''
        profile = cls.objects.filter(user = name)

        return profile


class Comment(models.Model):
    '''
    this is a blueprint that gives out a layout on how a comment will be made
    '''
    comment = HTMLField()
    posted_by = models.ForeignKey(User, on_delete = models.CASCADE)
    posted_on = models.DateField(auto_now_add=True)
    image_id = models.ForeignKey(Images,on_delete= models.CASCADE)

    @classmethod
    def get_all_comments(cls):
        '''
        this is a classmethod that gets all comments from the db
        '''
        comments = cls.objects.all()
        return comments
    @classmethod
    def get_comment_by_image_id(cls,image_id):
        '''
        this is a comment class method that fetches all comments that have the same image_id from the db
        '''
        comments = cls.objects.filter(image_id=image_id)
        return comments