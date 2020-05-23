"""shetuanhuodong_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include
from shetuanhuodong_backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.login, name='login'),
    path("register/", views.register, name='register'),
    path("home/", views.home, name='home'),
    path("home/activity/", views.activity, name='activity'),
    path("home/team/", views.team, name='team'),
    path("home/me/", views.me, name='me'),
    path("home/activity_info/", views.activity_info, name='activity_info'),
    path("home/sign_out_activity/", views.sign_out_activity, name='sign_out_activity'),
    path("home/launch_activity/", views.launch_activity, name='launch_activity'),
    path("home/personal_info/", views.personal_info, name='personal_info'),
    path("home/change_name/", views.change_name, name='change_name'),
    path("home/change_introduction/", views.change_introduction, name='change_introduction'),
    path("home/change_sex/", views.change_sex, name='change_sex'),
    path("home/fetch_load/", views.fetch_load, name='fetch_load'),
    path("home/upload/", views.upload, name='upload'),
    path("home/previous_activities/", views.previous_activities, name='previous_activities'),
    path("home/create_team/", views.create_team, name='create_team'),
    path("home/user/", views.user, name='user'),
    path("home/team_info/", views.team_info, name='team_info'),
    path("home/results/", views.results, name='results'),
    path("home/results2/", views.results2, name='results2'),
    path("home/leave_team/", views.leave_team, name='leave_team'),
    path("home/change_team_name/", views.change_team_name, name='change_team_name'),
    path("home/change_team_introduction/", views.change_team_introduction, name='change_team_introduction'),
    path("home/check_activity_in_team/", views.check_activity_in_team, name='check_activity_in_team'),
    path("home/dismiss_team/", views.dismiss_team, name='dismiss_team'),
    path("home/search_for_activity/", views.search_for_activity, name='search_for_activity'),
    path("home/sign_in_activity/", views.sign_in_activity, name='sign_in_activity'),
    path("home/show_people_in_activity/", views.show_people_in_activity, name='show_people_in_activity'),
    path("home/delete_activity/", views.delete_activity, name='delete_activity'),
    path("home/search_for_users/", views.search_for_users, name='search_for_users'),
    path("home/add_member/", views.add_member, name='add_member'),
    path("home/delete_member/", views.delete_member, name='delete_member'),
    path("home/check_friends/", views.check_friends, name='check_friends'),
    path("home/check_team_members/", views.check_team_members, name='check_team_members'),
    path("home/check_team_upload/", views.check_team_upload, name='check_team_upload'),
    path("home/change_nickname/", views.change_nickname, name='change_nickname'),
    path("home/nickname_user/", views.nickname_user, name='nickname_user'),
    path("home/send_verify/", views.send_verify, name='send_verify'),
    path("home/response/", views.response, name='response'),
    path("home/search_team/", views.search_team, name='search_team'),
]
