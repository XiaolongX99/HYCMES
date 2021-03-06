# Generated by Django 2.0.4 on 2018-07-13 12:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('p_pdm', '0004_auto_20180712_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='itempcodespec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('spec', models.CharField(blank=True, max_length=200, null=True, verbose_name='描述')),
                ('UCL', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=8, null=True, verbose_name='上限值')),
                ('CL', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=8, null=True, verbose_name='中心值')),
                ('LCL', models.DecimalField(blank=True, decimal_places=4, default=0, max_digits=8, null=True, verbose_name='下限值')),
                ('updatename', models.CharField(blank=True, max_length=40, verbose_name='添加者')),
                ('updatetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': '210参数规格',
                'verbose_name_plural': '210参数规格',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='itemgroup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='itemgroups', to='p_pdm.item', verbose_name='共用号'),
        ),
        migrations.AlterField(
            model_name='itemparameter',
            name='parameter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='itemparameter', to='p_pdm.parameter', verbose_name='参数'),
        ),
        migrations.AlterField(
            model_name='itemparameter',
            name='spec',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='描述'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='parameter',
            field=models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='参数'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='pmproperty',
            field=models.CharField(choices=[('1', '通用参数'), ('2', '标准参数')], default=1, help_text='1:通用参数，如进出烘箱时间；2:标准参数，如产品测试值。', max_length=20, null=True, verbose_name='特征'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='process',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(category='2'), null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='parameter', to='p_pdm.operation', verbose_name='所属'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='spec',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='描述'),
        ),
        migrations.AddField(
            model_name='itempcodespec',
            name='parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='specparam', to='p_pdm.parameter', verbose_name='参数'),
        ),
        migrations.AddField(
            model_name='itempcodespec',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='specroute', to='p_pdm.itempcode', verbose_name='途程'),
        ),
        migrations.AddField(
            model_name='itempcode',
            name='parameter',
            field=models.ManyToManyField(through='p_pdm.itempcodespec', to='p_pdm.parameter', verbose_name='参数'),
        ),
        migrations.AlterUniqueTogether(
            name='itempcodespec',
            unique_together={('route', 'parameter')},
        ),
    ]
