from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout,get_user_model
from .forms import Loginform,RegisterForm,ImageForm,ProfileForm,UpdateProfileForm
from django.contrib.auth.decorators import login_required
from .email import send_register_confirm_email
from .models import Images,Profile
from django.views.generic import RedirectView

User =get_user_model()
# Create your views here.

@login_required
def home(request):
    current_user = request.user
    images = Images.get_all_images()
    users = User.objects.all()
    
    return render(request,"home.html",{"images":images,"current_user":current_user,"users":users,})

def login_view(request):
    next = request.GET.get('next')
    form = Loginform(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username = username,password=password)
        login(request,user)
        if next:
            return redirect(next)
        return redirect('/')
    return render(request,"registration/login.html",{"form":form})

def register_view(request):
    next = request.GET.get('next')
    form =RegisterForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get('email')
        username = form.cleaned_data.get('username')
        user = form.save(commit=False)
        password  = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        send_register_confirm_email(username,email)
        if next:
            return redirect(next)
        return redirect('/')
    return render(request, 'registration/registration.html',{"form":form})

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
def edit_profile(request):
    current_user = request.user
    
    if request.method =='POST':
        form = ProfileForm(request.POST,request.FILES)

        if form.is_valid():
            profile = form.save(commit = False)
            profile.name = current_user
            profile.save()
        return redirect('home')
    else:
        form = ProfileForm()
    return render(request,"General/edit_profile.html",{"current_user":current_user,"form":form})

@login_required
def profile(request):
    name = request.user
    profile = Profile.get_profile_by_name(name)
    images = Images.get_images_by_name(name)

    return render(request,"General/profile.html",{"profile":profile,"images":images})
    
@login_required
def update_profile(request):
    current_user= request.user
    profile = Profile.get_profile_by_name(current_user)

    if request.method =='POST':
        form = UpdateProfileForm(request.POST,request.FILES)

        if form.is_valid():
            pic = form.cleaned_data.get("profile_pic")
            bio = form.cleaned_data.get("bio")
            profile.bio = bio

            profile.update(bio = bio,profile_pic = pic)
        return redirect('profile')
    else:
        form = UpdateProfileForm()
    return render(request,"General/update_profile.html",{"form":form})

def like(request):
    user = request.user
    image = get_object_or_404(Images,id= request.POST.get('image.id') )
    if image.liked.filter(id = user.id).exists():
        image.liked.remove(user)
    else:
        image.liked.add(request.user)
    return redirect('home')

