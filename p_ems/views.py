# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render,reverse,render_to_response
from django.contrib import auth,messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.db import connection

def ems(request,mds):
    userCHNname =request.user.first_name
    useremail =request.user.email
    username =request.user.username

    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    mcode='07'
    sql1="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and left(code,2)='" + mcode + "' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and left(code,2)='" + mcode + "'"
    paths=connection.cursor().execute(sql1).fetchall()

    if mds=='home':      
        connection.close
        return HttpResponse(get_template('tpems/ems0.html').render(locals()))    
    elif mds == 'equipment':
        connection.close
        return HttpResponse(get_template('tpems/ems1.html').render(locals())) 
    elif mds == 'category':
        connection.close
        return HttpResponse(get_template('tpems/ems2.html').render(locals())) 
    elif mds == 'tpmitem':
        connection.close
        return HttpResponse(get_template('tpems/ems3.html').render(locals())) 
    elif mds == 'maintance':
        connection.close
        return HttpResponse(get_template('tpems/ems4.html').render(locals())) 
    elif mds == 'trouble':
        connection.close
        return HttpResponse(get_template('tpems/ems5.html').render(locals())) 
    elif mds == 'report':
        connection.close
        return HttpResponse(get_template('tpems/ems6.html').render(locals())) 
    elif mds == 'resource':
        connection.close
        return HttpResponse(get_template('tpems/ems7.html').render(locals())) 
    elif mds == 'task':
        connection.close
        return HttpResponse(get_template('tpems/ems8.html').render(locals())) 
    elif mds == 'query':
        connection.close
        return HttpResponse(get_template('tpems/ems9.html').render(locals())) 
    else:
        connection.close
        return HttpResponse(get_template('index.html').render(locals())) 