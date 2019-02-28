from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name = 'index'),
    path('register/',views.register,name = 'register'),
    path('login/',auth_views.LoginView.as_view(redirect_authenticated_user=True,authentication_form=CustomAuthForm),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('profile/',views.view_profile,name='profile'),
    path('formular/',views.formular,name='formular'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)