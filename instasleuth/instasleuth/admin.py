from django.contrib import admin
from .models import UserPoints, UserData

class UserPointsAdmin(admin.ModelAdmin):
    pass
class UserDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserPoints, UserPointsAdmin)
admin.site.register(UserData, UserDataAdmin)