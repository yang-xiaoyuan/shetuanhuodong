from django.db import models

# Create your models here.
class users(models.Model):
    user_name = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=12, null=False)
    create_time = models.DateTimeField()
    sex = models.CharField(max_length=1, null=True)
    image = models.BinaryField(null=True)
    phone_number = models.CharField(max_length=15)
    teams = models.TextField(null=True)
    activities = models.TextField(null=True)
    time_schedule = models.CharField(max_length=84, null=True)
    self_introduction = models.TextField(null=True)
    friends = models.TextField(null=True)


class teams(models.Model):
    team_name = models.CharField(max_length=15, unique=True)
    team_members = models.TextField()
    creator = models.CharField(max_length=15)
    team_introduction = models.TextField(null=True)
    activities = models.TextField(null=True)
    previous_activities = models.TextField(null=True)
    uploaded_person_number = models.TextField(null=True)


class activities(models.Model):
    name = models.CharField(max_length=20)
    time = models.DateTimeField()
    location = models.CharField(max_length=30)
    content = models.TextField()
    requirement = models.CharField(max_length=30)
    launcher = models.CharField(max_length=10)
    team = models.CharField(max_length=15, null=True)
    status = models.BooleanField(default=True)