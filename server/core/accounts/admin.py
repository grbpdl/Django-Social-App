from django.contrib import admin
from .models import User, Follower, PasswordResetOTP

admin.site.register(User)
admin.site.register(Follower)
admin.site.register(PasswordResetOTP)