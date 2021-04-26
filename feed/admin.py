from django.contrib import admin
from .models import Post,UserProfile,Comments,Notification,Stories

admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Comments)
admin.site.register(Notification)
admin.site.register(Stories)