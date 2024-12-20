from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
from django.utils.translation import gettext_lazy as _

from .models import User

# Register your models here.


class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'dir': 'ltr'})
        self.fields['password1'].widget.attrs.update({'dir': 'ltr'})
        self.fields['password2'].widget.attrs.update({'dir': 'ltr'})


class UserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'dir': 'ltr'})


class AdminPasswordChangeForm(AdminPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'dir': 'ltr'})
        self.fields['password2'].widget.attrs.update({'dir': 'ltr'})


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2'),
            },
        ),
    )
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = (
        'groups',
        'user_permissions',
    )
