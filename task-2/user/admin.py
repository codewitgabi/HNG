from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["userId", "firstName", "lastName", "phone"]
    search_fields = ["firstName", "lastName"]
