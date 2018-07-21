# -*- coding:utf-8 -*-
#p_admin module
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect,render
from django.contrib import auth,messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from p_admin.forms import LoginForm,RegisterForm,LockForm
from p_admin.models import department,module
from django.db import connection
from django.db.models import Avg,Sum,Count
import time,datetime,json,pyodbc

#Home主页
@login_required
def index(request, pid=None, del_pass=None):
    userCHNname =request.user.first_name
    useremail =request.user.email
    username =request.user.username

    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    connection.close
    return HttpResponse(get_template('index.html').render(locals())) 

#锁定 
@csrf_exempt   
def lock(request):
    return render(request,'pages/lock.html')

#解锁
@csrf_exempt
def unlock(request):
    lock_name =request.user.username
    print(lock_name)
    if request.method == 'POST':
        lock_form = LockForm(request.POST)
        if lock_form.is_valid():
            lock_password=request.POST['password'].strip() 
            print(login_password)           
            user = authenticate(username=lock_name, password=lock_password)          

            if user is not None:
                return redirect('/')
        else:
            return HttpResponse(get_template('pages/lock.html').render(locals())) 
    else:
        lock_form = LoginForm() 
    
    return HttpResponse(get_template('pages/lock.html').render(locals())) 


#忘记密码
@csrf_exempt    
def reminder(req):
    return render(req,'pages/reminder.html')


#注册
@csrf_exempt
def register(request):
    context = {}
    form = RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():		
            username=form.cleaned_data["username"]
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            user=User.objects.create_user(username,email,password)
            user.first_name=first_name
            user.last_name=last_name
            user.is_active=0
            user.save()
            return render(request, 'pages/login.html', context)
        return render(request, 'pages/register.html', context)
    return render(request, 'pages/register.html', context)

    def clean_username(self):
        users = auth.authenticate(username = username)
        if not users:
            context['userExit']=True
            return HttpResponse("用户已被使用！")

    def clean_email(self):
        emails = auth.authenticate(email = email)
        if not emails:
            context['emailsExit']=True
            return render(req, 'pages/register.html', context)

#登陆
@csrf_exempt
def login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login_name=request.POST['username'].strip()
            login_password=request.POST['password']
            #print(login_name,login_password)
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    messages.add_message(request, messages.SUCCESS, '成功登录')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, '账号尚未启用')
            else:
                messages.add_message(request, messages.WARNING, '登录失败')
        else:
            messages.add_message(request, messages.INFO,'请检查输入内容')
    else:
        login_form = LoginForm()
    template = get_template('pages/login.html')
    return HttpResponse(template.render(locals()))

#登出 
@csrf_exempt   
def logout(req):
    #清理cookie里保存username
    auth.logout(req)
    return redirect('/login/')



@login_required
def profile(request,mds):
    userCHNname =request.user.first_name
    username =request.user.username
    
    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    mcode='13'
    sql1="select distinct code,name,url,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and left(code,2)='" + mcode + "' UNION select DISTINCT code,name,url,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.id where user_id='" + username + "' and left(code,2)='" + mcode + "'"
    paths=connection.cursor().execute(sql1).fetchall()

    sql2="select a.code,a.name from p_admin_department a left join p_admin_profile_department b on  a.code=b.department_id where profile_id='" + username + "' and category<>'C'" 
    deps=connection.cursor().execute(sql2).fetchall()
    if len(deps):
        dept= deps[0].code
    else:
        template = get_template('index.html')
        return HttpResponse(template.render(locals()))
    
    if mds=='home':
        connection.close
        return HttpResponse(get_template('tpadm/adm0.html').render(locals()))              
    elif mds == 'setting': 
        connection.close
        return HttpResponse(get_template('tpadm/adm1.html').render(locals()))  
    elif mds == 'tasks':
        connection.close
        return HttpResponse(get_template('tpadm/adm2.html').render(locals())) 
    elif mds == 'messages':
        connection.close
        return HttpResponse(get_template('tpadm/adm3.html').render(locals()))   
    elif mds == 'organization':
        connection.close
        return HttpResponse(get_template('tpadm/adm4.html').render(locals()))   
    elif mds == 'HR':
        connection.close
        return HttpResponse(get_template('tpadm/adm5.html').render(locals()))   
    elif mds == 'spc':
        connection.close
        return HttpResponse(get_template('tpadm/adm6.html').render(locals()))   
    elif mds == 'cim':
        connection.close
        return HttpResponse(get_template('tpadm/adm7.html').render(locals()))      
    elif mds == 'query':
        connection.close
        return HttpResponse(get_template('tpadm/adm8.html').render(locals()))  
    else:
        connection.close
        return HttpResponse(get_template('index.html').render(locals()))   