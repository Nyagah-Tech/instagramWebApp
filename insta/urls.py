from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('new/post/', views.post_image, name = 'new-image'),
    path('new/profile/edit/', views.edit_profile, name = "edit-profile"),
    path('instagram/profile/',views.profile,name="profile"),
    path('instagram/profile/update',views.update_profile,name="update-profile"),
    path('accounts/logout/',views.logout_view,name = 'logout'),
    path('like/',views.like,name = 'like')
    
]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)