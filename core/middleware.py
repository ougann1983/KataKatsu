from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """全局登录拦截中间件"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 定义不需要登录就能访问的白名单（登录页、注册页、以及 Django 官方后台）
        exempt_urls = [
            reverse('login'),
            reverse('register'),
            '/admin/',  # 允许访问官方后台
        ]

        # 如果用户未登录，且访问的页面不在白名单内，直接拦截并重定向到登录页
        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('login')

        response = self.get_response(request)
        return response