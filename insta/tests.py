from django.test import TestCase
from .models import Profile,Images,Comment

class ProfileTestClass(TestCase):

    def setup(self):
        self.profile = Profile(user = 'dan',profile_pic = 'd.jpg',bio ='my bio',followers = '1',following = '1',updated_on = '12/7/1019')
        self.profile.save()
    def test_instance(self):
        self.assertTrue(isinstance(self.profile,Profile))

    def test_get_profile_by_user(self):
        profile = Profile.get_profile_by_name(dan)
        self.assertTrue(profile == self.profile)

class CommentTestClass(TestCase):
    def setUp(self):
        self.comment = Comment(comment = 'i am a comment',posted_by = 'dan',posted_on = '12/23/2017',image_id='1')
        self.comment.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.comment,Comment))
    def test_get_all_comments(self):
        self.comment.save()
        comments = Comment.get_all_comments()
        self.assertTrue(len(comments)==1)
    def test_get_comment_by_image_id(1):
        self.comment.save()
        comments = Comment.get_comment_by_image_id(1)
        self.assertTrue(len(comments)==1)
class ImagesTestClass(TestCase):
    def setUp(self):
        self.image = Images(name='image',caption="happy now",image = 's.jpg',post_date = "4/12/2019",liked = 'dan',posted_by = 'dan')
        self.image.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.image,Images))

    def test_get_all_images():
        self.image.save()
        images = Images.get_all_images()
        self.assertTrue(len(image)==1)
    def test_get_images_by_name(image):
        self.image.save()
        image = Images.get_images_by_name(image)
        self.assertTrue(image.caption == 'happy now')
# Create your tests here.
