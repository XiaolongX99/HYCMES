#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from goflow.workflow.models import Transition
from django.contrib.auth.decorators import login_required
from django.conf import settings
#apptools

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
        verbose_name='Simulation object'

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
        verbose_name='图形'
        verbose_name_plural='图形'

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
        verbose_name='图标'
        verbose_name_plural='图标'

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
        verbose_name='按键'
        verbose_name_plural='按键'
