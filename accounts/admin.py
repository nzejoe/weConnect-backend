from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import UserFollower


User = get_user_model()


class FollowersInline(admin.StackedInline):
    model = UserFollower
    extra = 0
    fk_name = "follower"


class AccountAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name',
                    'last_name', 'gender', 'is_active']
    readonly_fields = ('date_joined', 'last_login',)
    fieldsets = ()

    list_filter = ('username',)
    filter_horizontal = ()
    inlines = [FollowersInline, ]


admin.site.register(User, AccountAdmin)
