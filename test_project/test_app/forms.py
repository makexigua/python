# 用户注册功能
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post

class UserRegisterForm(UserCreationForm):   # 用户注册表单
    email = forms.EmailField()

    class Meta:   # 表单元信息
        model = User   # 这个表单关联的是Django内置的User模型
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):   # 直接与模型关联的表单类
    class Meta:
        model = Post
        fields = ['title', 'content']