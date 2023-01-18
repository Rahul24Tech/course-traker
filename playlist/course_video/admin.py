from course_video.models import *
from django.contrib import admin
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilter

# Register your models here.


@admin.register(Course)
@admin.display(description="Firm URL")
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "title",
        "playlist_url",
        "tag_list",
        "public",
        "created_at",
        "updated_at",
        "days_since_creations",
    ]
    list_filter = ("public", ("created_at", DateRangeFilter))
    search_fields = ("title",)
    list_per_page = 40
    date_hierarchy = "created_at"
    list_editable = ("public", "title")
    fieldsets = (
        (
            None,
            {
                "fields": ("author", "title", "link", "tag_list"),
            },
        ),
        (
            "Advanced Options",
            {
                "fields": ("public",),
                "description": "Option to change course from public to private",
                "classes": ("collapse",),
            },
        ),
    )

    def playlist_url(self, obj):
        return format_html("<a href='{url}' target=_blank>{url}</a>", url=obj.link)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    def get_ordering(self, request):
        if request.user.is_superuser:
            return ("title", "-created_at")
        return ("title",)

    def set_course_to_private(self, request, queryset):
        count = queryset.update(public=False)
        self.message_user(
            request, "{} course is set to private successfully".format(count)
        )

    set_course_to_private.short_description = "Mark selected course as private"


@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ("list_item", "time", "link", "author", "status")
    search_fields = ("list_item",)
    list_per_page = 40
    list_filter = ["status"]
    fieldsets = (
        (
            None,
            {
                "fields": ("list_item", "time", "link", "author"),
            },
        ),
        (
            "Advanced Options",
            {
                "fields": ("status",),
                "description": "Option to change status of per playlist",
                "classes": ("collapse",),
            },
        ),
    )
