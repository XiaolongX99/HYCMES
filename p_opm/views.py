# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render,reverse,render_to_response
from django.contrib import auth,messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.core.mail import send_mail,send_mass_mail,EmailMultiAlternatives 
from django.conf import settings
from django.db import connection

# Create your views here.
"""
def foxmail():
	send_mail('HYC|MES测试，请勿回复！', 'MES系统邮箱测试.', 'gc17@hyc-system.com',['gc17@hyc-system.com'], fail_silently=False)
	print('OK!')
#message1 = ('Subject here', 'Here is the message', 'from@example.com', ['first@example.com', 'other@example.com'])
#message2 = ('Another Subject', 'Here is another message', 'from@example.com', ['second@test.com']) 
#send_mass_mail((message1, message2), fail_silently=False)
"""

def opm(request,mds):
    userCHNname =request.user.first_name
    useremail =request.user.email
    username =request.user.username
        
    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    mcode='03'
    sql1="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and left(code,2)='" + mcode + "' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and left(code,2)='" + mcode + "'"
    paths=connection.cursor().execute(sql1).fetchall()

    if mds=='home':      
        connection.close
        return HttpResponse(get_template('tpopm/opm0.html').render(locals()))  
    elif mds == 'skill':
        connection.close
        return HttpResponse(get_template('tpopm/opm1.html').render(locals())) 
    elif mds == 'group':
        connection.close
        return HttpResponse(get_template('tpopm/opm2.html').render(locals())) 
    elif mds == 'slp':
        connection.close
        return HttpResponse(get_template('tpopm/opm3.html').render(locals())) 
    elif mds == 'data':
        connection.close
        return HttpResponse(get_template('tpopm/opm4.html').render(locals())) 
    elif mds == 'performance':
        connection.close
        return HttpResponse(get_template('tpopm/opm5.html').render(locals())) 
    elif mds == 'review':
        connection.close
        return HttpResponse(get_template('tpopm/opm6.html').render(locals())) 
    elif mds == 'project':
        connection.close
        return HttpResponse(get_template('tpopm/opm7.html').render(locals())) 
    elif mds == 'task':
        connection.close
        return HttpResponse(get_template('tpopm/opm8.html').render(locals())) 
    elif mds == 'query':
        connection.close
        return HttpResponse(get_template('tpopm/opm9.html').render(locals())) 
    else:
        connection.close
        return HttpResponse(get_template('index.html').render(locals())) 