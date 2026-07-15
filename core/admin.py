from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile

# --- 方法一：单独管理 UserProfile 表 ---
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 在后台列表中展示：ID、网名、以及它关联的登录账户
    list_display = ('id', 'nickname', 'user')


# --- 方法二（更推荐）：把网名直接合并到自带的 User（用户）管理界面中 ---
# 这样你点击任何一个用户，就能在同一个页面直接看到并修改他的网名
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = '个人资料 (网名)'

# 重新定义 User 管理界面
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

# 注销掉系统默认的 User 注册，用我们合并了网名的自定义 UserAdmin 重新注册
admin.site.unregister(User)
admin.site.register(User, UserAdmin)