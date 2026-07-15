from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    # 建立与 Django 自带 User 的一对一关联（自带的 User 已经保证了 username 不可重复，且自带自增 ID）
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 用户的网名，用来在各个页面显示
    nickname = models.CharField(max_length=50, verbose_name="网名")

    def __str__(self):
        return f"{self.user.username} 的个人资料 ({self.nickname})"