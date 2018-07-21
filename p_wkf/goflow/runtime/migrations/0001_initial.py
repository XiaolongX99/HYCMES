# Generated by Django 2.0.4 on 2018-06-22 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, verbose_name='事件')),
            ],
            options={
                'verbose_name': '事件',
                'verbose_name_plural': '事件',
            },
        ),
        migrations.CreateModel(
            name='ProcessInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='模型名称')),
                ('creationTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('status', models.CharField(choices=[('initiated', '发起'), ('running', '进程中'), ('active', '有效'), ('complete', '完成'), ('terminated', '终止'), ('suspended', '暂停')], default='initiated', max_length=10, verbose_name='当前状态')),
                ('old_status', models.CharField(blank=True, choices=[('initiated', '发起'), ('running', '进程中'), ('active', '有效'), ('complete', '完成'), ('terminated', '终止'), ('suspended', '暂停')], max_length=10, null=True, verbose_name='原始状态')),
                ('condition', models.CharField(blank=True, max_length=50, null=True, verbose_name='条件')),
                ('object_id', models.PositiveIntegerField(verbose_name='正整数序号')),
            ],
            options={
                'verbose_name': '流程模型',
                'verbose_name_plural': '流程模型',
            },
        ),
        migrations.CreateModel(
            name='WorkItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('blocked', models.BooleanField(default=False, verbose_name='是否锁定')),
                ('priority', models.IntegerField(default=0, verbose_name='优先级别')),
                ('status', models.CharField(choices=[('blocked', '锁定'), ('inactive', '无效'), ('active', '有效'), ('suspended', '暂停'), ('fallout', '后续'), ('complete', '完成')], default='inactive', max_length=10, verbose_name='状态')),
            ],
            options={
                'verbose_name': '工作项目',
                'verbose_name_plural': '工作项目',
                'permissions': (('can_change_priority', 'Can change priority'),),
            },
        ),
    ]
