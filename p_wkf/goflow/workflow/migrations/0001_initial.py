# Generated by Django 2.0.4 on 2018-06-22 08:29

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='名称')),
                ('kind', models.CharField(choices=[('standard', '标准'), ('dummy', '虚拟'), ('subflow', '子流程')], default='standard', max_length=10, verbose_name='类型')),
                ('pushapp_param', models.CharField(blank=True, help_text="parameters dictionary; example: {'username':'john'}", max_length=100, null=True, verbose_name='推送应用参数')),
                ('app_param', models.CharField(blank=True, help_text='parameters dictionary', max_length=100, null=True, verbose_name='过程应用参数')),
                ('description', models.TextField(blank=True, null=True, verbose_name='说明')),
                ('autostart', models.BooleanField(default=False, verbose_name='自动开始')),
                ('autofinish', models.BooleanField(default=True, verbose_name='自动结束')),
                ('join_mode', models.CharField(choices=[('and', '与'), ('xor', '或')], default='xor', max_length=3, verbose_name='合并模式')),
                ('split_mode', models.CharField(choices=[('and', '与'), ('xor', '或')], default='and', max_length=3, verbose_name='分开模式')),
            ],
            options={
                'verbose_name': '过程定义',
                'verbose_name_plural': '过程定义',
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(help_text='relative to prefix in settings.WF_APPS_PREFIX', max_length=255, unique=True, verbose_name='应用路径')),
                ('suffix', models.CharField(blank=True, choices=[('w', '工作.id'), ('i', '程序.id'), ('o', '对像.id')], default='w', help_text='http://[host]/[settings.WF_APPS_PREFIX/][url]/[suffix]', max_length=1, null=True, verbose_name='应用类型')),
            ],
            options={
                'verbose_name': '应用定义',
                'verbose_name_plural': '应用定义',
            },
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enabled', models.BooleanField(default=True, verbose_name='是否可用')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='创建日期')),
                ('title', models.CharField(max_length=100, verbose_name='流程名称')),
                ('description', models.TextField(verbose_name='说明')),
                ('priority', models.IntegerField(default=0, verbose_name='优先级')),
                ('begin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='bprocess', to='workflow.Activity', verbose_name='开始过程')),
                ('end', models.ForeignKey(blank=True, help_text='a default end activity will be created if blank', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='eprocess', to='workflow.Activity', verbose_name='结束过程')),
            ],
            options={
                'verbose_name': '流程定义',
                'verbose_name_plural': '流程定义',
                'permissions': (('can_instantiate', 'Can instantiate'), ('can_browse', 'Can browse')),
            },
        ),
        migrations.CreateModel(
            name='PushApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': '推送应用',
                'verbose_name_plural': '推送应用',
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='名称')),
                ('condition', models.CharField(blank=True, help_text='ex: instance.condition=="OK" | OK', max_length=200, null=True, verbose_name='过程条件')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='过程说明')),
                ('precondition', models.SlugField(blank=True, help_text='object method that return True if transition is posible', null=True, verbose_name='预定条件')),
                ('input', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transition_inputs', to='workflow.Activity', verbose_name='过程输入')),
                ('output', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transition_outputs', to='workflow.Activity', verbose_name='过程输出')),
                ('process', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='transitions', to='workflow.Process', verbose_name='流程')),
            ],
            options={
                'verbose_name': '过程转换',
                'verbose_name_plural': '过程转换',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('web_host', models.CharField(default='http://192.168.1.3:83/profile/', max_length=100, verbose_name='个人网址')),
                ('notified', models.BooleanField(default=True, verbose_name='邮件通知')),
                ('last_notif', models.DateTimeField(default=datetime.datetime.now, verbose_name='最后通知时间')),
                ('nb_wi_notif', models.IntegerField(default=1, help_text='notification if the number of items waiting is reached', verbose_name='消息数')),
                ('notif_delay', models.IntegerField(default=1, help_text='in days', verbose_name='延后通知')),
                ('urgent_priority', models.IntegerField(default=5, help_text='a mail notification is sent when an item has at least this priority level', verbose_name='优先级')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户消息设置',
                'verbose_name_plural': '用户消息设置',
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='application',
            field=models.ForeignKey(blank=True, help_text='leave it blank for prototyping the process without coding', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='activities', to='workflow.Application', verbose_name='过程应用'),
        ),
        migrations.AddField(
            model_name='activity',
            name='process',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='activities', to='workflow.Process', verbose_name='流程'),
        ),
        migrations.AddField(
            model_name='activity',
            name='push_application',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='push_activities', to='workflow.PushApplication', verbose_name='推送应用'),
        ),
        migrations.AddField(
            model_name='activity',
            name='roles',
            field=models.ManyToManyField(blank=True, null=True, related_name='activities', to='auth.Group', verbose_name='过程角色'),
        ),
        migrations.AddField(
            model_name='activity',
            name='subflow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parent_activities', to='workflow.Process', verbose_name='子流程'),
        ),
        migrations.AlterUniqueTogether(
            name='activity',
            unique_together={('title', 'process')},
        ),
    ]
