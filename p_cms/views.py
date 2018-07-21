# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect,render,render_to_response
from django.template.loader import get_template
from django.db import connection
from django.db.models import Avg,Sum,Count
import time,datetime,json,pyodbc,math,xlwt,xlrd
from p_mes.views import dictfetchall
from django.db import models
from xlwt import Workbook


@login_required
def cms(request):
    #url = request.get_full_path()

    userCHNname =request.user.first_name
    username =request.user.username
    
    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    mcode='11'
    sql1="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and left(code,2)='" + mcode + "' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and left(code,2)='" + mcode + "'"
    paths=connection.cursor().execute(sql1).fetchall()

    sql2="select a.code,a.name from p_admin_department a left join p_admin_profile_department b on  a.code=b.department_id where profile_id='" + username + "' and category='P'" 
    deps=connection.cursor().execute(sql2).fetchall()
    if len(deps):
        dept= deps[0].code
    else:
        template = get_template('index.html')
        return HttpResponse(template.render(locals()))
    
    sql3="select b.code,b.name as cell from p_admin_department a inner join p_admin_department b on a.code=b.parent_id where b.category='C' and a.code='" + dept + "' order by b.code"
    cells=connection.cursor().execute(sql3).fetchall()
    
    sql4="select opcode,opcode+'-'+opname as operation from p_pdm_productline_operation LEFT JOIN p_pdm_operation on operation_id=opcode where productline_id='" + dept + "'"
    operations=connection.cursor().execute(sql4).fetchall()
    
    sql5="select top 1 ERP from p_pdm_productline a left join p_admin_department b on a.PL_id=b.code where b.code='" + dept + "'"
    ERPS=connection.cursor().execute(sql5).fetchall()

    sql6="select groupcode,groupdesc from p_opm_group where dep_id='"+ dept +"'"
    groups=connection.cursor().execute(sql6).fetchall()

    connection.close
    return HttpResponse(get_template('tpcms/cms0.html').render(locals()))              



