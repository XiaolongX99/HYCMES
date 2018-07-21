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
from p_sfm.models import dispatch
from django.db import models
#from xlwt import Workbook


@login_required
def sfm(request,mds):
    userCHNname =request.user.first_name
    username =request.user.username
    
    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    mcode='01'
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

    #print(sql1)

    if mds=='home':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm0.html').render(locals()))              
    elif mds == 'dispatch': 
        connection.close
        return HttpResponse(get_template('tpsfm/sfm1.html').render(locals()))  
    elif mds == 'transfer':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm2.html').render(locals())) 
    elif mds == 'workinghours':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm3.html').render(locals()))   
    elif mds == 'material':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm4.html').render(locals()))   
    elif mds == 'qc':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm5.html').render(locals()))   
    elif mds == 'spc':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm6.html').render(locals()))   
    elif mds == 'cim':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm7.html').render(locals()))      
    elif mds == 'query':
        connection.close
        return HttpResponse(get_template('tpsfm/sfm8.html').render(locals()))  
    else:
        connection.close
        return HttpResponse(get_template('index.html').render(locals()))      


#派工作业
@login_required
@csrf_exempt
def dispatch(request,fun):
    content={} 

    #ajax
    if  request.is_ajax(): 
        if fun == 'dep':               
            dep=request.POST.get('dep')
            sql1="select b.code,b.name as cell from p_admin_department a inner join p_admin_department b on a.code=b.parent_id where b.category='C' and a.code='" + dep + "' order by b.code"
            sql2="select top 1 ERP from p_pdm_productline where PL_id='" + dep + "'"
            content['cells']=dictfetchall(connection.cursor().execute(sql1))
            content['erps']=dictfetchall(connection.cursor().execute(sql2))
            connection.close         
            return JsonResponse(content)

        elif fun == 'cell':
            cell=request.POST.get('cell')
            sql1="select top 1 ERP from p_pdm_productline where PL_id='" + cell + "'"
            sql2="select opcode,opname as operation from p_pdm_productline_operation LEFT JOIN p_pdm_operation on operation_id=opcode where productline_id='" + cell + "'"
            content['erps']=dictfetchall(connection.cursor().execute(sql1))
            content['operations']=dictfetchall(connection.cursor().execute(sql2))
            connection.close                      
            return JsonResponse(content)

        elif fun == 'po':  
            operation=request.POST.get('operation')
            po=request.POST.get('po')
            sle=request.POST.get('sle')      
            if sle=='true':
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA011<>'Y' and TA021='"+ operation +"'  order by TA028,TA002"
            else:
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA011='Y' and TA021='"+ operation +"' order by TA028,TA002"
            sql2="select TC015 as crm,UDF04 as mrm,UDF05 as qrm,UDF06 as prm from ERP.HYC.dbo.COPTC where TC002=ltrim(rtrim('"+ po +"'))"
            content['poids']=dictfetchall(connection.cursor().execute(sql1))
            content['poinfos']=dictfetchall(connection.cursor().execute(sql2))
            connection.close
            #print(sql1)
            return JsonResponse(content)            

        elif fun == 'poid':
            dep=request.POST.get('dep')
            cell=request.POST.get('cell')
            operation=request.POST.get('operation')
            po=request.POST.get('po')
            poid=request.POST.get('poid')
            sle=request.POST.get('sle')
            if sle=='true':
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA028=ltrim(rtrim('"+ poid +"')) and TA011<>'Y' and TA021='"+ operation +"' order by TA028,TA002"
            else:
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA028=ltrim(rtrim('"+ poid +"')) and TA011='Y' and TA021='"+ operation +"' order by TA028,TA002"
            content['wos']=dictfetchall(connection.cursor().execute(sql1))
            #print(sql1)
            connection.close
            return JsonResponse(content) 

        elif fun == 'wo':
            dep=request.POST.get('dep')
            wo=request.POST.get('wo')
            sle=request.POST.get('sle')
            if sle=='true':
                sql1="select TA001 as category,TA002 as WO,ltrim(rtrim(TA006)) as item,TA003 as startdate,TA004 as enddate,TA011 as states,cast(TA015 as int) as startqty,cast(TA017 as int) as completeqty,cast(TA015-TA017 as int) as wodif,TA021 as operation,TA027 as PO,TA028 as POID,TA029 as woinfo,TA034 as itemdesc,TA035 as itemspec from ERP.HYC.dbo.MOCTA where TA001='5110' and TA002=ltrim(rtrim('"+ wo +"'))"
            else:
                sql1="select TA001 as category,TA002 as WO,ltrim(rtrim(TA006)) as item,TA009 as startdate,TA010 as enddate,TA011 as states,cast(TA015 as int) as startqty,cast(TA017 as int) as completeqty,cast(TA015-TA017 as int) as wodif,TA021 as operation,TA027 as PO,TA028 as POID,TA029 as woinfo,TA034 as itemdesc,TA035 as itemspec from ERP.HYC.dbo.MOCTA where TA001='5110' and TA002=ltrim(rtrim('"+ wo +"'))"             
            sql2="select TB001 as wt,TB002 as wo,TB003 as component,cast(TB004 as numeric(12,0)) as required,cast(TB005 as numeric(12,0)) as issued,case when qty is null then 0 else qty end as released,TB011 as ComTy,TB012 as Comdesc,TB013 as Comsepc from ERP.HYC.dbo.MOCTB \
            left join (select component,cast(sum(qty) as numeric(12,0)) as qty from p_sfm_dispatch left join p_sfm_dispatchbom on dpid=dpid_id where wo=ltrim(rtrim('"+ wo +"')) group by component)cqt on TB003=component \
            where TB001='5110' and TB002=ltrim(rtrim('"+ wo +"')) and left(TB003,1)<>4 and TB011=1"
            sql3="select sn,lotsize,cell,b.dispatch,b.updatetime from p_sfm_dispatchsn b left join p_sfm_dispatch a on dpid=dpid_id where wo=ltrim(rtrim('"+ wo +"')) order by sn"
            sql4="select case when sum(startqty) is null then 0 else sum(startqty) end as SQ from p_sfm_dispatch where wo=ltrim(rtrim('"+ wo +"'))"
            content['woinfos']=dictfetchall(connection.cursor().execute(sql1))
            content['boms']=dictfetchall(connection.cursor().execute(sql2))
            content['snlist']=dictfetchall(connection.cursor().execute(sql3))
            content['SQ']=dictfetchall(connection.cursor().execute(sql4))
            #print(sql1)
            connection.close
            return JsonResponse(content) 

        elif fun == 'item':
            dep=request.POST.get('dep')
            item=request.POST.get('item')

            sql1="select operation_id,pcode,pname,labor,step from p_pdm_itempcode left join p_pdm_pcode on pcode=pcode_id where item_id=(select case when itemgroup_id is null then item  else itemgroup_id end as item from p_pdm_item where item='"+ item +"') order by operation_id,step"
            sql2="select parameter_id,spec,UCL,CL,LCL from p_pdm_itempcode a left join p_pdm_itempcodespec b on a.id=b.route_id where parameter_id is not null and item_id=(select case when itemgroup_id is null then item  else itemgroup_id end as item from p_pdm_item where item='"+ item +"') order by step"
            sql3="select case when MG004 is null then MG003 else MG004 end as CPN from ERP.HYC.dbo.COPMG where MG002=ltrim(rtrim('"+ item +"'))"
            content['routings']=dictfetchall(connection.cursor().execute(sql1))
            content['parameters']=dictfetchall(connection.cursor().execute(sql2))
            content['cuspns']=dictfetchall(connection.cursor().execute(sql3))
            #print(sql2)
            
            connection.close
            return JsonResponse(content) 

        elif fun == 'sn':
            sn=request.POST.get('sn')
            sql1="select * from p_sfm_dispatchsn where sn=ltrim(rtrim('"+ sn +"'))"
            obj=connection.cursor().execute(sql1).fetchall()
            if len(obj) == 0:
                content['sns'] = 0
            else:
                content['sns'] = 1
            return JsonResponse(content)

        elif fun == 'printsn':             
            item=request.POST.get('item')
            sns=eval(request.POST.get('sns'))
            msn=[]

            for i in sns:
                sql1="select sn,lotsize,PL,cell,operation,po,poid,item,wo,startdate,completedate,a.states from p_sfm_dispatchsn a left join p_sfm_dispatch b on dpid_id=dpid where sn='"+ i['sn'] +"'"
                #print(sql1)
                msn+=dictfetchall(connection.cursor().execute(sql1))  #单个产品
                

            content['msns']=msn

            sql2="select operation_id,step,pcode,pname from p_pdm_itempcode a left join p_pdm_pcode b on a.pcode_id=b.pcode where item_id=(select case when itemgroup_id is null then item  else itemgroup_id end as item from p_pdm_item where item='"+ item +"')  ORDER BY operation_id,step"
            content['routs']=dictfetchall(connection.cursor().execute(sql2)) 
            #print(sql2)
            
            sql3="select distinct step,pcode_id,parameter_id,b.spec,UCL,CL,LCL,pmproperty from p_pdm_itempcode a left join p_pdm_itempcodespec b on a.id=b.route_id left join p_pdm_pcode c on a.pcode_id=c.pcode left join p_pdm_parameter e on parameter_id=parameter where parameter_id is not null and item_id=(select case when itemgroup_id is null then item  else itemgroup_id end as item from p_pdm_item where item='"+ item +"') order by step"
            content['params']=dictfetchall(connection.cursor().execute(sql3)) 
            #print(sql3)

            #print(content)
            connection.close          
            return JsonResponse(content) 

        elif fun=='dispatch':
            dep=request.POST.get('dep')
            cell=request.POST.get('cell')
            operation=request.POST.get('operation')
            po=request.POST.get('po')
            poid=request.POST.get('poid')
            wo=request.POST.get('wo')
            item=request.POST.get('item')
            trid=request.POST.get('trid')
            lotsize=int(request.POST.get('lotsize'))
            lotqty=int(request.POST.get('lotqty'))
            dispatchqty=int(request.POST.get('dispatchqty'))
            sntype=request.POST.get('sntype')
            dg1=time.strftime('%Y-%m-%d',time.strptime(request.POST.get('dg1'),'%Y%m%d'))
            dg2=time.strftime('%Y-%m-%d',time.strptime(request.POST.get('dg2'),'%Y%m%d'))
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            boms=eval(request.POST.get('boms'))
            routs=eval(request.POST.get('routs'))
            #print(routs)

#自动编码
            if sntype=='true':

                if dispatchqty == 0 or lotqty==0 :
                    exit()
                else :
                    lotsize=dispatchqty // lotqty   #整除数
                    lts=dispatchqty % lotqty        #余数
                    if lts != 0 :
                        lotsize += math.ceil(lts / lotqty)
                        lts=dispatchqty % lotsize
                        if lts==0:
                            lotqty=lotqty-1

                #print(dispatchqty,lotqty,lotsize,lts)

                if dispatchqty==0 or lotqty==0 or lotsize==0 :
                    exit()

                sql1="select max(sn) as snt from p_sfm_dispatch left join p_sfm_dispatchsn on dpid=dpid_id where po=ltrim(rtrim('"+ po +"')) and poid=ltrim(rtrim('"+ poid +"'))"
                snt=connection.cursor().execute(sql1).fetchall()
                #print(sql1)
                
                try:
                    if type(snt[0][0])!='NoneType':
                        snt=snt[0].snt
                        snstart=int(snt[-3:])
                    else:
                        snstart=0
                except:
                    snstart=0

                #content['dispatch']={'dispatchqty':dispatchqty,'lotqty':lotqty,'lotsize':lotsize}

                sql2="insert into p_sfm_dispatch values('" + trid + "','" + dep +"','"+ cell +"','"+ operation +"','" + po +"','"+ poid +"','"+ item +"','"+ wo +"','"+ str(dispatchqty) +"','0','"+ dg1 +"','"+ dg2 +"','0','"+ nowTime +"')"
                connection.cursor().execute(sql2)
                #print(sql2)
                
                #整数批
                if lts==0:
                    for i in range(snstart+1,snstart+1+lotqty):
                        sn=po + str(poid[-2:]) + ('000'+ str(i))[-3:]
                        #print(sn,lotsize)
                        sql3="insert into p_sfm_dispatchsn(sn,lotsize,states,updatetime,dpid_id,dispatch)values('"+ sn +"','"+ str(lotsize) +"','1','"+ nowTime +"','"+ trid +"','"+ operation +"')"
                        #print(sql3)
                        connection.cursor().execute(sql3)
                        
                else:
                    for i in range(snstart+1,snstart+lotqty):
                        sn=po + str(poid[-2:]) + ('000'+ str(i))[-3:]
                        sql3="insert into p_sfm_dispatchsn(sn,lotsize,states,updatetime,dpid_id,dispatch)values('"+ sn +"','"+ str(lotsize) +"','1','"+ nowTime +"','"+ trid +"','"+ operation +"')"
                        #print(sql3)
                        connection.cursor().execute(sql3)

                    #零数批
                    sn=po + str(poid[-2:]) + ('000'+ str(snstart+lotqty))[-3:]
                    #print(sn,lts)
                    sql4="insert into p_sfm_dispatchsn(sn,lotsize,states,updatetime,dpid_id,dispatch)values('"+ sn +"','"+ str(lts) +"','1','"+ nowTime +"','"+ trid +"','"+ operation +"')"
                    connection.cursor().execute(sql4)
                    #print(sql4)
                
                sql5="select sn,lotsize,cell,b.dispatch,b.updatetime from p_sfm_dispatchsn b left join p_sfm_dispatch a on dpid=dpid_id where wo=ltrim(rtrim('"+ wo +"')) order by sn"
                content['snlist']=dictfetchall(connection.cursor().execute(sql5))
                #print(sql5)

                for i in boms:
                    sql6="insert into p_sfm_dispatchbom values('"+ str(i['component']) +"','"+ str(i['qty']) +"','"+ str(i['lot']) +"','1','"+ nowTime + "','"+ trid + "')"
                    #print(sql6)
                    connection.cursor().execute(sql6)
                    
                
                for j in routs:
                    sql9="insert into p_sfm_dispatchrouting values('"+ str(j['step']) +"','"+ str(j['states']) +"','"+ nowTime + "','"+ trid + "','" + str(j['pcode']) + "')"
                    connection.cursor().execute(sql9)

#手动输入SN
            else:

                sns=eval(request.POST.get('sns'))

                sql2="insert into p_sfm_dispatch values('" + trid + "','" + dep +"','"+ cell +"','"+ operation +"','" + po +"','"+ poid +"','"+ item +"','"+ wo +"','"+ str(dispatchqty) +"','0','"+ dg1 +"','"+ dg2 +"','0','"+ nowTime +"')"
                connection.cursor().execute(sql2)

                for j in sns:                    
                    sql7="insert into p_sfm_dispatchsn(sn,lotsize,states,updatetime,dpid_id,dispatch)values('"+ str(j['sn']) +"','"+ str(j['qty']) +"','1','"+ nowTime +"','"+ trid +"','"+ operation +"')"
                    if len(str(j['sn']))!=0:
                        #print(sql7)
                        connection.cursor().execute(sql7)                

                for i in boms:
                    sql6="insert into p_sfm_dispatchbom values('"+ str(i['component']) +"','"+ str(i['qty']) +"','"+ str(i['lot']) +"','1','"+ nowTime + "','"+ trid + "')"
                    connection.cursor().execute(sql6)

                for j in routs:
                    sql8="insert into p_sfm_dispatchrouting values('"+ str(j['step']) +"','"+ str(j['states']) +"','"+ nowTime + "','"+ trid + "','" + str(j['pcode']) + "')"                
                    connection.cursor().execute(sql8)


            content['dispatch']={'dispatchqty':dispatchqty,'lotqty':lotqty,'lotsize':lotsize}
            connection.close
            return JsonResponse(content) 


#移转作业
@login_required
@csrf_exempt
def transfer(request,fun):
    content={} 

    #ajax
    if  request.is_ajax(): 

        if fun == 'dep':               
            dep=request.POST.get('dep')
            sql1="select b.code,b.name as cell from p_admin_department a inner join p_admin_department b on a.code=b.parent_id where b.category='C' and a.code='" + dep + "' order by b.code"
            sql2="select top 1 ERP from p_pdm_productline where PL_id='" + dep + "'"
            sql3="select groupcode,groupdesc from p_opm_group where dep_id='"+ dep +"'"
            sql4="select opcode,opname as operation from p_pdm_productline_operation LEFT JOIN p_pdm_operation on operation_id=opcode where productline_id='" + dep + "'"
            content['cells']=dictfetchall(connection.cursor().execute(sql1))
            content['erps']=dictfetchall(connection.cursor().execute(sql2))
            content['groups']=dictfetchall(connection.cursor().execute(sql3))
            content['inoperations']=dictfetchall(connection.cursor().execute(sql4))
            connection.close         
            return JsonResponse(content)

        elif fun == 'cell':
            cell=request.POST.get('cell')
            sql1="select top 1 ERP from p_pdm_productline where PL_id='" + cell + "'"
            sql2="select opcode,opname as operation from p_pdm_productline_operation LEFT JOIN p_pdm_operation on operation_id=opcode where productline_id='" + cell + "'"
            sql3="select groupcode,groupdesc from p_opm_group_cell left join p_opm_group on groupcode=group_id where department_id='" + cell + "'"
            content['erps']=dictfetchall(connection.cursor().execute(sql1))
            content['operations']=dictfetchall(connection.cursor().execute(sql2))
            content['groups']=dictfetchall(connection.cursor().execute(sql3))
            connection.close                       
            return JsonResponse(content)

        elif fun == 'operation':
            operation=request.POST.get('operation')
            sql1="select pcode,pname,labor from  p_pdm_pcode where operation_id='" + operation + "'"
            sql2="select failcode,faildesc from p_sfm_modelfail where operation_id='" + operation + "'"
            sql3="select process_id from p_pdm_operation_process where operation_id='" + operation + "'"

            content['processs']=dictfetchall(connection.cursor().execute(sql1))
            content['failmodels']=dictfetchall(connection.cursor().execute(sql2))
            content['operationpros']=dictfetchall(connection.cursor().execute(sql3))
            #print(content['failmodels'])
            connection.close                      
            return JsonResponse(content)

        elif fun == 'group':
            group=request.POST.get('group')
            cell=request.POST.get('cell')
            operation=request.POST.get('operation')
            sql1="select jn,name,AMT from p_opm_org left join p_opm_group on groupcode=group_id left join p_admin_organization on jn=jn_id where operation_id='" + operation + "' and cell_id='" + cell + "' and group_id='" + group + "'"
            content['operators']=dictfetchall(connection.cursor().execute(sql1))
            connection.close                     
            return JsonResponse(content)

        elif fun == 'po':  
            erp=request.POST.get('erp')
            po=request.POST.get('po')
            sle=request.POST.get('sle')    
            if sle=='true':
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA011<>'Y' and TA021='"+ erp +"'  order by TA028,TA002"
            else:
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA011='Y' and TA021='"+ erp +"' order by TA028,TA002"
            sql2="select TC015 as crm,UDF04 as mrm,UDF05 as qrm,UDF06 as prm from ERP.HYC.dbo.COPTC where TC002=ltrim(rtrim('"+ po +"'))"
            #print(sql1)
            content['poids']=dictfetchall(connection.cursor().execute(sql1))
            content['poinfos']=dictfetchall(connection.cursor().execute(sql2))
            connection.close
            return JsonResponse(content)            

        elif fun == 'poid':
            dep=request.POST.get('dep')
            cell=request.POST.get('cell')
            erp=request.POST.get('erp')
            po=request.POST.get('po')
            poid=request.POST.get('poid')
            sle=request.POST.get('sle')
            if sle=='true':
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA028=ltrim(rtrim('"+ poid +"')) and TA011<>'Y' and TA021='"+ erp +"' order by TA028,TA002"
            else:
                sql1="select distinct TA002 as wo,TA028 as poid from ERP.HYC.dbo.MOCTA where TA001='5110' and TA027=ltrim(rtrim('"+ po +"')) and TA028=ltrim(rtrim('"+ poid +"')) and TA011='Y' and TA021='"+ erp +"' order by TA028,TA002"
            content['wos']=dictfetchall(connection.cursor().execute(sql1))
            connection.close
            return JsonResponse(content) 

        elif fun == 'wo':
            dep=request.POST.get('dep')
            wo=request.POST.get('wo')
            operation=request.POST.get('operation')
            sle=request.POST.get('sle')
            #print(wo,operation)
            if sle=='true':
                sql1="select TA001 as category,TA002 as WO,ltrim(rtrim(TA006)) as item,TA003 as startdate,TA004 as enddate,TA011 as states,cast(TA015 as int) as startqty,cast(TA017 as int) as completeqty,cast(TA015-TA017 as int) as wodif,TA021 as operation,TA027 as PO,TA028 as POID,TA029 as woinfo,TA034 as itemdesc,TA035 as itemspec from ERP.HYC.dbo.MOCTA where TA001='5110' and TA002=ltrim(rtrim('"+ wo +"'))"
            else:
                sql1="select TA001 as category,TA002 as WO,ltrim(rtrim(TA006)) as item,TA009 as startdate,TA010 as enddate,TA011 as states,cast(TA015 as int) as startqty,cast(TA017 as int) as completeqty,cast(TA015-TA017 as int) as wodif,TA021 as operation,TA027 as PO,TA028 as POID,TA029 as woinfo,TA034 as itemdesc,TA035 as itemspec from ERP.HYC.dbo.MOCTA where TA001='5110' and TA002=ltrim(rtrim('"+ wo +"'))"          
            sql2="select TB001 as wt,TB002 as wo,TB003 as component,cast(TB004 as numeric(12,0)) as required,cast(TB005 as numeric(12,0)) as issued,case when qty is null then 0 else qty end as released,TB011 as ComTy,TB012 as Comdesc,TB013 as Comsepc from ERP.HYC.dbo.MOCTB \
            left join (select component,cast(sum(qty) as numeric(12,0)) as qty from p_sfm_dispatch left join p_sfm_dispatchbom on dpid=dpid_id where wo=ltrim(rtrim('"+ wo +"')) group by component)cqt on TB003=component \
            where TB001='5110' and TB002=ltrim(rtrim('"+ wo +"')) and left(TB003,1)<>4 and TB011=1"
            sql4="select case when sum(startqty) is null then 0 else sum(startqty) end as SQ from p_sfm_dispatch where wo=ltrim(rtrim('"+ wo +"'))"
            sql3="select wo,cell,sn,lotsize,dispatch,distates,updatetime,cast(case when sum(wip) is null then lotsize else sum(wip) end as int )as wip\
                    from(select b.wo,b.cell,a.sn,lotsize,dispatch,a.states as distates,a.updatetime,case when d.states=0 then -(c.passqty+c.failqty) else c.passqty end as wip\
                    from p_sfm_dispatchsn a \
                    left join p_sfm_dispatch b on dpid=dpid_id  \
                    left join p_sfm_transfersn c on a.sn=c.sn and a.dispatch=c.operation and a.states=c.states\
                    left join p_sfm_transfer d on c.trid_id=d.trid where b.wo=ltrim(rtrim('"+ wo +"')) and dispatch=ltrim(rtrim('"+ operation +"')))snwip\
                    group by wo,cell,sn,lotsize,dispatch,distates,updatetime"

            #print(sql3)

            content['woinfos']=dictfetchall(connection.cursor().execute(sql1))
            content['boms']=dictfetchall(connection.cursor().execute(sql2))
            content['snlist']=dictfetchall(connection.cursor().execute(sql3))
            content['SQ']=dictfetchall(connection.cursor().execute(sql4))
            #print(sql3)
            connection.close
            return JsonResponse(content) 

        elif fun == 'item':
            dep=request.POST.get('dep')
            item=request.POST.get('item')
            operation=request.POST.get('operation')

            sql1="select operation_id,pcode,pname,labor,step from p_pdm_itempcode left join p_pdm_pcode on pcode=pcode_id  where item_id=(select case when itemgroup_id is null then item  else itemgroup_id end as item from p_pdm_item where item='"+ item +"')  and operation_id=ltrim(rtrim('"+ operation +"')) order by step"
            sql2="select case when MG004 is null then MG003 else MG004 end as CPN from ERP.HYC.dbo.COPMG where MG002=ltrim(rtrim('"+ item +"'))"

            content['processs']=dictfetchall(connection.cursor().execute(sql1))
            content['cuspns']=dictfetchall(connection.cursor().execute(sql2))  #客户料号
            #print(sql2)
            connection.close
            return JsonResponse(content) 

        elif fun == 'sn':
            sn=request.POST.get('sn')
            cell=request.POST.get('cell')
            operation=request.POST.get('operation')
            processs=request.POST.get('processs')
            lot=request.POST.get('lot')
            wo=request.POST.get('wo')
            item=request.POST.get('item')
            sntype=request.POST.get('sntype')

            #print(processs)

            sql1="select wo,sn,lotsize,dispatch,distates,cast(case when sum(wip) is null then lotsize else sum(wip) end as int )as wip\
                    from(select b.wo,a.sn,lotsize,dispatch,a.states as distates,case when d.states=0 then -(c.passqty+c.failqty) else c.passqty end as wip\
                    from p_sfm_dispatchsn a \
                    left join p_sfm_dispatch b on dpid=dpid_id  \
                    left join p_sfm_transfersn c on a.sn=c.sn and a.dispatch=c.operation and a.states=c.states\
                    left join p_sfm_transfer d on c.trid_id=d.trid where a.sn=ltrim(rtrim('"+ sn +"')))snwip\
                    group by wo,sn,lotsize,dispatch,distates"
            sql2="select item_id,pcode_id,parameter_id,e.spec,UCL,CL,LCL,pmproperty from p_pdm_itempcode a left join p_pdm_itempcodespec b on a.id=b.route_id left join p_pdm_pcode c on a.pcode_id=c.pcode left join p_pdm_parameter e on parameter_id=parameter where parameter_id is not null and pcode_id in "+ processs +" and item_id=(select case when itemgroup_id is null then item  else itemgroup_id end as item from p_pdm_item where item='"+ item +"')  order by pmproperty"
            #po+poid编码规则7+2
            sql3="select RIGHT(max(prsn),5) as msn from p_sfm_productsn where left(trsn_id,9)='"+ lot +"'"

            sql4="select prsn,lotsize,states from p_sfm_productsn where trsn_id='"+ sn +"'"
            #print(sql2)

            content['sns']=dictfetchall(connection.cursor().execute(sql1))
            content['parameters']=dictfetchall(connection.cursor().execute(sql2))
            content['maxsn']=dictfetchall(connection.cursor().execute(sql3))
            content['prsns']=dictfetchall(connection.cursor().execute(sql4))
           

            if content['maxsn'][0]['msn'] is None:
                content['msn']=0
            else:
                content['msn']=int(content['maxsn'][0]['msn'])

            if len(content['prsns'])==0:
                content['prsns']=0

            #print(content['msn'])

            if len(content['sns'])!=0 :
                snqty=content['sns'][0]['wip']  #单批数量
                if content['sns'][0]['dispatch']==operation and content['sns'][0]['wo']==wo :
                    content['state']=0

                elif content['sns'][0]['dispatch']==operation: 
                    content['state']=1     #工单错误！

                elif content['sns'][0]['wo']==wo :  
                    content['state']=2   #工站错误！

                else:
                    content['state']=3   #工站和工单错误！

            else:  
                content['state']=4   #无SN信息

            #print(content)
            connection.close
            return JsonResponse(content)

        elif fun == 'transfer':
            dep=request.POST.get('dep')
            cell=request.POST.get('cell')
            operation=request.POST.get('operation')
            inoperation=request.POST.get('inoperation')
            group=request.POST.get('group')
            po=request.POST.get('po')
            poid=request.POST.get('poid')
            wo=request.POST.get('wo')
            item=request.POST.get('item')
            trid=request.POST.get('trid')
 
            inputqty=int(request.POST.get('inputqty'))
            passqty=int(request.POST.get('passqty'))
            failqty=inputqty-passqty #int(request.POST.get('failqty'))    
            failmodels=request.POST.get('failmodels')
            faildesc=request.POST.get('faildesc')

            trstates=request.POST.get('trstates')      #移转状态
            distates=request.POST.get('distates')      #流程单状态    

            operators=request.POST.get('operators')
            processs=request.POST.get('processs')            

            wdate=request.POST.get('wdate')
            nowTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            boms=eval(request.POST.get('boms'))
            parameters=eval(request.POST.get('parameters'))

            pro=int(request.POST.get('pro'))    #工站参数
            sntype=request.POST.get('sntype')

            #print(boms,parameters)

            #Lot
            if sntype=='true':  
                sn=request.POST.get('sns') 

                #主移转序列
                sql1="insert into p_sfm_transfer(trid,workingdate,PL,cell,operation,groups,po,poid,item,wo,passqty,failqty,starttime,completetime,states,operatorlist,processlist,remark)\
                values('"+ trid +"','"+ wdate +"','"+ dep +"','"+ cell +"','"+ operation +"','"+ group +"','"+ po +"','"+ poid +"','"+ item +"','"+ wo +"','"+ str(passqty) +"','"+ str(failqty) +"','"+ nowTime +"','"+ nowTime +"','"+ trstates +"','"+ operators +"','"+ processs +"',null)"
                #print(sql1)  
                connection.cursor().execute(sql1)
                             
                #更新派单表
                if pro==1:
                    sql2="update p_sfm_dispatchsn set lotsize='"+ str(inputqty) +"',dispatch='"+ inoperation +"',states='"+ distates +"',updatetime='"+ nowTime +"' where sn='"+ sn +"'"
                else:
                    sql2="update p_sfm_dispatchsn set dispatch='"+ inoperation +"',states='"+ distates +"',updatetime='"+ nowTime +"' where sn='"+ sn +"'"
                #print(sql2)
                connection.cursor().execute(sql2)
                
                #移转序号
                sql3="insert into p_sfm_transfersn(sn,passqty,failqty,operation,operator,states,updatetime,trid_id)values('"+ sn +"','"+ str(passqty) +"','"+ str(failqty) +"','"+ inoperation +"','"+ operators +"','"+ distates +"','"+ nowTime +"','"+ trid +"')"
                #print(sql3)  
                connection.cursor().execute(sql3)

                #制程不良记录
                if failqty!=0:
                    sql4="insert into p_sfm_transferfail(sn,failqty,failcode,faildesc,states,updatetime,trid_id)values('"+ sn +"','"+ str(failqty) +"','"+ failmodels +"','"+ faildesc +"','1','"+ nowTime +"','"+ trid +"')"
                    connection.cursor().execute(sql4)

                #更新SN状态
                if trstates!='0':
                    sql7="update p_sfm_dispatchsn set dispatch='"+ inoperation +"' where sn='"+ sn +"'"
                    #print(sql4)
                    connection.cursor().execute(sql7)
                    sql8="update c set c.states='"+ trstates +"'  from  p_sfm_dispatchsn a left join  p_sfm_transfersn b on a.sn=b.sn and b.operation=a.dispatch and a.states=b.states left join p_sfm_transfer c on b.trid_id=c.trid where a.sn='"+ sn +"'"
                    #print(sql5)
                    connection.cursor().execute(sql8)
                    sql9="update b set b.operation='"+ inoperation +"' from  p_sfm_dispatchsn a left join  p_sfm_transfersn b on a.sn=b.sn and b.operation=a.dispatch and a.states=b.states where a.sn='"+ sn +"'"
                    #print(sql6)
                    connection.cursor().execute(sql9)   #修改同SN,States,operation未完工状态和工站


                #材料不良记录
                for i in boms:
                    sql5="insert into p_sfm_transfertracking(component,lot,failqty,faildesc,states,updatetime,trid_id)values('"+ str(i['component']) +"','"+ str(i['lot']) +"','"+ str(i['failqty']) +"','"+ str(i['faildesc']) +"','1','"+ nowTime + "','"+ trid + "')"
                    connection.cursor().execute(sql5)

                #参数记录
                for i in parameters:
                    if str(i['pvalue']) !='':
                        sql6="insert into p_sfm_transferparameter(sn,parameter,pvalue,pdesc,updatetime,trid_id)values('"+ str(i['sn']) +"','"+ str(i['parameter']) +"','"+ str(i['pvalue']) +"','"+ str(i['pdesc']) +"','"+ nowTime + "','"+ trid + "')"
                        connection.cursor().execute(sql6)
                    if sn!=str(i['sn']) and pro==1:    #派工站
                        sql6B="insert into p_sfm_productsn(prsn,lotsize,states,updatetime,trsn_id)values('"+ str(i['sn']) +"','1','1','"+ nowTime + "','"+ sn + "')"
                        try:
                            connection.cursor().execute(sql6B)
                        except:
                            pass

                #返回产品清单
                sql10="select wo,cell,sn,lotsize,dispatch,distates,updatetime,cast(case when sum(wip) is null then lotsize else sum(wip) end as int )as wip\
                    from(select b.wo,b.cell,a.sn,lotsize,dispatch,a.states as distates,a.updatetime,case when d.states=0 then -(c.passqty+c.failqty) else c.passqty end as wip\
                    from p_sfm_dispatchsn a \
                    left join p_sfm_dispatch b on dpid=dpid_id  \
                    left join p_sfm_transfersn c on a.sn=c.sn and a.dispatch=c.operation and a.states=c.states\
                    left join p_sfm_transfer d on c.trid_id=d.trid where b.wo=ltrim(rtrim('"+ wo +"')) and dispatch=ltrim(rtrim('"+ operation +"')))snwip\
                    group by wo,cell,sn,lotsize,dispatch,distates,updatetime"
                #print(sql4)
                content['snlist']=dictfetchall(connection.cursor().execute(sql10))
               
            #Batch
            else:
                sns=eval(request.POST.get('sns'))

                #主移转序列
                sql1="insert into p_sfm_transfer(trid,workingdate,PL,cell,operation,groups,po,poid,item,wo,passqty,failqty,starttime,completetime,states,operatorlist,processlist,remark)\
                values('"+ trid +"','"+ wdate +"','"+ dep +"','"+ cell +"','"+ operation +"','"+ group +"','"+ po +"','"+ poid +"','"+ item +"','"+ wo +"','"+ str(passqty) +"','"+ str(failqty) +"','"+ nowTime +"','"+ nowTime +"','"+ trstates +"','"+ operators +"','"+ processs +"',null)"
                #print(sql1)  
                connection.cursor().execute(sql1)

                for i in sns:
                    sn=str(i['sn']) 
                    PQ=int(i['sn1'])
                    FQ=int(i['sn2'])
                    FM=str(i['sn3']) 
                    FD=str(i['sn4'])
                    OP=str(i['sn5'])  
                    DSA=str(i['sn6'])   
                              
                    #更新派单表
                    if pro==1:
                        sql2="update p_sfm_dispatchsn set lotsize='"+ str(inputqty) +"',dispatch='"+ inoperation +"',states='"+ distates +"',updatetime='"+ nowTime +"' where sn='"+ sn +"'"
                    else:
                        sql2="update p_sfm_dispatchsn set dispatch='"+ inoperation +"',states='"+ distates +"',updatetime='"+ nowTime +"' where sn='"+ sn +"'"
                    #print(sql2)
                    connection.cursor().execute(sql2)
                    
                    #移转序号
                    sql3="insert into p_sfm_transfersn(sn,passqty,failqty,operation,operator,states,updatetime,trid_id)values('"+ sn +"','"+ str(PQ) +"','"+ str(FQ) +"','"+ inoperation +"','"+ OP +"','"+ DSA +"','"+ nowTime +"','"+ trid +"')"
                    #print(sql3)  
                    connection.cursor().execute(sql3)

                    #制程不良记录
                    if FQ!=0:
                        sql4="insert into p_sfm_transferfail(sn,failqty,failcode,faildesc,states,updatetime,trid_id)values('"+ sn +"','"+ str(FQ) +"','"+ FM +"','"+ FD +"','1','"+ nowTime +"','"+ trid +"')"
                        connection.cursor().execute(sql4)

                    #更新SN状态
                    if trstates!='0':
                        sql7="update p_sfm_dispatchsn set dispatch='"+ inoperation +"' where sn='"+ sn +"'"
                        #print(sql4)
                        connection.cursor().execute(sql7)
                        sql8="update c set c.states='"+ trstates +"'  from  p_sfm_dispatchsn a left join  p_sfm_transfersn b on a.sn=b.sn and b.operation=a.dispatch and a.states=b.states left join p_sfm_transfer c on b.trid_id=c.trid where a.sn='"+ sn +"'"
                        #print(sql5)
                        connection.cursor().execute(sql8)
                        sql9="update b set b.operation='"+ inoperation +"' from  p_sfm_dispatchsn a left join  p_sfm_transfersn b on a.sn=b.sn and b.operation=a.dispatch and a.states=b.states where a.sn='"+ sn +"'"
                        #print(sql6)
                        connection.cursor().execute(sql9)   #修改同SN,States,operation未完工状态和工站


                #材料不良记录
                for i in boms:
                    sql5="insert into p_sfm_transfertracking(component,lot,failqty,faildesc,states,updatetime,trid_id)values('"+ str(i['component']) +"','"+ str(i['lot']) +"','"+ str(i['failqty']) +"','"+ str(i['faildesc']) +"','1','"+ nowTime + "','"+ trid + "')"
                    connection.cursor().execute(sql5)

                #参数记录
                for i in parameters:
                    if str(i['pvalue']) !='':
                        sql6="insert into p_sfm_transferparameter(sn,parameter,pvalue,pdesc,updatetime,trid_id)values('"+ str(i['sn']) +"','"+ str(i['parameter']) +"','"+ str(i['pvalue']) +"','"+ str(i['pdesc']) +"','"+ nowTime + "','"+ trid + "')"
                        connection.cursor().execute(sql6)
                    if sn!=str(i['sn']) and pro==1:    #派工站
                        sql6B="insert into p_sfm_productsn(prsn,lotsize,states,updatetime,trsn_id)values('"+ str(i['sn']) +"','1','1','"+ nowTime + "','"+ sn + "')"
                        try:
                            connection.cursor().execute(sql6B)
                        except:
                            pass


                #返回产品清单
                sql10="select wo,cell,sn,lotsize,dispatch,distates,updatetime,cast(case when sum(wip) is null then lotsize else sum(wip) end as int )as wip\
                    from(select b.wo,b.cell,a.sn,lotsize,dispatch,a.states as distates,a.updatetime,case when d.states=0 then -(c.passqty+c.failqty) else c.passqty end as wip\
                    from p_sfm_dispatchsn a \
                    left join p_sfm_dispatch b on dpid=dpid_id  \
                    left join p_sfm_transfersn c on a.sn=c.sn and a.dispatch=c.operation and a.states=c.states\
                    left join p_sfm_transfer d on c.trid_id=d.trid where b.wo=ltrim(rtrim('"+ wo +"')) and dispatch=ltrim(rtrim('"+ operation +"')))snwip\
                    group by wo,cell,sn,lotsize,dispatch,distates,updatetime"
                #print(sql4)
                content['snlist']=dictfetchall(connection.cursor().execute(sql10))


            connection.close
            return JsonResponse(content)