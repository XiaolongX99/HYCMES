#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.forms.models import modelform_factory
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import get_template
from django.shortcuts import render_to_response,redirect,render
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from p_wkf.logger import Log; log = Log('goflow.apptools.views')
from p_wkf.notification import send_mail
from p_wkf.forms import *
from p_wkf.models import *

@login_required
def wkf(request):
    userCHNname =request.user.first_name
    username =request.user.username
    
    sql0="select distinct code,name,url,icon,parent_id,level from p_admin_module left join p_admin_profile_module on code=module_id where profile_id='" + username + "' and level='1' UNION select DISTINCT code,name,url,icon,parent_id,level  from p_admin_module a left join p_admin_module_group b on code=module_id left join auth_user_groups c on b.group_id=c.group_id where user_id='" + username + "' and level='1'"
    menus=connection.cursor().execute(sql0).fetchall()

    mcode='12'
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

    #print(sql1,deps,paths,cells)

    #if mds=='home':
    connection.close
    return HttpResponse(get_template('tpwkf/wkf0.html').render(locals()))  


@login_required
def start_application(request, app_label=None, model_name=None, process_name=None, instance_label=None,
                       template=None, template_def='goflow/start_application.html',
                       form_class=None, redirect='home', submit_name='action',
                       ok_value='OK', cancel_value='Cancel', extra_context={}):
    '''
    generic handler for application that enters a workflow.
    
    parameters:
    
    app_label, model_name
        model linked to workflow instance (deprecated)
    process_name
        default: same name as app_label
    instance_label
        default: process_name + str(object)
    template 
        default: 'start_%s.html' % app_label
    template_def
        used if template not found - default: 'goflow/start_application.html'
    form_class
        default: django.forms.models.modelform_factory(model)
    '''
    if not process_name:
        process_name = app_label
    try:
        Process.objects.check_can_start(process_name, request.user)
    except Exception as v:
        return HttpResponse(str(v))
    
    #if not instance_label: instance_label = '%s-%s' % (app_label, model_name)
    if not template: template = 'start_%s.html' % app_label
    if not form_class:
        model = models.get_model(app_label, model_name)
        form_class = modelform_factory(model)
        is_form_used = False
    else:
        is_form_used = True
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        submit_value = request.POST[submit_name]
        if submit_value == cancel_value:
            return HttpResponseRedirect(redirect)
        
        if submit_value == ok_value and form.is_valid():
            try:
                if is_form_used:
                    ob = form.save(user=request.user, data=request.POST)
                else:
                    ob = form.save()
            except Exception as v:
                if is_form_used:
                    raise
                    log.error("the save method of the form must accept parameters user and data")
                else:
                    log.error("forme save error: %s", str(v))
            
            if ob:
                priority = int(form.cleaned_data['priority'])
                ProcessInstance.objects.start(process_name, request.user, ob, instance_label, priority=priority)
            
            return HttpResponseRedirect(redirect)
    else:
        form = form_class()
        # precheck
        form.pre_check(user=request.user)
    context = {'form': form, 'process_name':process_name,
               'submit_name':submit_name, 'ok_value':ok_value, 'cancel_value':cancel_value}
    context.update(extra_context)
    return render_to_response((template, template_def), context,
                              RequestContext(request))


@login_required
def default_app(request, id, template='goflow/default_app.html', redirect='../../', submit_name='action'):
    '''
    default application, used for prototyping workflows.
    '''
    submit_values = ('OK', 'Cancel')
    id = int(id)
    if request.method == 'POST':
        data = request.POST.copy()
        workitem = WorkItem.objects.get_safe(id, user=request.user)
        inst = workitem.instance
        ob = inst.wfobject()
        form = DefaultAppForm(data, instance=ob)
        if form.is_valid():
            #data = form.cleaned_data
            submit_value = request.POST[submit_name]
            
            workitem.instance.condition = submit_value
            
            workitem.instance.save()
            ob = form.save(workitem=workitem, submit_value=submit_value)
            #ob.comment = data['comment']
            #ob.save(workitem=workitem, submit_value=submit_value)
            
            workitem.complete(request.user)
            return HttpResponseRedirect(redirect)
    else:
        workitem = WorkItem.objects.get_safe(id, user=request.user)
        inst = workitem.instance
        ob = inst.wfobject()
        form = DefaultAppForm(instance=ob)
        # add header with activity description, submit buttons dynamically
        if workitem.activity.split_mode == 'x':
            tlist = workitem.activity.transition_inputs.all()
            if tlist.count() > 0:
                submit_values = []
                for t in tlist:
                    submit_values.append( _cond_to_button_value(t.condition) )
    
    return render_to_response(template, {'form': form,
                                         'activity':workitem.activity,
                                         'workitem':workitem,
                                         'instance':inst,
                                         'history':inst.wfobject().history,
                                         'submit_values':submit_values,},
                              context_instance=RequestContext(request))


def _cond_to_button_value(cond):
    '''
    extract "a value" from "instance.condition=='a value'"
    used to generate buttons on default application
    '''
    import re
    s = cond.strip()
    try:
        m = re.match("instance.condition *== *(.*)", s)
        s = m.groups()[0]
        s = s.strip('"').strip("'")
    except Exception:
        pass
    return s


@login_required
def edit_model(request, id, form_class, cmp_attr=None,template=None, template_def='goflow/edit_model.html', title="",
               redirect='home', submit_name='action', ok_values=('OK',), save_value=None, cancel_value='Cancel',
               extra_context={}):
    '''
    generic handler for editing a model.
    
    parameters:

    id
        workitem id (required)
    form_class
        model form based on goflow.apptools.forms.BaseForm (required)
    cmp_attr
        edit obj.cmp_attr attribute instead of obj - default=None
    template 
        default: 'goflow/edit_%s.html' % model_lowercase
    template_def
        used if template not found - default: 'goflow/edit_model.html'
    title
        default=""
    redirect
        default='home'
    submit_name
        name for submit buttons - default='action'
    ok_values
        submit buttons values - default=('OK',)
    save_value
        save button value - default='Save'
    cancel_value
        cancel button value - default='Cancel'
    extra_context
        default={}
    '''
    if not template: template = 'goflow/edit_%s.html' % form_class._meta.model._meta.object_name.lower()
    model_class = form_class._meta.model
    workitem = WorkItem.objects.get_safe(int(id), user=request.user)
    instance = workitem.instance
    activity = workitem.activity
    
    obj = instance.wfobject()
    obj_context = obj
    # objet composite intermédiaire
    if cmp_attr:
        obj = getattr(obj, cmp_attr)
    
    template = override_app_params(activity, 'template', template)
    redirect = override_app_params(activity, 'redirect', redirect)
    submit_name = override_app_params(activity, 'submit_name', submit_name)
    ok_values = override_app_params(activity, 'ok_values', ok_values)
    cancel_value = override_app_params(activity, 'cancel_value', cancel_value)

    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        submit_value = request.POST[submit_name]
        if submit_value == cancel_value:
            return HttpResponseRedirect(redirect)
        
        if form.is_valid():
            if (submit_value == save_value):
                # just save
                #ob = form.save()
                try:
                    ob = form.save(workitem=workitem, submit_value=submit_value)
                except Exception as v:
                    raise Exception(str(v))
                return HttpResponseRedirect(redirect)
            
            if submit_value in ok_values:
                # save and complete activity
                #ob = form.save()
                try:
                    ob = form.save(workitem=workitem, submit_value=submit_value)
                except Exception as v:
                    raise Exception(str(v))
                instance.condition = submit_value
                instance.save()
                workitem.complete(request.user)
                return HttpResponseRedirect(redirect)
    else:
        form = form_class(instance=obj)
        # precheck
        form.pre_check(obj_context, user=request.user)
    
    context = {  'form': form, 'object':obj, 'object_context':obj_context,
                 'instance':instance, 'workitem':workitem,
                 'submit_name':submit_name, 'ok_values':ok_values,
                 'save_value':save_value, 'cancel_value':cancel_value,
                 'title':title}
    context.update(extra_context)
    return render_to_response((template, template_def), context,
                              context_instance=RequestContext(request))


@login_required
def view_application(request, id, template='goflow/view_application.html', redirect='home', title="",
               submit_name='action', ok_values=('OK',), cancel_value='Cancel',
               extra_context={}):
    '''
    generic handler for a view application.
    
    useful for a simple view or a complex object edition.

    parameters:
    
    id
        workitem id (required)
    template 
        default: 'goflow/view_application.html'
    redirect
        default='home'
    title
        default=""
    submit_name
        name for submit buttons - default='action'
    ok_values
        submit buttons values - default=('OK',)
    cancel_value
        cancel button value - default='Cancel'
    extra_context
        default={}
    '''
    workitem = WorkItem.objects.get_safe(int(id), user=request.user)
    instance = workitem.instance
    activity = workitem.activity
    
    obj = instance.wfobject()
    
    template = override_app_params(activity, 'template', template)
    redirect = override_app_params(activity, 'redirect', redirect)
    submit_name = override_app_params(activity, 'submit_name', submit_name)
    ok_values = override_app_params(activity, 'ok_values', ok_values)
    cancel_value = override_app_params(activity, 'cancel_value', cancel_value)

    if request.method == 'POST':
        submit_value = request.POST[submit_name]
        if submit_value == cancel_value:
            return HttpResponseRedirect(redirect)
        
        if submit_value in ok_values:
            instance.condition = submit_value
            instance.save()
            workitem.complete(request.user)
            return HttpResponseRedirect(redirect)
        
    context = {  'object':obj,'instance':instance, 'workitem':workitem,
                 'submit_name':submit_name,
                 'ok_values':ok_values,'cancel_value':cancel_value,
                 'title':title}
    context.update(extra_context)
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


@login_required
def choice_application(request, id, template='goflow/view_application_image.html', redirect='home', title="Choice",
               submit_name='image', cancel_action='cancel', extra_context={}):
    '''
    a view to make a choice within image buttons.
    
    - actions are generated from instances conditions of outer transitions
    - the activity split_mode must be xor
    - actions are rendered with images
    - actions are mapped to images with ImageButton instances

    parameters:
    
    id
        workitem id (required)
    template 
        default: 'goflow/view_application_image.html'
    redirect
        default='home'
    title
        default='Choice'
    submit_name
        name for submit buttons - default='image'
    cancel_value
        cancel button value - default='Cancel'
    extra_context
        default={}
    '''
    workitem = WorkItem.objects.get_safe(int(id), user=request.user)
    activity = workitem.activity
    if activity.split_mode != 'xor':
        raise Exception('choice_application: split_mode xor required')
    list_trans = Transition.objects.filter(input=activity)
    ok_values = []
    for t in list_trans:
        if ImageButton.objects.filter(action=t.condition).count() == 0:
            raise Exception('no ImageButton for action [%s]' % t.condition)
        ok_values.append(t.condition)
        
    return view_application(request, id, template, redirect, title,
               submit_name, ok_values, cancel_action, extra_context)

def sendmail(workitem, subject='goflow.apptools sendmail message', template='goflow/app_sendmail.txt'):
    '''send a mail notification to the workitem user.
    
    parameters:
    
    subject
        default='goflow.apptools sendmail message'
    template
        default='goflow/app_sendmail.txt'
    '''
    send_mail(workitems=(workitem,), user=workitem.user, subject=subject, template=template)

def override_app_params(activity, name, value):
    '''
    usage: param = _override_app_params(activity, 'param', param)
    '''
    try:
        if not activity.app_param:
            return value
        dicparams = eval(activity.app_param)
        if dicparams.has_key(name):
            return dicparams[name]
    except Exception as v:
        log.error('_override_app_params %s %s - %s', activity, name, v)
    return value


@login_required
def app_env(request, action, id, template=None):
    """
    creates/removes unit test environment for applications.
    
    a process named "test_[app]" with one activity
    a group with appropriate permission
    """
    app = Application.objects.get(id=int(id))
    rep = 'Nothing done.'
    if action == 'create':
        app.create_test_env(user=request.user)
        rep = 'test env created for app %s' % app.url
    if action == 'remove':
        app.remove_test_env()
        rep = 'test env removed for app %s' % app.url
    
    rep += '<hr><p><b><a href=../../../>return</a></b>'
    return HttpResponse(rep)

@login_required
def test_start(request, id, template='goflow/test_start.html'):
    """
    starts test instances.
    
    for a given application, with its unit test environment, the user
    choose a content-type then generates unit test process instances
    by cloning existing content-type objects (**Work In Progress**).
    """
    app = Application.objects.get(id=int(id))
    context = {}
    if request.method == 'POST':
        submit_value = request.POST['action']
        if submit_value == 'Create':
            ctype = ContentType.objects.get(id=int(request.POST['ctype']))
            model = ctype.model_class()
            for inst in model.objects.all():
                # just objects without link to a workflow instance
                if ProcessInstance.objects.filter(
                    content_type__pk=ctype.id,
                    object_id=inst.id
                ).count() > 0:
                    continue
                inst.id = None
                inst.save()
                #TODO: convert this to method
                ProcessInstance.objects.start(
                #start_instance(
                            process_name='test_%s' % app.url,
                            user=request.user, item=inst, 
                            title="%s test instance for app %s" % (
                                ctype.name, app.url
                            ))
            request.user.message_set.create(message='test instances created')
        return HttpResponseRedirect('../..')
    form = ContentTypeForm()
    context['form'] = form
    return render_to_response(template, context)


@login_required
def image_update(request):
    '''
    Import Image instances as Icon instances.
    
    GoFlow can use local images as well as http distant images.
    For a genericity reason, local images (Image) are obtained as
    Icon images by their url; this view is useful to wrap all local
    images in a row. 
    '''
    rep = '<h1>Update Icons from Images</h1>'
    for im in Image.objects.all():
        if Icon.objects.filter(url__endswith=str(im.url)).count() == 0:
            ic, created = Icon.objects.get_or_create(category='local-'+im.category, url=im.url())
            if created: rep += '<br> %s added ' % im.url()
    rep += '<hr><p><b><a href=../>return</a></b>'
    return HttpResponse(rep)
    
    


def index(request, template='workflow/index.html', extra_context={}):
    """workflow dashboard handler.    
    template context contains following objects:
    - user
    - processes
    - roles    
    other applications (ie runtime or apptools) should fill extra_context.
    """
    #print('index request\n\n\n')
    me = request.user
    roles = Group.objects.all()
    processes = Process.objects.all()
    # optional package (ugly design)
    try:
        from goflow.apptools.models import DefaultAppModel
        obinstances = DefaultAppModel.objects.all()
    except Exception:
        obinstances = None
    
    context = {'processes':processes, 'roles':roles}
    context.update(extra_context)
    return render(request, template, context)

def debug_switch_user(request, username, password, redirect=None):
    """
    fast user switch for test purpose.
    
    parameters:
    
    username
        username
    password
        password
    redirect
        redirection url
    
    *FOR TEST ONLY*
    
    see template tag switch_users.
    """
    logout(request)
    #return HttpResponseRedirect(redirect)
    if not redirect:
        redirect = request.META['HTTP_REFERER']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(redirect)
        else:
            return HttpResponse('user is not active')
    else:
        return HttpResponse('authentication failed')

def userlist(request, template):
    '''
    not used
    '''
    return HttpResponse('user page.')


def process_dot(request, id, template='goflow/process.dot'):
    """graphviz generator (**Work In Progress**).
    (**Work In Progress**)
    
    id process id
    template graphviz template
    
    context provides: process, roles, activities
    """
    process = Process.objects.get(id=int(id))
    context = {
               'process': process,
               'roles': ({'name':'role1', 'color':'red'},),
               'activities': Activity.objects.filter(process=process)
               }
    return render_to_response(template, context)

def cron(request=None):
    """
    (**Work In Progress**)
    TODO: move to instances ?
    """
    for t in Transition.objects.filter(condition__contains='workitem.timeout'):
        workitems = WorkItem.objects.filter(
            activity=t.input).exclude(status='complete')
        for wi in workitems:
            wi.forward(timeout_forwarding=True)
    
    if request:
        request.user.message_set.create(message="cron has run.")
        if request.META.has_key('HTTP_REFERER'):
            url = request.META['HTTP_REFERER']
        else:
            url = 'home/'
        return HttpResponseRedirect(url)








@login_required
def mywork(request, template='goflow/mywork.html'):
    '''
    displays the worklist of the current user.
    
    parameters:
    
    template
        default:'goflow/mywork.html'
    '''
    workitems = WorkItem.objects.list_safe(user=request.user, noauto=True)
    return render_to_response(template, {'workitems':workitems},
                              RequestContext(request))

@login_required
def otherswork(request, template='goflow/otherswork.html'):
    worker = request.GET['worker']
    workitems = WorkItem.objects.list_safe(username=worker, noauto=False)
    return render_to_response(template, {'worker':worker, 'workitems':workitems},
                              RequestContext(request))

@login_required
def instancehistory(request, template='goflow/instancehistory.html'):
    id = int(request.GET['id'])
    inst = ProcessInstance.objects.get(pk=id)
    return render_to_response(template, {'instance':inst},
                              RequestContext(request))

@login_required
def myrequests(request, template='goflow/myrequests.html'):
    inst_list = ProcessInstance.objects.filter(user=request.user)
    return render_to_response(template, {'instances':inst_list},
                              RequestContext(request))

@login_required
def activate(request, id):
    '''
    activates and redirect to the application.
    
    parameters:
    
    id
        workitem id
    '''
    id = int(id)
    workitem = WorkItem.objects.get_safe(id=id, user=request.user)
    workitem.activate(request.user)
    return _app_response(workitem)

@login_required
def complete(request, id):
    '''
    redirect to the application.
    
    parameters:
    
    id
        workitem id
    '''
    id = int(id)
    workitem = WorkItem.objects.get_safe(id=id, user=request.user)
    return _app_response(workitem)

def _app_response(workitem):
    id = workitem.id
    activity = workitem.activity
    if not activity.process.enabled:
        return HttpResponse('process %s disabled.' % activity.process.title)
    
    
    if activity.kind == 'subflow':
        # subflow
        sub_workitem = workitem.start_subflow()
        return _app_response(sub_workitem)
    
    # no application: default_app
    if not activity.application:
        url = '../../../default_app'
        return HttpResponseRedirect('%s/%d/' % (url, id))
    
    if activity.kind == 'standard':
        # standard activity
        return HttpResponseRedirect(activity.application.get_app_url(workitem))
    return HttpResponse('completion page.')


def graph(request, id, template='goflow/graphics/graph.html'):
    processes = Process.objects.all()
    graph = Graph.objects.get(id=(int(id)))
    return render_to_response(template, {'processes':processes, 'graph':graph})

def graph_save(request, id):
    # save positions TODO
    return HttpResponseRedirect('..')