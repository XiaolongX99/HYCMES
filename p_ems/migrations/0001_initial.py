# Generated by Django 2.0.4 on 2018-07-19 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('p_admin', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('p_pdm', '0009_auto_20180716_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='assets',
            fields=[
                ('scode', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='资产编码')),
                ('sname', models.CharField(max_length=80, verbose_name='设备名称')),
                ('sspec', models.CharField(blank=True, max_length=40, null=True, verbose_name='设备规格')),
                ('category', models.CharField(blank=True, max_length=40, null=True, verbose_name='类型')),
                ('parent', models.CharField(blank=True, max_length=40, null=True, verbose_name='主件编码')),
                ('assets', models.CharField(blank=True, max_length=40, null=True, verbose_name='资产类别')),
                ('supply', models.CharField(blank=True, max_length=40, null=True, verbose_name='设备厂家')),
                ('eqty', models.SmallIntegerField(default=1, verbose_name='数量')),
                ('durable', models.SmallIntegerField(default=60, verbose_name='耐用月数')),
                ('entrydate', models.DateField(default=django.utils.timezone.now, verbose_name='进厂日期')),
                ('createtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '701固定资产',
                'verbose_name_plural': '701固定资产',
            },
        ),
        migrations.CreateModel(
            name='category',
            fields=[
                ('tcode', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='编码')),
                ('tname', models.CharField(max_length=80, unique=True, verbose_name='分类')),
                ('tdesc', models.TextField(blank=True, null=True, verbose_name='说明')),
                ('userguide', models.FileField(blank=True, null=True, upload_to='TPM/UserGuide/%Y%m%d/', verbose_name='用户手册')),
                ('createtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '705设备分类',
                'verbose_name_plural': '705设备分类',
            },
        ),
        migrations.CreateModel(
            name='equipment',
            fields=[
                ('ecode', models.CharField(help_text='此处以资产编号替代设备编号', max_length=40, primary_key=True, serialize=False, verbose_name='设备编码')),
                ('ename', models.CharField(max_length=80, verbose_name='设备名称')),
                ('status', models.CharField(choices=[('1', '运行中'), ('2', '维修中'), ('3', '保养中'), ('4', '闲置中'), ('5', '验收中'), ('6', '校验中')], default='4', max_length=40, verbose_name='当前状态')),
                ('station', models.CharField(default='工具室', help_text='以部门/Cell-工站-识别号 方式进行地点编码。', max_length=80, verbose_name='使用地点')),
                ('remark', models.TextField(blank=True, null=True, verbose_name='说明')),
                ('updatetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('updatename', models.CharField(blank=True, max_length=40, verbose_name='更新者')),
                ('MEG', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='equipment', to=settings.AUTH_USER_MODEL, verbose_name='设备工程师')),
            ],
            options={
                'verbose_name': '702设备主档',
                'verbose_name_plural': '702设备主档',
            },
        ),
        migrations.CreateModel(
            name='runstatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(help_text='1：运行，2：维修，3：保养，4：闲置，5：验收，6：校验', max_length=40, verbose_name='状态')),
                ('station', models.CharField(max_length=80, verbose_name='位置')),
                ('starttime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='开始时间')),
                ('endtime', models.DateTimeField(blank=True, null=True, verbose_name='结束时间')),
                ('updatename', models.CharField(blank=True, max_length=40, verbose_name='添加者')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runstatus', to='p_ems.equipment', verbose_name='设备')),
            ],
            options={
                'verbose_name': '706运行状态',
                'verbose_name_plural': '706运行状态',
            },
        ),
        migrations.CreateModel(
            name='station',
            fields=[
                ('station', models.CharField(max_length=80, primary_key=True, serialize=False, verbose_name='位置编码')),
                ('location', models.CharField(default=1, help_text='当同一个工作中心，有多个工站时，使用区别码', max_length=40, verbose_name='区别码')),
                ('stationdesc', models.TextField(blank=True, null=True, verbose_name='备注')),
                ('updatetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('PIC', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='station4', to=settings.AUTH_USER_MODEL, verbose_name='保管人')),
                ('cell', models.ForeignKey(blank=True, limit_choices_to=models.Q(category='C'), null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='station2', to='p_admin.department', verbose_name='Cell')),
                ('dep', models.ForeignKey(blank=True, limit_choices_to=models.Q(_negated=True, category='C'), null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='station1', to='p_admin.department', verbose_name='部门')),
                ('operation', models.ForeignKey(blank=True, limit_choices_to=models.Q(category='2'), null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='station3', to='p_pdm.operation', verbose_name='工作中心')),
            ],
            options={
                'verbose_name': '703工站位置',
                'verbose_name_plural': '703工站位置',
            },
        ),
        migrations.CreateModel(
            name='tpmitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mcode', models.CharField(max_length=40, verbose_name='设备类')),
                ('mitem', models.CharField(max_length=120, verbose_name='项目')),
                ('mcontent', models.TextField(max_length=120, verbose_name='内容和方法')),
                ('mspec', models.CharField(max_length=120, verbose_name='标准要求')),
                ('category', models.CharField(choices=[('1', '日常点检'), ('2', '定期保养'), ('3', '预防校验')], default=1, max_length=20, verbose_name='分类')),
                ('period', models.SmallIntegerField(default=1, verbose_name='间隔天数')),
                ('createtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '704维护项目',
                'verbose_name_plural': '704维护项目',
            },
        ),
        migrations.CreateModel(
            name='tpmrecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tpmdate', models.DateField(default=django.utils.timezone.now, verbose_name='日期')),
                ('judge', models.BooleanField(default=1, verbose_name='判定')),
                ('remark', models.CharField(blank=True, max_length=200, null=True, verbose_name='备注')),
                ('updatename', models.CharField(blank=True, max_length=40, verbose_name='添加者')),
                ('createtime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tpmrecords1', to='p_ems.equipment', verbose_name='设备')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='tpmrecords2', to='p_ems.tpmitem', verbose_name='项目')),
            ],
            options={
                'verbose_name': '707检修记录',
                'verbose_name_plural': '707检修记录',
            },
        ),
        migrations.CreateModel(
            name='troublecode',
            fields=[
                ('troublecode', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='故障代码')),
                ('troublename', models.CharField(max_length=80, verbose_name='故障状况')),
                ('updatetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('PIC', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='troublecode', to=settings.AUTH_USER_MODEL, verbose_name='维修人')),
            ],
            options={
                'verbose_name': '708故障代码',
                'verbose_name_plural': '708故障代码',
            },
        ),
        migrations.CreateModel(
            name='troublerecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('troubledesc', models.TextField(blank=True, null=True, verbose_name='故障描述')),
                ('createname', models.CharField(blank=True, max_length=40, verbose_name='故障发现者')),
                ('confirm', models.CharField(blank=True, max_length=40, verbose_name='故障确认者')),
                ('Repair', models.TextField(blank=True, verbose_name='修复方案')),
                ('confirmtime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='确认时间')),
                ('dispose', models.CharField(choices=[('1', '厂内维修'), ('2', '发外维修'), ('3', '限制使用'), ('4', '申请报废'), ('0', '其它')], default=1, max_length=80, verbose_name='处置措施')),
                ('status', models.CharField(choices=[('1', '故障确认中'), ('2', '方案审核中'), ('3', '设备维修中'), ('4', '设备验收中'), ('5', '结案')], default=1, max_length=40, verbose_name='处置状态')),
                ('remark', models.TextField(blank=True, verbose_name='备注')),
                ('updatetime', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='更新时间')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='troublerecords1', to='p_ems.equipment', verbose_name='设备')),
                ('trouble', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='troublerecords2', to='p_ems.troublecode', verbose_name='故障')),
            ],
            options={
                'verbose_name': '709故障记录',
                'verbose_name_plural': '709故障记录',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='equipment',
            field=models.ManyToManyField(blank=True, null=True, related_name='tpmcategory2', to='p_ems.equipment', verbose_name='设备清单'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='p_ems.category', verbose_name='主分类'),
        ),
        migrations.AddField(
            model_name='category',
            name='tpm',
            field=models.ManyToManyField(blank=True, null=True, related_name='tpmcategory1', to='p_ems.tpmitem', verbose_name='TPM项目'),
        ),
    ]
