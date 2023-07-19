from django.contrib import admin
from .models import MyUser
from django.contrib.auth.admin import UserAdmin


class MyUserAdmin(UserAdmin):
    search_fields = ('email', 'first_name')
    search_help_text = 'Search is available on email and first_name'
    list_display = ('email', 'username', 'first_name')
    fieldsets = (("Info", {'fields': ('email', 'username', 'first_name', 'last_name')}),
                 ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),)
    add_fieldsets = (
        ('Login Info', {'fields': ('email', 'username', 'password1', 'password2')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    )


admin.site.register(MyUser, MyUserAdmin)
