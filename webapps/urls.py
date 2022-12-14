"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('',views.stream, name='home'),
    path('login',views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    path('otherProfile/<int:id>', views.otherProfile, name='otherProfile'),
    path('followerStream', views.followerStream, name='followerStream'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('follow/<int:id>', views.follow, name='follow'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('myProfile', views.myProfile, name='myProfile'),
    path('socialnetwork/get-global', views.get_stream, name='socialnetwork/get-global'),
    path('socialnetwork/add-comment', views.add_comment, name='socialnetwork/add-comment'),
    path('socialnetwork/get-follower', views.get_follower, name='socialnetwork/get-follower')
]
