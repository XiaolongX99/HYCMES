# -*- coding:utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from p_mes.models import SumReport
from django.db import connection
from django.db.models import Avg,Sum,Count
import time,datetime,json,pyodbc

# 日期转换
def timestr(str,tf):
    tsm=int(time.mktime(time.strptime(str,"%Y-%m-%d"))) + (tf*24*3600)
    return time.strftime("%Y-%m-%d",time.localtime(tsm))

#json自定义编码
class MyEncoder(json.JSONEncoder):  
    def default(self, obj):  
        if isinstance(obj, bytes):  
            return str(obj, encoding='utf-8');  
        elif isinstance(obj,pyodbc.Row):
            return str(list(obj)[0])     
        return json.JSONEncoder.default(self, obj) 

#SQL转JSON
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row))for row in cursor.fetchall()]


#战情资讯 
@login_required
@csrf_exempt
def dashboard(request):
    userCHNname =request.user.first_name
    username =request.user.username 

    #局部刷新
    if  request.is_ajax(): 
        content={}    
        dep=request.POST.get('dep')
        cell=request.POST.get('cell')
        std=request.POST.get('std')
        etd=request.POST.get('etd')
        dst=request.POST.get('dst')
        sle=request.POST.get('sle')
        if len(etd)==0:
            etd='2018-01-01'
            std='2018-01-01'
            std2='2018-01-01'
        std2=timestr(etd,-28)
        if (std2>std):
            std2=std
        if dst=='Weekly':
            sql2="select datepart(wk,WorkingDate) as WorkingDate,cast(sum(CompleteQty) as int) as FG,cast(sum(PQ) as int) as PQ,cast(cast(avg(UPPH) as numeric(8,2)) as varchar(8)) as UPPH,cast(avg(URT)*100 as int) as URT,cast(avg(PPM) as int) as PPM,cast(100*avg(FCY) as int) as FCY,cast(avg(Efficiency)*100 as int) as EFY,cast(avg(Productivity)*100 as int) as ACR from p_mes_sumreport where PL='"+ dep +"' and WorkingDate between '"+ std2 +"' and '"+ etd +"' group by datepart(wk,WorkingDate) order by datepart(wk,WorkingDate)" 
            sql3="select datepart(wk,WorkingDate) as WorkingDate,cast(sum(CompleteQty) as int) as FG,cast(sum(PQ) as int) as PQ,cast(cast(avg(UPPH) as numeric(8,2)) as varchar(8)) as UPPH,cast(avg(URT)*100 as int) as URT,cast(avg(PPM) as int) as PPM,cast(100*avg(FCY) as int) as FCY,cast(avg(Efficiency)*100 as int) as EFY,cast(avg(Productivity)*100 as int) as ACR from p_mes_sumreport where Cell='"+ cell +"' and WorkingDate between '"+ std2 +"' and '"+ etd +"' group by datepart(wk,WorkingDate) order by datepart(wk,WorkingDate)" 
        elif dst=='Monthly':
            sql2="select month(WorkingDate) as WorkingDate,cast(sum(CompleteQty) as int) as FG,cast(sum(PQ) as int) as PQ,cast(cast(avg(UPPH) as numeric(8,2)) as varchar(8)) as UPPH,cast(avg(URT)*100 as int) as URT,cast(avg(PPM) as int) as PPM,cast(100*avg(FCY) as int) as FCY,cast(avg(Efficiency)*100 as int) as EFY,cast(avg(Productivity)*100 as int) as ACR from p_mes_sumreport where PL='"+ dep +"' and WorkingDate between '"+ std2 +"' and '"+ etd +"' group by month(WorkingDate) order by month(WorkingDate)" 
            sql3="select month(WorkingDate) as WorkingDate,cast(sum(CompleteQty) as int) as FG,cast(sum(PQ) as int) as PQ,cast(cast(avg(UPPH) as numeric(8,2)) as varchar(8)) as UPPH,cast(avg(URT)*100 as int) as URT,cast(avg(PPM) as int) as PPM,cast(100*avg(FCY) as int) as FCY,cast(avg(Efficiency)*100 as int) as EFY,cast(avg(Productivity)*100 as int) as ACR from p_mes_sumreport where Cell='"+ cell +"' and WorkingDate between '"+ std2 +"' and '"+ etd +"' group by month(WorkingDate) order by month(WorkingDate)" 
        else:
            sql2="select right(convert(varchar(12),WorkingDate,112),4) as WorkingDate,cast(sum(CompleteQty) as int) as FG,cast(sum(PQ) as int) as PQ,cast(cast(avg(UPPH) as numeric(8,2)) as varchar(8)) as UPPH,cast(avg(URT)*100 as int) as URT,cast(avg(PPM) as int) as PPM,cast(100*avg(FCY) as int) as FCY,cast(avg(Efficiency)*100 as int) as EFY,cast(avg(Productivity)*100 as int) as ACR from p_mes_sumreport where PL='"+ dep +"' and WorkingDate between '"+ std2 +"' and '"+ etd +"' group by WorkingDate order by WorkingDate" 
            sql3="select right(convert(varchar(12),WorkingDate,112),4) as WorkingDate,cast(sum(CompleteQty) as int) as FG,cast(sum(PQ) as int) as PQ,cast(cast(avg(UPPH) as numeric(8,2)) as varchar(8)) as UPPH,cast(avg(URT)*100 as int) as URT,cast(avg(PPM) as int) as PPM,cast(100*avg(FCY) as int) as FCY,cast(avg(Efficiency)*100 as int) as EFY,cast(avg(Productivity)*100 as int) as ACR from p_mes_sumreport where Cell='"+ cell +"' and WorkingDate between '"+ std2 +"' and '"+ etd +"' group by WorkingDate order by WorkingDate" 

        if sle=='1':
        #by dep
            sql="select b.name as cell  from p_admin_department a inner join p_admin_department b on a.code=b.parent_id where b.category='C' and a.name='" + dep + "' order by  b.name"
            sql5="select case when len(FailureMode)=0 then 'NA' else FailureMode end as FM,sum(FailQty) as Qty from MES2017.dbo.v_FQC_Detail where Qdate between '"+ std2 +"' and '"+ etd +"' and PL='" + dep + "'  and PPM>0 group by FailureMode order by sum(FailQty) desc"
            cells=dictfetchall(connection.cursor().execute(sql))
            DQ=SumReport.objects.filter(PL='' + dep + '',WorkingDate__range=('' + std + '', ''+etd+'')).values('PL').annotate(FG=Sum('CompleteQty'),PQ=Sum('PQ'),UPPH=Avg('UPPH'),URT=Avg('URT'),PPM=Avg('PPM'),FCY=Avg('FCY'),ACR=Avg('Productivity'),EFY=Avg('Efficiency')).values('UPPH','FCY','PPM','URT','ACR','EFY','FG','PQ')
        else:
            if sle=='3':
                #update datesum to mes2018 
                mes_refresh="exec P_ReportSum '"+ std +"','"+ etd +"'" 
                connection.cursor().execute(mes_refresh)
        #by cell,std,etd
            if cell=='CellSUM':
                sql5="select case when len(FailureMode)=0 then 'NA' else FailureMode end as FM,sum(FailQty) as Qty from MES2017.dbo.v_FQC_Detail where Qdate between '"+ std2 +"' and '"+ etd +"' and PL='" + dep + "'  and PPM>0 group by FailureMode order by sum(FailQty) desc"
                DQ=SumReport.objects.filter(PL='' + dep + '',WorkingDate__range=('' + std + '', ''+etd+'')).values('PL').annotate(FG=Sum('CompleteQty'),PQ=Sum('PQ'),UPPH=Avg('UPPH'),URT=Avg('URT'),PPM=Avg('PPM'),FCY=Avg('FCY'),ACR=Avg('Productivity'),EFY=Avg('Efficiency')).values('UPPH','FCY','PPM','URT','ACR','EFY','FG','PQ')
            else:
                sql5="select case when len(FailureMode)=0 then 'NA' else FailureMode end as FM,sum(FailQty) as Qty from MES2017.dbo.v_FQC_Detail where Qdate between '"+ std2 +"' and '"+ etd +"' and Cell='" + cell + "'  and PPM>0 group by FailureMode order by sum(FailQty) desc"
                DQ=SumReport.objects.filter(Cell='' + cell + '',WorkingDate__range=('' + std + '', ''+etd+'')).values('Cell').annotate(FG=Sum('CompleteQty'),PQ=Sum('PQ'),UPPH=Avg('UPPH'),URT=Avg('URT'),PPM=Avg('PPM'),FCY=Avg('FCY'),ACR=Avg('Productivity'),EFY=Avg('Efficiency')).values('UPPH','FCY','PPM','URT','ACR','EFY','FG','PQ')
                sql2=sql3
            cells="CellSUM" 
        #cellsum
        sql1="select Cell,cast(sum(CompleteQty) as int) as FG,cast(sum(PQ) as int) as PQ,cast(cast(avg(UPPH) as numeric(8,2)) as varchar(8)) as UPPH,cast(avg(URT)*100 as int) as URT,cast(avg(PPM) as int) as PPM,cast(100*avg(FCY) as int) as FCY,cast(avg(Efficiency)*100 as int) as EFY,cast(avg(Productivity)*100 as int) as ACR from p_mes_sumreport where PL='"+ dep +"' and WorkingDate between '"+ std +"' and '"+ etd +"' group by Cell"           
        sql4="select tcode,cast(tucl as varchar(12)) as ucl,cast(tlcl as varchar(12)) as lcl from p_mes_deptarget a left join p_admin_department b on dep_id=b.code where name='"+ dep +"'"
        cellsum=dictfetchall(connection.cursor().execute(sql1))
        datesum=dictfetchall(connection.cursor().execute(sql2))
        targetsum=dictfetchall(connection.cursor().execute(sql4))
        fqcfmsum=dictfetchall(connection.cursor().execute(sql5))
        connection.close
        
            
        if DQ is not None:
            try:              
                content['EFY']=('%d %%' % (100*float(dict(list(DQ)[0])['EFY'])))
                content['URT']=('%d %%' % (100*float(dict(list(DQ)[0])['URT'])))
                content['ACR']=('%d %%' % (100*float(dict(list(DQ)[0])['ACR'])))                
                content['FG']=('%d' % float(dict(list(DQ)[0])['FG']))
                content['PQ']=('%d' % float(dict(list(DQ)[0])['PQ']))
                content['UPPH']=('%.2f' % float(dict(list(DQ)[0])['UPPH']))
                content['PPM']=('%d' % float(dict(list(DQ)[0])['PPM']))
                content['FCY']=('%d %%' % (100*float(dict(list(DQ)[0])['FCY'])))
            except:
                pass
        content['cells']=cells 
        content['cellsum']=cellsum
        content['datesum']=datesum
        content['targetsum']=targetsum
        content['fqcfmsum']=fqcfmsum 
       
        return JsonResponse(content)  
        
    #首次加载
    else:
        sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
        menus=connection.cursor().execute(sql0).fetchall()

        
        sql="select a.name from p_admin_department a left join p_admin_profile_department b on  a.code=b.department_id where profile_id='" + username + "' and category='P'" 
        deps=connection.cursor().execute(sql).fetchall()
        if len(deps):
            dept= deps[0].name
        else:
            template = get_template('index.html')
            return HttpResponse(template.render(locals()))

        sql="select b.name from p_admin_department a inner join p_admin_department b on a.code=b.parent_id where b.category='C' and a.name='" + dept + "' order by b.name"
        cells=connection.cursor().execute(sql).fetchall()
        connection.close
        startdate=(datetime.date.today()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        enddate=(datetime.date.today()+datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
        template = get_template('pages/dashboard.html')
        return HttpResponse(template.render(locals()))   


#子报表查询
@login_required
@csrf_exempt
def dashboardetail(request):
    pass
