from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from .forms import Loginform,RegisterForm,ImageForm,UpdateProfileForm,UserUpdateform,CommentForm
from django.contrib.auth.decorators import login_required
from .email import send_register_confirm_email
from .models import Images,Profile,Comment
from django.contrib import messages
from django.views.generic import RedirectView

User =get_user_model()
# Create your views here.

@login_required(login_url = 'accounts/login/')
def home(request):
    '''
    this is a view function that renders our homepage
    '''
    current_user = request.user
    images = Images.get_all_images()
    users = User.objects.all()
    
    return render(request,"home.html",{"images":images,"current_user":current_user,"users":users,})

def register(request):
    '''
    this is a view function that is responsible for rendering our register form and funtionality
    '''
    if request.method == 'POST':
        username = request.POST['username']
        first_name =request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 =request.POST['password1']
        
        if password1 == password:
            if User.objects.filter(username = username):
                messages.info(request,'This username is taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,password = password,email = email,first_name = first_name,last_name = last_name,)
                user.save()
                send_register_confirm_email(username,email)
                return redirect('home')
        else:
            messages.info(request,'passwords should match')
            return redirect('register')
        
    else:
        return render(request,'registration/registration_form.html')

def logout_view(request):
    logout(request)
    return redirect('/')
@login_required
def post_image(request):
    '''
    this is a view function that enables a user to post an image
    '''
    current_user = request.user
    if request.method == 'POST':
        form = ImageForm(request.POST,request.FILES)

        if form.is_valid():
            image = form.save(commit = False)
            image.posted_by = current_user
            image.save()
        return redirect('home')
    else:
        form = ImageForm()
    return render(request,'General/new_image.html',{"form":form})
@login_required
def profile(request):
    '''
    this is a view function that will return the users profile as well as render the profile.html
    '''
    name = request.user
    profile = Profile.get_profile_by_name(name)
    images = Images.get_images_by_name(name)

    return render(request,"General/profile.html",{"profile":profile,"images":images,"name":name})
    
@login_required
def update_profile(request):
    '''
    this is a view function that carries out the update profile functionality
    '''

    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)
        form1 = UserUpdateform(request.POST,instance=request.user)
        if form.is_valid() and form1.is_valid():
            form1.save() 
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=request.user.profile)
        form1 = UserUpdateform(instance=request.user)
    return render(request,"General/update_profile.html",{"form":form,"form1":form1})

def like(request):
    '''
    view function that handles the like functionality
    '''
    user = request.user
    image = get_object_or_404(Images,id= request.POST.get('image.id') )
    if image.liked.filter(id = user.id).exists():
        image.liked.remove(user)
    else:
        image.liked.add(request.user)
    return redirect('home')

def follow(request):
    '''
    views function that handles the follow functionality
    '''
    user = request.user
    follow = get_object_or_404(Profile,user= request.POST.get('usr.id'))
    if follow.followers.filter(id = user.id).exists():
        follow.followers.remove(user)
    else:
        follow.followers.add(user)
    return redirect('home')

def navbar_view(request):
    current_user = request.user

    return render(request,'navbar.html',{"current_user":current_user})

def search_view(request):
    '''
    this is a view function that handles the search user by username functionality
    '''
    if request.method == 'POST':
        search = request.POST['search']
        searchterm = User.objects.filter(username = search).first()
        if Profile.get_profile_by_name(searchterm.id) is None:
            messages.info(request,'Username doesnot exist')
            return redirect('navbar_view')
        else:
            profile = Profile.get_profile_by_name(searchterm.id)
            images = Images.get_images_by_name(searchterm.id)
            return render(request,'General/search.html',{"profile":profile,"images":images,"search":search})
    else:
        messages.info(request,'Filling the input field')
        return redirect('home')

def find(request):
    current_user = request.user
    profile = get_object_or_404(Profile,user = current_user.id)
    usrs = User.objects.all()
    noUser = []
    users=[]
    for user in usrs:
        if profile.followers.filter(id = user.id).exists():
            noUser.append(user)
        else:
            users.append(user)
    return render(request,'General/find.html',{"users":users,"noUser":noUser})
def comment(request,id):
    '''
    view function that handles the comment feature funtionality
    '''
    if request.method =='POST':
        image = get_object_or_404(Images,id =id)
        form = CommentForm(request.POST)

        if form.is_valid():
            imageComment = form.save(commit = False)
            imageComment.posted_by = request.user
            images = Images.objects.get(id = id)
            imageComment.image_id = images
            imageComment.save()
            return redirect('home')

    else:
        form =CommentForm()
        image = get_object_or_404(Images,id =id)
        id = image.id
    return render(request,'General/comment.html',{"form":form,"id":id})

def comment_view(request,id):
    '''
    view function that contains the view comments functionality
    '''
    image = Images.objects.filter(id=id)
    comments = Comment.objects.filter(image_id = id)
    return render(request,'General/image.html',{"image":image,"comments":comments})


            