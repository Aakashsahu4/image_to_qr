"""External Imports"""
from django.urls import path

"""Internal imports"""
from . import apis
from . import views

urlpatterns = [
    path('api/signup/', apis.SignupAPI.as_view(), name='signup'),
    path('api/login/', apis.LoginAPI.as_view(), name='login'),
    path('api/upload/', apis.UploadImageAPI.as_view(), name='upload'),
    path('api/gallery/', apis.GalleryAPI.as_view(), name='gallery'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_page, name='signup'),
    path('upload/', views.upload_page, name='upload'),
    path('images/', views.images_page, name='images'),
]