from django.urls import path, include
from back_end import views

urlpatterns = [
    path("", views.login, name='login'),

]