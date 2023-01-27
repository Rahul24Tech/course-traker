from django.contrib import admin
from members.models import *
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("bio",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "content")
    search_fields = ("name", "email")
    list_per_page = 40
    fieldsets = (
        (
            None,
            {
                "fields": ("name", "phone", "email", "content"),
            },
        ),
    )
