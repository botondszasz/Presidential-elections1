from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Event, Profile

# Unregister Groups
admin.site.unregister(Group)

# Register Profile
admin.site.register(Profile)

# Register Event
admin.site.register(Event)





	
