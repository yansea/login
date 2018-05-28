from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib
import re

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# Create your views here.


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login',None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            useremail = login_form.cleaned_data['useremail']
            password = login_form.cleaned_data['password']
            if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",useremail) != None:
                message = "邮箱格式错误！"
                return render(request, 'login/register.html', locals())
            try:
                user = models.User.objects.get(email=useremail)
                if user.password == hash_code(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_email'] = user.email
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            useremail = register_form.cleaned_data['useremail']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            nickname = register_form.cleaned_data['nickname']
            sex = register_form.cleaned_data['sex']
            if not re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",useremail) != None:
                message = "邮箱格式错误！"
                return render(request, 'login/register.html', locals())
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            if len(password1)<6 or len(password1)>18:  # 用户名唯一
                message = '密码长度为6-18位！'
                return render(request, 'login/register.html', locals())
            if not re.search('^(?![A-Z]+$)(?![a-z]+$)(?!\d+$)(?![\W_]+$)\S{6,}$',password1):
                message = '密码必须为数字和字母的组合！'
                return render(request, 'login/register.html', locals())

            else:
                same_name_user = models.User.objects.filter(email=useremail)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User()
                new_user.email = useremail
                new_user.password = hash_code(password1)
                new_user.nickname = nickname
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())



def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_email']
    return redirect("/index/")



def alter(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有修改密码一说
        return redirect("/index/")
    if request.method == "POST":
        alter_form = forms.AlterForm(request.POST)
        message = "请检查填写的内容！"
        if alter_form.is_valid():  # 获取数据

            password1 = alter_form.cleaned_data['password1']
            password2 = alter_form.cleaned_data['password2']

            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/alter.html', locals())
            if len(password1) < 6 or len(password1) > 18:  # 用户名唯一
                message = '密码长度为6-18位！'
                return render(request, 'login/alter.html', locals())
            if not re.search('^(?![A-Z]+$)(?![a-z]+$)(?!\d+$)(?![\W_]+$)\S{6,}$', password1):
                message = '密码必须为数字和字母的组合！'
                return render(request, 'login/alter.html', locals())

            else:

                # 当一切都OK的情况下，修改用户密码
                alter_useremail= request.session['user_email']
                user=models.User.objects.get(email=alter_useremail)
                user.password = hash_code(password1)
                user.save()
                request.session.flush()
            return redirect('/login/')  # 自动跳转到登录页面
    alter_form = forms.AlterForm()
    return render(request, 'login/alter.html', locals())