from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.Profile.models import CustomUser


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'email', 'mobile', 'is_active', 'status', 'project', 'is_staff', 'created_at', 'updated_at')
    search_fields = ('email', 'mobile', 'status', 'last_name')
    list_filter = ('email', 'project', 'status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('mobile', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
        ('Project info', {'fields': ('status', 'project')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser', 'project', 'status')}
         ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
