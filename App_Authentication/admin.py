from django.contrib import admin
from .models import UserProfileModel, Follow

# Register your models here.
admin.site.register(UserProfileModel)
admin.site.register(Follow) 