#--*-- coding=utf-8 --*--
from django import forms
from django.contrib.auth.models import User
#p_admin models

class LoginForm(forms.Form):
    username = forms.CharField(required = True,label=u"帐号",error_messages={'required':'请输入帐号'},widget=forms.TextInput(attrs={'placeholder':u"帐号",}),)   
    password = forms.CharField(required=True,label=u"密码",error_messages={'required':u'请输入密码'},widget=forms.PasswordInput(attrs={'placeholder':u"密码",}),)   

class RegisterForm(forms.Form):
	email=forms.EmailField(label=u"邮件",max_length=30,widget=forms.TextInput(attrs={'size': 30,}),)
	password=forms.CharField(label=u"密码",max_length=20,widget=forms.PasswordInput(attrs={'size': 20,}),)
	username=forms.CharField(label=u"帐号",max_length=20,widget=forms.TextInput(attrs={'size': 20,}),)
	first_name=forms.CharField(label=u"姓名",max_length=20,widget=forms.TextInput(attrs={'size': 20,}),)
	last_name=forms.CharField(label=u"部门",max_length=20,widget=forms.TextInput(attrs={'size': 20,}),)
    
class LockForm(forms.Form):
	password=forms.CharField(label=u"密码",max_length=20,widget=forms.PasswordInput(attrs={'size': 20,}),)
