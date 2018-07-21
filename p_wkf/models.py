#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import resolve
from django.conf import settings
from django import forms
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

from p_wkf.notification import send_mail
from django.core.mail import mail_admins
from django.contrib.contenttypes import fields

from django.contrib.contenttypes.fields import GenericForeignKey

import logging
from p_wkf.logger import Log; log = Log('goflow.runtime.managers')

log = logging.getLogger('goflow.workflow.managers')


class DefaultAppModel(models.Model):
    """Default implementation object class  for process instances.
    
    When a process instance starts, the instance has to carry an
    implementation object that contains the application data. The
    specifications for the implementation class is:
    
    (nothing: now managed by generic relation)
    
    This model is used in process simulations: you don't have to define
    application in activities for this; the DefaultAppModel is used
    to keep workflow history for displaying to users.
    """
    history = models.TextField(editable=False, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return 'simulation model %s' % str(self.id)
    class Admin:
        list_display = ('__str__',)
    class Meta:
        verbose_name='1101应用'
        verbose_name_plural='1101应用'

class Image(models.Model):
    '''
    An image stored in the database
    '''
    category = models.CharField(max_length=20, null=True, blank=True, verbose_name='图形分类')
    file = models.ImageField(upload_to='images',verbose_name='图形文件')
    
    def url(self):
        return "%s%s" % (settings.MEDIA_URL, self.file)
    
    #@login_required
    def graphic(self):
        '''
        generates an *img* html tag for html rendering
        '''        
        return '<img name="image%d" src="%s">' % (self.pk, self.url())
    
    #@login_required
    def graphic_input(self):
        '''
        generates an *input* html tag with type=image for html rendering
        '''
        return '<input type=image name=icon src=%s>' % self.get_file_url()
    
    def __str__(self):
        return str(self.file)

    class Meta:
        verbose_name='1102图形'
        verbose_name_plural='1102图形'

class Icon(models.Model):
    '''
    An image accessible by an url.
    Tip: all of the "Image" objects can be imported as "Icon" from the
    admin panel.
    '''
    category = models.CharField(max_length=20, null=True, blank=True, verbose_name='图标分类')
    # url = models.URLField(verify_exists=False)
    url = models.URLField()
    
    #@login_required
    def graphic(self):
        '''
        generates an *img* html tag for html rendering
        '''
        return '<img name="image%d" src="%s">' % (self.pk, self.url)
    
    #@login_required
    def graphic_input(self):
        '''
        generates an *input* html tag with type=image for html rendering
        '''
        return '<input type=image name=icon src="%s">' % self.url
    
    def __str__(self):
        return self.url

    class Meta:
        verbose_name='1103图标'
        verbose_name_plural='1103图标'

class ImageButton(models.Model):
    '''
    Mapping object between an "action" and an "Icon".
    
    ImageButton objects have also a textual field: label.
    '''
    action = models.SlugField(primary_key=True,verbose_name='动作')
    label = models.CharField(max_length=100,verbose_name='标签')
    icon = models.ForeignKey(Icon,on_delete=models.DO_NOTHING,verbose_name='图标')
    
    #@login_required
    def graphic(self):
        '''
        generates an *img* html tag for html rendering
        '''
        return '<img name="image-%s" src="%s">' % (self.pk, self.icon.url)
    
    #@login_required
    def graphic_input(self):
        '''
        generates an *input* html tag with type=image for html rendering
        '''
        return '<input type=image name=image src="%s" value="%s" title="%s">' % (self.icon.url, self.pk, self.label)
    
    def __str__(self):
        return self.label

    class Meta:
        verbose_name='1104按键'
        verbose_name_plural='1104按键'




#过程定义
class Activity(models.Model):
    """Activities represent any kind of action an employee might want to do on an instance.    
    The action might want to change the object instance, or simply
    route the instance on a given path. Activities are the places
    where any of these action are resolved by employees.a
    """
    KIND_CHOICES = (
                    ('standard', '标准'),
                    ('dummy', '虚拟'),
                    ('subflow', '子流程'),
                    )
    COMP_CHOICES = (
                    ('and', '与'),
                    ('xor', '或'),
                    )
    title = models.CharField(max_length=100,verbose_name='名称')
    kind =  models.CharField(max_length=10, choices=KIND_CHOICES, verbose_name='类型', default='standard')
    process = models.ForeignKey('Process',on_delete=models.DO_NOTHING, related_name='activities',verbose_name='流程')
    push_application = models.ForeignKey('PushApplication',on_delete=models.DO_NOTHING, related_name='push_activities', verbose_name='推送应用', null=True, blank=True)
    pushapp_param = models.CharField(max_length=100, null=True, blank=True,verbose_name='推送应用参数', 
                                help_text="parameters dictionary; example: {'username':'john'}")
    application = models.ForeignKey('Application',on_delete=models.DO_NOTHING, related_name='activities', verbose_name='过程应用',null=True, blank=True,
                                help_text='leave it blank for prototyping the process without coding')
    app_param = models.CharField(max_length=100, verbose_name='过程应用参数', 
                                 help_text='parameters dictionary', null=True, blank=True)
    subflow = models.ForeignKey('Process',on_delete=models.DO_NOTHING, related_name='parent_activities', verbose_name='子流程',null=True, blank=True)
    roles = models.ManyToManyField(Group, related_name='activities',verbose_name='过程角色', null=True, blank=True)
    description = models.TextField(null=True, blank=True,verbose_name='说明')
    autostart = models.BooleanField(default=False,verbose_name='自动开始')
    autofinish = models.BooleanField(default=True,verbose_name='自动结束')
    join_mode =  models.CharField(max_length=3, choices=COMP_CHOICES, verbose_name='合并模式', default='xor')
    split_mode =  models.CharField(max_length=3, choices=COMP_CHOICES, verbose_name='分开模式', default='and')
    
    def nb_input_transitions(self):
        ''' returns the number of inputing transitions.
        '''
        return Transition.objects.filter(output=self, process=self.process).count()

    def __str__(self):
        return '%s (%s)' % (self.title, self.process.title)
    
    class Meta:
        unique_together = (("title", "process"),)
        verbose_name = '1105过程定义'
        verbose_name_plural = '1105过程定义'

#流程管理
class ProcessManager(models.Manager):
    '''Custom model manager for Process
    '''
    
    #TODO: also not too happy about this one.
    def is_enabled(self, title):
        '''
        Determines given a title if a process is enabled or otherwise
        
        :rtype: bool
        
        usage::
        
            if Process.objects.is_enabled('leave1'):
                # do something
        
        '''
        return self.get(title=title).enabled
    
    def check_can_start(self, process_name, user):
        '''
        Checks whether a process is enabled and whether the user has permission
        to instantiate it; raises exceptions if not the case, returns None otherwise.
        
        @type process_name: string
        @param process_name: a name of a process. e.g. 'leave'
        @type user: User
        @param user: an instance of django.contrib.auth.models.User, 
                     typically retrieved through a request object.
        @rtype:
        @return: passes silently if checks are met, 
                 raises exceptions otherwise.
        '''
        if not self.is_enabled(process_name):
            raise Exception('process %s disabled.' % process_name)

        if not user.is_superuser:
            if user.has_perm("workflow.can_instantiate"):
                lst = user.groups.filter(name=process_name)
                if lst.count()==0 or \
                   (lst[0].permissions.filter(codename='can_instantiate').count() == 0):
                    raise Exception('permission needed to instantiate process %s.' % process_name)
            else:
                raise Exception('permission needed.')
        return

#流程定义
class Process(models.Model):
    """A process holds the map that describes the flow of work.
    
    The process map is made of activities and transitions.
    The instances you create on the map will begin the flow in
    the configured begin activity. Instances can be moved
    forward from activity to activity, going through transitions,
    until they reach the End activity.
    """
    enabled = models.BooleanField(default=True,verbose_name='是否可用')
    date = models.DateTimeField(auto_now=True,verbose_name='创建日期')
    title = models.CharField(max_length=100,verbose_name='流程名称')
    description = models.TextField(verbose_name='说明')
    description.login_required=True
    begin = models.ForeignKey('Activity',on_delete=models.DO_NOTHING, related_name='bprocess', verbose_name='开始过程', null=True, blank=True)
    end = models.ForeignKey('Activity',on_delete=models.DO_NOTHING, related_name='eprocess', verbose_name='结束过程', null=True, blank=True,
                            help_text='a default end activity will be created if blank')
    priority = models.IntegerField(default=0,verbose_name='优先级')
        
    # add new ProcessManager
    objects = ProcessManager()
    
    class Meta:
        verbose_name_plural = '1106流程定义'
        verbose_name='1106流程定义'
        permissions = (
            ("can_instantiate", "Can instantiate"),
            ("can_browse", "Can browse"),
        )
    
    def __str__(self):
        return self.title
    
    #@login_required
    def summary(self):
        return '<pre>%s</pre>' % self.description
    
    #@login_required
    def action(self):
        return 'add <a href=../activity/add/>a new activity</a> or <a href=../activity/>copy</a> an activity from another process'

    
    def add_activity(self, name):
        '''
        name: name of activity (get or created)
        '''
        a, created = Activity.objects.get_or_create(title=name, process=self, 
                                                    defaults={'description':'(add description)'})
        return a 
    
    def add_transition(self, name, activity_out, activity_in):
        t, created = Transition.objects.get_or_create(name=name, process=self,
                                             output=activity_out,
                                             defaults={'input':activity_in})
        return t
    
    def create_authorized_group_if_not_exists(self):
        g, created = Group.objects.get_or_create(name=self.title)
        if created:
            ptype = ContentType.objects.get_for_model(Process)
            cip = Permission.objects.get(content_type=ptype, codename='can_instantiate')
            g.permissions.add(cip)
        
    def save(self, no_end=False):
        models.Model.save(self)
        # instantiation group
        self.create_authorized_group_if_not_exists()
        
        if not no_end and not self.end:
            self.end = Activity.objects.create(title='End', process=self, kind='dummy', autostart=True)
            models.Model.save(self)
        try:
            if self.end and self.end.process.id != self.id:
                a = self.end
                a.id = None
                a.process = self
                a.save()
                self.end = a
                models.Model.save(self)
            if self.begin and self.begin.process.id != self.id:
                a = self.begin
                a.id = None
                a.process = self
                a.save()
                self.begin = a
                models.Model.save(self)
        except Exception:
            # admin console error ?!?
            pass

#应用定义
class Application(models.Model):
    """ An application is a python view that can be called by URL.
    
        Activities can call applications.
        A commmon prefix may be defined: see settings.WF_APPS_PREFIX
    """
    url = models.CharField(max_length=255, unique=True, verbose_name='应用路径',help_text='relative to prefix in settings.WF_APPS_PREFIX')
    # TODO: drop abbreviations (perhaps here not so necessary to ??
    SUFF_CHOICES = (
                    ('w', '工作.id'),
                    ('i', '程序.id'),
                    ('o', '对像.id'),
                    )
    suffix =  models.CharField(max_length=1, choices=SUFF_CHOICES, verbose_name='应用类型', null=True, blank=True,
                               default='w', help_text='http://[host]/[settings.WF_APPS_PREFIX/][url]/[suffix]')
    detected_as_auto = None
    
    def __str__(self):
        return self.url
    
    def get_app_url(self, workitem=None, extern_for_user=None):
        from django.conf import settings
        path = '%s/%s/' % (settings.WF_APPS_PREFIX, self.url)
        if workitem:
            if self.suffix:
                if self.suffix == 'w': path = '%s%d/' % (path, workitem.id)
                if self.suffix == 'i': path = '%s%d/' % (path, workitem.instance.id)
                if self.suffix == 'o': path = '%s%d/' % (path, workitem.instance.content_object.id)
            else:
                path = '%s?workitem_id=%d' % (path, workitem.id) 
        if extern_for_user:
            profile = UserProfile.objects.get(user=user)
            path = 'http://%s%s' % (profile.web_host, path)
        return path
    
    def get_handler(self):
        '''returns handler mapped to url.
        '''
        try:
            func, args, kwargs = resolve(self.get_app_url() + '0/')
            self.detected_as_auto = False
        except Exception:
            func, args, kwargs = resolve(self.get_app_url())
            self.detected_as_auto = True
        return func
    
    #@login_required
    def documentation(self):
        doc = ''
        if self.detected_as_auto:
            doc = 'detected as auto application.<hr>'
        try:
            doc += u'<pre>%s</pre>' % self.get_handler().__doc__
        except Exception as v:
            doc += 'WARNING: the url %s is not resolved.' % self.get_app_url()
        return doc
    
    def has_test_env(self):
        if Process.objects.filter(title='test_%s' % self.url).count() > 0:
            return True
        return False
    
    def create_test_env(self, user=None):
        if self.has_test_env(): 
            return
        
        g = Group.objects.create(name='test_%s' % self.url)
        ptype = ContentType.objects.get_for_model(Process)
        cip = Permission.objects.get(content_type=ptype, codename='can_instantiate')
        g.permissions.add(cip)
        # group added to current user
        if user: 
            user.groups.add(g)

        p = Process.objects.create(title='test_%s' % self.url, description='unit test process')
        p.begin = p.end
        p.begin.autostart = False
        p.begin.title = "test_activity"
        p.begin.kind = 'standard'
        p.begin.application = self
        p.begin.description = 'test activity for application %s' % self.url
        p.begin.save()
        
        p.begin.roles.add(g)
        
        p.save()
    
    def remove_test_env(self):
        if not self.has_test_env(): return
        Process.objects.filter(title='test_%s' % self.url).delete()
        Group.objects.filter(name='test_%s' % self.url).delete()
    
    #@login_required
    def test(self):
        if self.has_test_env():
            return ('<a href=teststart/%d/>start test instances</a> | '
                    '<a href=testenv/remove/%d/>remove unit test env</a>') % (self.id, self.id)
        else:
            return '<a href=testenv/create/%d/>create unit test env</a>' % self.id

    class Meta:
        verbose_name='1107应用定义'
        verbose_name_plural='1107应用定义'

#推送应用
class PushApplication(models.Model):
    """A push application routes a workitem to a specific user.
    It is a python function with the same prototype as the built-in
    one below::    
        def route_to_requester(workitem):
            return workitem.instance.user    
    Other parameters may be added (see Activity.pushapp_param field).
    Built-in push applications are implemented in pushapps module.
    A commmon prefix may be defined: see settings.WF_PUSH_APPS_PREFIX
    
    """
    url = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name='1108推送应用'
        verbose_name_plural='1108推送应用'
            
    
    def get_handler(self):
        '''returns handler mapped to url.
        '''
        try:
            # search first in pre-built handlers
            import pushapps
            if self.url in dir(pushapps):
                # TODO
                return eval('pushapps.%s' % self.url)
            # then search elsewhere
            prefix = settings.WF_PUSH_APPS_PREFIX
            # dyn import
            exec('import %s' % prefix)
            return eval('%s.%s' % (prefix, self.url))
        except Exception as v:
            log.error('PushApplication.get_handler %s', v)
        return None
    
    #@login_required
    def documentation(self):
        return u'<pre>%s</pre>' % self.get_handler().__doc__
        
    def execute(self, workitem, **kwargs):
        handler = self.get_handler()
        return handler(workitem, **kwargs)
    
    def __str__(self):
        return self.url
    
    #@login_required
    def test(self):
        return '<a href=#>test (not yet implemented)</a>' 
      
#过程转换  
class Transition(models.Model):
    """ A Transition connects two Activities: a From and a To activity.    
    Since the transition is oriented you can think at it as being a
    link starting from the From and ending in the To activity.
    Linking the activities in your process you will be able to draw
    the map.    
    Each transition is associated to a condition that will be tested
    each time an instance has to choose which path to follow.
    If the only transition whose condition is evaluated to true will
    be the transition choosen for the forwarding of the instance.
    """
    name = models.CharField(max_length=50, null=True, blank=True,verbose_name='名称')
    process = models.ForeignKey(Process,on_delete=models.DO_NOTHING, related_name='transitions',verbose_name='流程')
    input = models.ForeignKey(Activity,on_delete=models.DO_NOTHING, related_name='transition_inputs',verbose_name='过程输入')
    condition = models.CharField(max_length=200, null=True, blank=True,verbose_name='过程条件',
                                 help_text='ex: instance.condition=="OK" | OK')
    output = models.ForeignKey(Activity,on_delete=models.DO_NOTHING, related_name='transition_outputs',verbose_name='过程输出')
    description = models.CharField(max_length=100, null=True, blank=True,verbose_name='过程说明')
    precondition = models.SlugField(null=True, blank=True,verbose_name='预定条件', help_text='object method that return True if transition is posible')
    
    def is_transition(self):
        ''' used in admin templates.
        '''
        return True
    
    def save(self):
        if self.input.process != self.process or self.output.process != self.process:
            raise Exception("a transition and its activities must be linked to the same process")
        models.Model.save(self)
    
    def __str__(self):
        return self.name or 't%s' % str(self.pk)


    def __str__(self):
        return self.name or 't%s' % str(self.pk)

    class Meta:
        verbose_name = '1109过程转换'
        verbose_name_plural='1109过程转换'
        pass

#用户消息
class UserProfile(models.Model):
    """Contains workflow-specific user data.
    """
    user = models.OneToOneField(User,on_delete=models.CASCADE, unique=True,verbose_name='用户')
    web_host = models.CharField(max_length=100, default='http://192.168.1.3:83/profile/',verbose_name='个人网址')
    notified = models.BooleanField(default=True, verbose_name='邮件通知')
    last_notif = models.DateTimeField(default=datetime.now,verbose_name='最后通知时间')
    nb_wi_notif = models.IntegerField(default=1, verbose_name='消息数',help_text='notification if the number of items waiting is reached')
    notif_delay = models.IntegerField(default=1, verbose_name='延后通知', help_text='in days')
    urgent_priority = models.IntegerField(default=5, verbose_name='优先级', help_text='a mail notification is sent when an item has at least this priority level')
    
    def save(self, **kwargs):
        if not self.last_notif:
            self.last_notif = datetime.now()
        models.Model.save(self,  **kwargs)
    
    def check_notif_to_send(self):
        now = datetime.now()
        if now > self.last_notif + timedelta(days=self.notif_delay or 1):
            return True
        return False
    
    def notif_sent(self):
        now = datetime.now()
        self.last_notif = now
        self.save()

    class Meta:
        verbose_name='1110用户消息设置'
        verbose_name_plural='1110用户消息设置'







#流程实例管理
class ProcessInstanceManager(models.Manager):
    '''Custom model manager for ProcessInstance
    '''
   
    def start(self, process_name, user, item, title=None, priority=0):
        '''
        Returns a workitem given the name of a preexisting enabled Process 
        instance, while passing in the id of the user, the contenttype 
        object and the title.
        
        :type process_name: string
        :param process_name: a name of a process. e.g. 'leave'
        :type user: User
        :param user: an instance of django.contrib.auth.models.User, 
                     typically retrieved through a request object.
        :type item: ContentType
        :param item: a content_type object e.g. an instance of LeaveRequest
        :type: title: string
        :param title: title of new ProcessInstance instance (optional)
        :type: priority: integer
        :param priority: default priority (optional)
        :rtype: WorkItem
        :return: a newly configured workitem sent to auto_user, 
                 a target_user, or ?? (roles).
        
        usage::
            
            wi = Process.objects.start(process_name='leave', 
                                       user=admin, item=leaverequest1)

        '''
        
        process = Process.objects.get(title=process_name, enabled=True)
        if priority == 0: priority = process.priority
            
        if not title or (title=='instance'):
            title = '%s %s' % (process_name, str(item))
        instance = ProcessInstance.objects.create(process=process, user=user, title=title, content_object=item)
        # instance running
        instance.set_status('running')
        
        workitem = WorkItem.objects.create(instance=instance, user=user, 
                                           activity=process.begin, priority=priority)
        log.event('created by ' + user.username, workitem)
        log('process:', process_name, 'user:', user.username, 'item:', item)
    
        if process.begin.kind == 'dummy':
            log('routing activity', process.begin.title, 'workitem:', workitem)
            auto_user = User.objects.get(username=settings.WF_USER_AUTO)
            workitem.activate(actor=auto_user)
            workitem.complete(actor=auto_user)
            return workitem
        
        if process.begin.autostart:
            log('run auto activity', process.begin.title, 'workitem:', workitem)
            auto_user = User.objects.get(username=settings.WF_USER_AUTO)
            workitem.activate(actor=auto_user)
    
            if workitem.exec_auto_application():
                log('workitem.exec_auto_application:', workitem)
                workitem.complete(actor=auto_user)
            return workitem

        if process.begin.push_application:
            target_user = workitem.exec_push_application()
            log('application pushed to user', target_user.username)
            workitem.user = target_user
            workitem.save()
            log.event('assigned to '+target_user.username, workitem)
            #notify_if_needed(user=target_user)
        else:
            # set pull roles; useful (in activity too)?
            workitem.pull_roles = workitem.activity.roles.all()
            workitem.save()
            #notify_if_needed(roles=workitem.pull_roles)
        
        return workitem
#流程实例
class ProcessInstance(models.Model):
    """ This is a process instance.
    
    A process instance is created when someone decides to do something,
    and doing this thing means start using a process defined in GoFlow.
    That's why it is called "process instance". The process is a class
    (=the definition of the process), and each time you want to
    "do what is defined in this process", that means you want to create
    an INSTANCE of this process.
    
    So from this point of view, an instance represents your dynamic
    part of a process. While the process definition contains the map
    of the workflow, the instance stores your usage, your history,
    your state of this process.
    
    The ProcessInstance will collect and handle workitems (see definition)
    to be passed from activity to activity in the process.
    
    Each instance can have more than one workitem depending on the
    number of split actions encountered in the process flow.
    That means that an instance is actually the collection of all of
    the instance "pieces" (workitems) that we get from splits of the
    same original process instance.
    
    Each ProcessInstance keeps track of its history through a graph.
    Each node of the graph represents an activity the instance has
    gone through (normal graph nodes) or an activity the instance is
    now pending on (a graph leaf node). Tracking the ProcessInstance history
    can be very useful for the ProcessInstance monitoring.
    
    When a process instance starts, the instance has to carry an
    implementation object that contains the application data. The
    specifications for the implementation class is:
    
    (nothing: now managed by generic relation)
    
    From the instance, the implementation object is reached as following:
      obj = instance.content_object (or instance.wfobject()).
    In a template, a field date1 will be displayed like this:
      {{ instance.wfobject.date1 }} or {{ instance.content_object.date1 }}
    
    From the object, instances may be reached with the reverse generic relation:
    the following can be added to the model:
      wfinstances = generic.GenericRelation(ProcessInstance)
    
    """
    STATUS_CHOICES = (
                      ('initiated', '发起'),
                      ('running', '进程中'),
                      ('active', '有效'),
                      ('complete', '完成'),
                      ('terminated', '终止'),
                      ('suspended', '暂停'),
                      )
    title = models.CharField(max_length=100,verbose_name='模型名称')
    process = models.ForeignKey(Process,on_delete=models.DO_NOTHING, related_name='instances', null=True, blank=True,verbose_name='流程')
    creationTime = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='instances',verbose_name='用户')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='initiated',verbose_name='当前状态')
    old_status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=True, blank=True,verbose_name='原始状态')
    condition = models.CharField(max_length=50, null=True, blank=True,verbose_name='条件')
    
    # refactoring
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING,verbose_name='数据模型')
    object_id = models.PositiveIntegerField(verbose_name='正整数序号')
    content_object = fields.GenericForeignKey('content_type', 'object_id')
    
    # add new ProcessInstanceManager
    objects = ProcessInstanceManager()
    
    def wfobject(self):
        return self.content_object
    
    #@login_required
    def workitems_list(self):
        '''provide html link to workitems for a process instance in admin change list.
        @rtype: string
        @return: html href link "../workitem/?instance__id__exact=[self.id]&ot=asc&o=0"
        '''
        nbwi = self.workitems.count()
        return '<a href=../workitem/?instance__id__exact=%d&ot=asc&o=0>%d item(s)</a>' % (self.pk, nbwi)
    
    def __str__(self):
        return str(self.pk)
    
    def __str__(self):
        return self.title
    
    def set_status(self, status):
        if not status in [x for x,y in ProcessInstance.STATUS_CHOICES]:
            raise Exception('instance status incorrect :%s' % status)
        self.old_status = self.status
        self.status = status
        self.save()

    class Meta:
        verbose_name='1111流程模型'
        verbose_name_plural='1111流程模型'
#工作项目管理
class WorkItemManager(models.Manager):
    '''Custom model manager for WorkItem
    '''
    def get_safe(self, id, user=None, enabled_only=False, status=('inactive','active')):
        '''
        Retrieves a single WorkItem instance given a set of parameters
        
        :type id: int
        :param id: the id of the WorkItem instance
        :type user: User
        :param user: an instance of django.contrib.auth.models.User, 
                     typically retrieved through a request object.
        :type enabled_only: bool
        :param enabled_only: implies that only enabled processes should be queried
        :type status: tuple or string
        :param status: ensure that workitem has one of the given set of statuses
        
        usage::
        
            workitem = WorkItem.objects.get_safe(id, user=request.user)
        
        '''
        if enabled_only:
            workitem = self.get(id=id, activity__process__enabled=True)
        else:
            workitem = self.get(id=id)
        workitem._check(user, status)
        return workitem

    def list_safe(self, user=None, username=None, queryset='qs_default', activity=None, status=None,
                      notstatus=('blocked','suspended','fallout','complete'), noauto=True):
        """
        Retrieve list of workitems (in order to display a task list for example).
        
        :type user: User
        :param user: filter on instance of django.contrib.auth.models.User (default=all) 
        :type username: string
        :param username: filter on username of django.contrib.auth.models.User (default=all) 
        :type queryset: QuerySet
        :param queryset: pre-filtering (default=WorkItem.objects)
        :type activity: Activity
        :param activity: filter on instance of goflow.workflow.models.Activity (default=all) 
        :type status: string
        :param status: filter on status (default=all) 
        :type notstatus: string or tuple
        :param notstatus: list of status to exclude (default: [blocked, suspended, fallout, complete])
        :type noauto: bool
        :param noauto: if True (default) auto activities are excluded.
        
        usage::
        
            workitems = WorkItem.objects.list_safe(user=me, notstatus='complete', noauto=True)
        
        """
        if queryset == 'qs_default': queryset = WorkItem.objects
        if status: notstatus = []
        
        groups = Group.objects.all()
        if user:
            query = queryset.filter(user=user, activity__process__enabled=True).order_by('-priority')
            groups = user.groups.all()
        else:
            if username:
                query = queryset.filter(
                        user__username=username, 
                        activity__process__enabled=True
                ).order_by('-priority')
                groups = User.objects.get(username=username).groups.all()
            else:
                query = None
        if query:
            if status:
                query = query.filter(status=status)
            
            if notstatus:
                for s in notstatus: 
                    query = query.exclude(status=s)
            
            if noauto:
                query = query.exclude(activity__autostart=True)
            
            if activity:
                #TODO: this is not used...??
                sq = query.filter(activity=activity)
            
            query = list(query)
        else:
            query = []
        
        # search pullable workitems
        for role in groups:
            pullables = queryset.filter(pull_roles=role, activity__process__enabled=True).order_by('-priority')
            if status:
                pullables = pullables.filter(status=status)
            
            if notstatus:
                for s in notstatus:
                    pullables = pullables.exclude(status=s)
            
            if noauto:
                pullables = pullables.exclude(activity__autostart=True)
            
            if activity:
                pullables = pullables.filter(activity=activity)
            
            if user:
                pullables = pullables.filter(user__isnull=True) # tricky
                pullables = pullables.exclude(user=user)
                query.extend(list(pullables))
            
            if username:
                pullables = pullables.exclude(user__username=username)
            
            log.debug('pullables workitems role %s: %s', role, str(pullables))
            query.extend(list(pullables))
        
        # search workitems pullable by anybody
        pullables = queryset.filter(pull_roles__isnull=True,
                                    activity__process__enabled=True,
                                    user__isnull=True).order_by('-priority')
        if status:
            pullables = pullables.filter(status=status)
        if notstatus:
            for s in notstatus:
                pullables = pullables.exclude(status=s)
        if noauto:
            pullables = pullables.exclude(activity__autostart=True)
        if activity:
            pullables = pullables.filter(activity=activity)
        if pullables.count() > 0:
            log.debug('anybody\'s workitems: %s', str(pullables))
            query.extend(list(pullables))
        
        return query
    
    def notify_if_needed(self, user=None, roles=None):
        ''' notify user if conditions are fullfilled
        '''
        if user:
            workitems = self.list_safe(user=user, notstatus='complete', noauto=True)
            profile, created = UserProfile.objects.get_or_create(user=user)
            if len(workitems) >= profile.nb_wi_notif:
                try:
                    if profile.check_notif_to_send():
                        send_mail(workitems=workitems, user=user, subject='message', template='mail.txt')
                        profile.notif_sent()
                        log.info('notification sent to %s' % user.username)
                except Exception as v:
                    log.error('sendmail error: %s' % v)
        return

#工作项目
class WorkItem(models.Model):
    """A workitem object represents an activity you are performing.
    
    An Activity object defines the activity, while the workitem object
    represents that you are performing this activity. So workitem is
    an "instance" of the activity.
    """
    STATUS_CHOICES = (
                      ('blocked', '锁定'),
                      ('inactive', '无效'),
                      ('active', '有效'),
                      ('suspended', '暂停'),
                      ('fallout', '后续'),
                      ('complete', '完成'),
                      )
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name='workitems', null=True, blank=True, verbose_name='用户')
    instance = models.ForeignKey(ProcessInstance,on_delete=models.DO_NOTHING, related_name='workitems',verbose_name='流程')
    activity = models.ForeignKey(Activity,on_delete=models.DO_NOTHING, related_name='workitems',verbose_name='活动')
    workitem_from = models.ForeignKey('self',on_delete=models.DO_NOTHING, related_name='workitems_to', null=True, blank=True,verbose_name='工作表单')
    others_workitems_from = models.ManyToManyField('self', related_name='others_workitems_to', null=True, blank=True,verbose_name='关联表单')
    push_roles = models.ManyToManyField(Group, related_name='push_workitems', null=True, blank=True,verbose_name='角色拉动')
    pull_roles = models.ManyToManyField(Group, related_name='pull_workitems', null=True, blank=True,verbose_name='角色推动')
    blocked = models.BooleanField(default=False,verbose_name='是否锁定')
    priority = models.IntegerField(default=0,verbose_name='优先级别')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='inactive',verbose_name='状态')

    objects = WorkItemManager()
    
    def forward(self, timeout_forwarding=False, subflow_workitem=None):
        # forward_workitem(workitem, path=None, timeout_forwarding=False, subflow_workitem=None):
        '''
        Convenience procedure to forwards workitems to valid destination activities.
        
        @type path: string??
        @param path: XXX TODO: This is not used, so don't know why it's here.
        @type timeoutForwarding: bool
        @param timeoutForwarding:
        @type: subflow_workitem: WorkItem
        @param subflow_workitem: a workitem associated with a subflow ???
        
        '''
        log.info(u'forward_workitem %s', self.__str__())
        if not timeout_forwarding:
            if self.status != 'complete':
                return
        if self.has_workitems_to() and not subflow_workitem:
            log.debug('forward_workitem canceled for %s: ' 
                       'workitem.has_workitems_to()', self.__str__())
            return
        
        if timeout_forwarding:
            log.info('timeout forwarding')
            Event.objects.create(name='timeout', workitem=self)
        
        for destination in self.get_destinations(timeout_forwarding):
            self._forward_workitem_to_activity(destination)
            if self.activity.split_mode == 'xor': break

    def _forward_workitem_to_activity(self, target_activity):
        '''
        Passes the process instance embedded in the given workitem 
        to a new workitem that is associated with the destination activity.
        
        @type target_activity: Activity
        @param target_activity: the activity instance to which the workitem 
                                should be forwarded
        @rtype: WorkItem
        @return: a workitem that has been passed on to the next 
                 activity (and next user)
        '''
        instance = self.instance
        # search a blocked workitem first
        qwi = WorkItem.objects.filter(instance=instance, activity=target_activity, status='blocked')
        if qwi.count() == 0:
            wi = WorkItem.objects.create(instance=instance, activity=target_activity,
                                         user=None, priority=self.priority)
            created = True
            log.info('forwarded to %s', target_activity.title)
            Event.objects.create(name='creation by %s' % self.user.username, workitem=wi)
            Event.objects.create(name='forwarded to %s' % target_activity.title, workitem=self)
            wi.workitem_from = self
        else:
            created = False
            wi = qwi[0]
        
        if target_activity.join_mode == 'and':
            nb_input_transitions = target_activity.nb_input_transitions()
            if nb_input_transitions > 1:
                if created:
                    # first worktem: block it
                    wi.block()
                    return    
                else:
                    wi.others_workitems_from.add(self)
                    if wi.others_workitems_from.all().count() + 1 < nb_input_transitions:
                        # keep blocked
                        return
                    else:
                        # check if the join is OK
                        if wi.check_join():
                            wi.status = 'inactive'
                            wi.save()
                            log.info('activity %s: workitem %s unblocked', target_activity.title, str(wi))
                        else:
                            return
        else:
            if not created:
                # join_mode='and'
                log.error('activity %s: join_mode must be and', target_activity.title)
                self.fall_out()
                wi.fall_out()
                return
        
        if target_activity.autostart:
            log.info('run auto activity %s workitem %s', target_activity.title, str(wi))
            try:
                auto_user = User.objects.get(username=settings.WF_USER_AUTO)
            except Exception:
                error = 'a user named %s (settings.WF_USER_AUTO) must be defined for auto activities'
                raise Exception(error % settings.WF_USER_AUTO)
            wi.activate(actor=auto_user)
            if wi.exec_auto_application():
                wi.complete(actor=auto_user)
            return wi
        
        if target_activity.push_application:
            target_user = wi.exec_push_application()
            log.info('application pushed to user %s', target_user.username)
            wi.user = target_user
            wi.save()
            Event.objects.create(name='assigned to %s' % target_user.username, workitem=wi)
            WorkItem.objects.notify_if_needed(user=target_user)
        else:
            wi.pull_roles = wi.activity.roles.all()
            wi.save()
            WorkItem.objects.notify_if_needed(roles=wi.pull_roles)
        return wi
    
    def check_join(self):
        log.warning('workitem check_join NYI- useful ?')
        return True
    
    def _check(self, user, status=('inactive','active')):
        '''
        helper function to determine whether process is:
            - enabled, etc..
        
        '''
        if type(status)==type(''):
            status = (status,)
            
        if not self.activity.process.enabled:
            error = 'process %s disabled.' % self.activity.process.title
            log.error('workitem._check: %s' % error)
            raise Exception(error)
            
        if not self.check_user(user):
            error = 'user %s cannot take workitem %d.' % (user.username, self.pk)
            log.error('workitem._check: %s' % error)
            self.fall_out()
            raise Exception(error)
            
        if not self.status in status:
            error = 'workitem %d has not a correct status (%s/%s).' % (
                self.pk, self.status, str(status))
            log.error('workitem._check: %s' % error)
            raise Exception(error)
        return
    
    def get_destinations(self, timeout_forwarding=False):
        #get_destinations(workitem, path=None, timeout_forwarding=False):
        '''
        Return list of destination activities that meet the conditions of each transition
        
        @type path: string??
        @param path: XXX TODO: This is not used, so don't know why it's here.
        @type timeout_forwarding: bool
        @param timeout_forwarding: a workitem with a time-delay??
        @rtype: [Activity]
        @return: list of destination activities.
        '''
        transitions = Transition.objects.filter(input=self.activity)
        if timeout_forwarding:
            transitions = transitions.filter(condition__contains='workitem.time_out')
        destinations = []
        for t in transitions:
            if self.eval_transition_condition(t):
                destinations.append(t.output)
        return destinations
    
    def eval_transition_condition(self, transition):
        '''
        evaluate the condition of a transition
        '''
        if not transition.condition:
            return True
        instance = self.instance
        wfobject = instance.wfobject()
        log.debug('eval_transition_condition %s - %s', 
            transition.condition, instance.condition)
        try:
            result = eval(transition.condition)
            
            # boolean expr
            if type(result) == type(True):
                log.debug('eval_transition_condition boolean %s', str(result))
                return result
            if type(result) == type(''):
                log.debug('eval_transition_condition cmp instance.condition %s', str(instance.condition==result))
                return (instance.condition==result)
        except Exception as v:
            log.debug('eval_transition_condition [%s]: %s', transition.condition, v)
            return (instance.condition==transition.condition)
            #log.error('eval_transition_condition [%s]: %s', transition.condition, v)
        return False
    
    def exec_push_application(self):
        '''
        Execute push application in workitem
        '''
        if not self.activity.process.enabled:
            raise Exception('process %s disabled.' % self.activity.process.title)
        params = self.activity.pushapp_param
        try:
            if params: kwargs = eval(params)
            else: kwargs = {}
            result = self.activity.push_application.execute(self, **kwargs)
        except Exception as v:
            log.error('exec_push_application %s', v)
            result = None
            self.fall_out()
        return result
    
    def exec_auto_application(self):
        '''
        creates a test auto application for activities that don't yet have applications
        @rtype: bool
        '''
        try:
            if not self.activity.process.enabled:
                raise Exception('process %s disabled.' % self.activity.process.title)
            # no application: default auto app
            if not self.activity.application:
                return self.default_auto_app()
            
            func, args, kwargs = resolve(self.activity.application.get_app_url())
            params = self.activity.app_param
            # params values defined in activity override those defined in urls.py
            if params:
                params = eval('{'+params.lstrip('{').rstrip('}')+'}')
                kwargs.update(params)
            func(workitem=self , **kwargs)
            return True
        except Exception as v:
            log.error('execution wi %s:%s', self, v)
        return False
    
    def default_auto_app(self):
        '''
        retrieves wfobject, logs info to it saves
        
        @rtype: bool
        @return: always returns True
        '''
        obj = self.instance.wfobject()
        obj.history += '\n>>> execute auto activity: [%s]' % self.activity.title
        obj.save()
        return True
    
    def activate(self, actor):
        '''
        changes workitem status to 'active' and logs event, activator
        
        '''
        self._check(actor, ('inactive', 'active'))
        if self.status == 'active':
            log.warning('activate_workitem actor %s workitem %s already active', 
                        actor.username, str(self))
            return
        self.status = 'active'
        self.user = actor
        self.save()
        log.info('activate_workitem actor %s workitem %s', 
                 actor.username, str(self))
        Event.objects.create(name='activated by %s' % actor.username, workitem=self)
    
    def complete(self, actor):
        '''
        changes status of workitem to 'complete' and logs event
        '''
        self._check(actor, 'active')
        self.status = 'complete'
        self.user = actor
        self.save()
        log.info('complete_workitem actor %s workitem %s', actor.username, str(self))
        Event.objects.create(name='completed by %s' % actor.username, workitem=self)
        
        if self.activity.autofinish:
            log.debug('activity autofinish: forward')
            self.forward()
        
        # if end activity, instance is complete
        if self.instance.process.end == self.activity:
            log.info('activity end process %s' % self.instance.process.title)
            # first test subflow
            lwi = WorkItem.objects.filter(activity__subflow=self.instance.process,
                                          status='blocked',
                                          instance=self.instance)
            if lwi.count() > 0:
                log.info('parent process for subflow %s' % self.instance.process.title)
                workitem0 = lwi[0]
                workitem0.instance.process = workitem0.activity.process
                workitem0.instance.save()
                log.info('process change for instance %s' % workitem0.instance.title)
                workitem0.status = 'complete'
                workitem0.save()
                workitem0.forward(subflow_workitem=self)
            else:
                self.instance.set_status('complete')
    
    def start_subflow(self, actor=None):
        '''
        starts subflow and blocks passed in workitem
        '''
        if not actor: actor = self.user
        subflow_begin_activity = self.activity.subflow.begin
        instance = self.instance
        instance.process = self.activity.subflow
        instance.save()
        self.status = 'blocked'
        self.blocked = True
        self.save()
        
        sub_workitem = self._forward_workitem_to_activity(subflow_begin_activity)
        return sub_workitem
    
    def eval_condition(self, transition):
        '''
        evaluate the condition of a transition
        '''
        raise Exception("New API (not yet implemented)")
    
    def __str__(self):
        return str(self.pk)
    
    def __str__(self):
        return u'%s-%s-%s' % (self.instance.__str__(), self.activity.__str__(), str(self.pk))
    
    def has_workitems_to(self):
        b = ( self.workitems_to.count() > 0 )
        return b
    
    def check_user(self, user):
        """returns True if authorized, False if not.
        
        For dummy activities, returns always True
        """
        if self.activity.kind == 'dummy':
            return True
        
        if user and self.user and self.user != user:
            return False
        ugroups = user.groups.all()
        agroups = self.activity.roles.all()
        authorized = False
        if agroups and len(agroups) > 0:
            for g in ugroups:
                if g in agroups:
                    authorized = True
                    break
        else:
            authorized = True
        return authorized
            
    def set_user(self, user, commit=True):
        """affect user if he has a role authorized for activity.
        
        return True if authorized, False if not (workitem then falls out)
        """
        if self.check_user(user):
            self.user = user
            if commit: self.save()
            return True
        self.fallOut()
        return False
    
    def can_priority_change(self):
        '''can the user change priority.
        
        @rtype: bool
        @return: returns True if the user can change priority
        
        the user must belong to a group with "workitem.can_change_priority"  permission,
        and this group's name must be the same as the process title.
        '''
        if self.user.has_perm("workitem.can_change_priority"):
            lst = self.user.groups.filter(name=self.instance.process.title)
            if lst.count()==0 or \
               (lst[0].permissions.filter(codename='can_change_priority').count() == 0):
                return False
            return True
        return False
    
    def block(self):
        self.status = 'blocked'
        self.save()
        Event.objects.create(name='blocked', workitem=self)
    
    def fall_out(self):
        self.status = 'fallout'
        self.save()
        Event.objects.create(name='fallout', workitem=self)
        if not settings.DEBUG:
            mail_admins(subject='workflow workitem %s fall out' % str(self.pk),
                    message=u'''
                                The workitem [%s] was falling out.
                                Process:  %s
                                Activity: %s
                                instance: %s
                                ----------------------------------
                    ''' % (
                           self.instance.process,
                           self.activity,
                           self.instance,
                           ))
    
    def html_action(self):
        label = 'action'
        if self.status == 'inactive':
            label = 'activate'
            url='activate/%d/' % self.id
        if self.status == 'active':
            label = 'complete'
            url='complete/%d/' % self.id
        if self.status == 'complete':
            return 'completed'
        return '<a href=%s>%s</a>' % (url, label)
    
    def html_action_link(self):
        if self.status == 'inactive':
            url='activate/%d/' % self.id
        if self.status == 'active':
            url='complete/%d/' % self.id
        if self.status == 'complete':
            raise Exception('no action for completed workitems')
        return url
    
    def time_out(self, delay, unit='days'):
        '''
        return True if timeout reached
          delay:    nb units
          unit: 'weeks' | 'days' | 'hours' ... (see timedelta)
        '''
        tdelta = eval('timedelta('+unit+'=delay)')
        now = datetime.now()
        return (now > (self.date + tdelta))
    
    #@login_required
    def events_list(self):
        '''provide html link to events for a workitem in admin change list.
        @rtype: string
        @return: html href link "../event/?workitem__id__exact=[self.id]&ot=asc&o=0"
        '''
        nbevt = self.events.count()
        return '<a href=../event/?workitem__id__exact=%d&ot=asc&o=0>%d item(s)</a>' % (self.pk, nbevt)
    
    class Meta:
        permissions = (
            ("can_change_priority", "Can change priority"),
        )
        verbose_name='1112工作项目'
        verbose_name_plural='1112工作项目'

#事件
class Event(models.Model):
    """Event are changes that happens on workitems.
    """
    date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50,verbose_name='事件')
    workitem = models.ForeignKey(WorkItem,on_delete=models.DO_NOTHING, related_name='events',verbose_name='工作')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='1113事件'
        verbose_name_plural='1113事件'


#grahpics

class graphicsImage(models.Model):
    file = models.ImageField(upload_to='images')
    info = models.CharField(max_length=100, null=True, blank=True)
    
    @login_required
    def graphic(self):
        return '<img name=image%d src=%s>' % (self.id, self.get_file_url())

    def __str__(self):
        return self.info


    class Meta:
        verbose_name='1114事件图形'
        verbose_name_plural='1114事件图形'


class Graph(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING, null=True, blank=True, related_name='children')
    background = models.ForeignKey('Visual',on_delete=models.DO_NOTHING, null=True, blank=True, related_name='bg_graphes')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='1115'
        verbose_name_plural='1115'


class MetaGraph(models.Model):
    template = models.ForeignKey(Graph,on_delete=models.DO_NOTHING)
    parent = models.ForeignKey('self',on_delete=models.DO_NOTHING, null=True, blank=True, related_name='children')
    content_type = models.ManyToManyField(ContentType)

    parent_attr = models.CharField(max_length=50, default='parent')
    children_attr = models.CharField(max_length=50, default='children')
    position_method = models.CharField(max_length=50, default='position')
    zorder_method = models.CharField(max_length=50, default='zorder')
    moveable_method = models.CharField(max_length=50, default='is_moveable')   

    class Meta:
        verbose_name='1116'
        verbose_name_plural='1116'


class Visual(models.Model):
    x = models.PositiveSmallIntegerField(default=0)
    y = models.PositiveSmallIntegerField(default=0)
    w = models.PositiveSmallIntegerField(default=0)
    h = models.PositiveSmallIntegerField(default=0)
    need_update = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    z = models.PositiveSmallIntegerField(default=0)
    image = models.ForeignKey(Image,on_delete=models.DO_NOTHING, null=True, blank=True)
    
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    graph = models.ForeignKey(Graph,on_delete=models.DO_NOTHING)

    @login_required
    def graphic(self):
        return '<img src=%s>' % self.image.get_file_url()

    class Meta:
        verbose_name='1117流程可视'
        verbose_name_plural='1117流程可视'