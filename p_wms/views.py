# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect,render,reverse,render_to_response
from django.contrib import auth,messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.db import connection

def wms(request,mds):
    userCHNname =request.user.first_name
    useremail =request.user.email
    username =request.user.username  
    
    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    mcode='06'
    sql1="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and left(code,2)='" + mcode + "' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and left(code,2)='" + mcode + "'"
    paths=connection.cursor().execute(sql1).fetchall()

    if mds=='home':      
        connection.close
        return HttpResponse(get_template('tpwms/wms0.html').render(locals()))    
    elif mds == 'warehouse':
        connection.close
        return HttpResponse(get_template('tpwms/wms1.html').render(locals())) 
    elif mds == 'location':
        connection.close
        return HttpResponse(get_template('tpwms/wms2.html').render(locals())) 
    elif mds == 'plan':
        connection.close
        return HttpResponse(get_template('tpwms/wms3.html').render(locals())) 
    elif mds == 'quatity':
        connection.close
        return HttpResponse(get_template('tpwms/wms4.html').render(locals())) 
    elif mds == 'leadtime':
        connection.close
        return HttpResponse(get_template('tpwms/wms5.html').render(locals())) 
    elif mds == 'iqc':
        connection.close
        return HttpResponse(get_template('tpwms/wms6.html').render(locals())) 
    elif mds == 'resource':
        connection.close
        return HttpResponse(get_template('tpwms/wms7.html').render(locals())) 
    elif mds == 'task':
        connection.close
        return HttpResponse(get_template('tpwms/wms8.html').render(locals())) 
    elif mds == 'query':
        connection.close
        return HttpResponse(get_template('tpwms/wms9.html').render(locals())) 
    else:
        connection.close
        return HttpResponse(get_template('index.html').render(locals())) 