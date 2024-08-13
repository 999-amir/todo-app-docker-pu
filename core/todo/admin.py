from django.contrib import admin
from .models import TodoModel


class TodoInline(admin.TabularInline):
    model = TodoModel
    can_delete = True
    extra = 0


@admin.register(TodoModel)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("profile", "level", "is_done", "created", "dead_end")
    list_filter = ("is_done",)
    fieldsets = (
        ("USER", {"fields": ("profile",)}),
        ("TASK", {"fields": ("level", "is_done", "job")}),
        ("DATE", {"fields": ("dead_end", "updated", "created")}),
    )
    readonly_fields = ("updated", "created")
    ordering = ("dead_end", "created")
