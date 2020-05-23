from django.contrib import admin
from back_end.models import users
from back_end.models import teams
from back_end.models import activities

# Register your models here.
admin.site.register(users)
admin.site.register(teams)
admin.site.register(activities)