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
    current_user = request.user
    images = Images.get_all_images()
    users = User.objects.all()
    
    return render(request,"home.html",{"images":images,"current_user":current_user,"users":users,})



def logout_view(request):
    logout(request)
    return redirect('/')
@login_required
def post_image(request):
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
    name = request.user
    profile = Profile.get_profile_by_name(name)
    images = Images.get_images_by_name(name)

    return render(request,"General/profile.html",{"profile":profile,"images":images,"name":name})
    
@login_required
def update_profile(request):
   
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
    user = request.user
    image = get_object_or_404(Images,id= request.POST.get('image.id') )
    if image.liked.filter(id = user.id).exists():
        image.liked.remove(user)
    else:
        image.liked.add(request.user)
    return redirect('home')

def follow(request):
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




            