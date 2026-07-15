from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from .models import UserProfile

def index(request):
    """首页 (已被中间件拦截)"""
    profile = getattr(request.user, 'profile', None)
    nickname = profile.nickname if profile else request.user.username
    return render(request, 'index.html', {'nickname': nickname})

def register_view(request):
    """注册页面"""
    if request.method == 'POST':
        # 💡 这里修正了：从 request.form 改为 request.POST
        username = request.POST.get('username', '').strip()
        nickname = request.POST.get('nickname', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not nickname or not password:
            messages.error(request, "所有字段均为必填项！")
            return redirect('register')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, "该账户名已被占用，请换一个。")
            return redirect('register')
            
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user, nickname=nickname)
        
        messages.success(request, "注册成功！请登录。🌸")
        return redirect('login')
        
    return render(request, 'register.html')

def login_view(request):
    """登录页面"""
    if request.method == 'POST':
        # 💡 这里同样修正了：从 request.form 改为 request.POST
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # 👑 核心改动：如果是超级管理员（王様），直接送进 Admin 后台！
            if user.is_superuser:
                messages.success(request, "欢迎回来，王様！")
                return redirect('admin:index')
                
            messages.success(request, "欢迎回来！")
            return redirect('index')
        else:
            messages.error(request, "账户或密码错误，请重试。")
            return redirect('login')
            
    return render(request, 'login.html')

def logout_view(request):
    """退出登录"""
    auth_logout(request)
    messages.info(request, "您已成功退出登录。")
    return redirect('login')