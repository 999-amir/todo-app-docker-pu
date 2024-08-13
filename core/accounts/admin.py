from django.contrib import admin
from .models import CostumeUser, ProfileModel
from django.contrib.auth.models import Group
from .forms import CostumeUserCreationForm, CostumeUserChangeForm
from django.contrib.auth.admin import UserAdmin
from todo.admin import TodoInline


class CostumeUserAdmin(UserAdmin):
    form = CostumeUserChangeForm
    add_form = CostumeUserCreationForm

    list_display = (
        "email",
        "is_active",
        "is_verify",
        "is_admin",
        "last_login",
    )
    list_filter = ("is_active", "is_verify", "is_admin")
    fieldsets = (
        ("USER", {"fields": ("email", "password")}),
        (
            "USER-PERMISSIONS",
            {"fields": ("is_active", "is_verify", "is_admin")},
        ),
        ("DATE", {"fields": ("last_login", "updated", "created")}),
    )
    add_fieldsets = (
        ("CREATE-USER", {"fields": ("email", "password_1", "password_2")}),
    )
    search_fields = ("email",)
    ordering = ("email", "last_login", "created")
    filter_horizontal = ()
    readonly_fields = ("last_login", "updated", "created")


admin.site.unregister(Group)
admin.site.register(CostumeUser, CostumeUserAdmin)


@admin.register(ProfileModel)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "f_name", "l_name")
    fieldsets = (
        (
            "USER-INFORMATION",
            {"fields": ("user", "f_name", "l_name", "description")},
        ),
        ("DATE", {"fields": ("updated", "created")}),
    )
    search_fields = ("f_name", "l_name")
    ordering = ("l_name", "user")
    readonly_fields = ("created", "updated")
    inlines = (TodoInline,)
