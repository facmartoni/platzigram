"""User admin classes"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin"""

    list_display = ('pk', 'user', 'phone_number', 'website', 'picture')
    list_display_links = ('user', 'pk')
    list_editable = ('phone_number', 'website', 'picture')
    search_fields = ('user__email', 'user__first_name',
                     'user__last_name', 'phone_number', 'user__username')
    list_filter = ('created', 'modified', 'user__is_active', 'user__is_staff')
    fieldsets = (
        ('Profile', {
            'fields': (
                ('user', 'picture'),
            ),
        }),
        ('Extra Info', {
            'fields': (
                ('website', 'phone_number'),
                ('biography'),
            ),
        }),
        ('Metadata', {
            'fields': (
                ('created', 'modified')
            ),
        })
    )
    readonly_fields = ('created', 'modified')


class ProfileInline(admin.StackedInline):
    """Profile inline admin for users"""

    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'


class UserAdmin(BaseUserAdmin):
    """Add profile admin to base user admin"""

    inlines = (ProfileInline,)
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
    )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
