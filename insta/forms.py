from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .models import Images,Profile,Comment

User = get_user_model()
class Loginform(forms.Form):
    username =forms.CharField(label='Your username',max_length= 50)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user= User.objects.filter(username=username)
            if not user:
                raise forms.ValidationError('papapapapapa')
            if not user.check_password(password):
                raise forms.ValidationError('Incoreect password')
        return super(Loginform, self).clean(*args, **kwargs)


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    email2 = forms.EmailField(label='confirm email')
    username = forms.CharField(label='your username')
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password',
            
        ]
    def clean_password(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        username = self.cleaned_data.get('username')

        if email != email2:
            raise forms.ValidationError('email must match')
        user = User.objects.filter(username = username)
        if user.exists():
            raise forms.ValidationError('This username exists!')
        return username 

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        exclude = [
            'posted_by',
            'posted_date',
            'liked',
            'comments'
        ]
            
class UserUpdateform(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

class UpdateProfileForm(forms.ModelForm):
    bio = forms.Textarea()
    class Meta:
        model = Profile
        exclude =[
            'updated_on',
            'user',
            'followers',
            'following',
        ]
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment'
        ]



    
