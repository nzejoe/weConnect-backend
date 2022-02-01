from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import UserFollower


User = get_user_model()


class FollowersInline(admin.StackedInline):
    model = UserFollower
    extra = 0
    fk_name = "following"
    readonly_fields = ['follower', 'created']


class AccountAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'first_name',
                    'last_name', 'gender', 'is_active']
    readonly_fields = ('date_joined', 'last_login',)
    fieldsets = ()

    list_filter = ('username',)
    filter_horizontal = ()
    inlines = [FollowersInline, ]

class FollowersAdmin(admin.ModelAdmin):
    model = UserFollower
    list_display = ['following', 'follower', 'created']


admin.site.register(User, AccountAdmin)
admin.site.register(UserFollower, FollowersAdmin)
