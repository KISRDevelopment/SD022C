# Generated by Django 4.2.2 on 2023-12-25 06:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentName', models.CharField(max_length=60)),
                ('sex', models.CharField(max_length=60)),
                ('schoolName', models.CharField(max_length=60)),
                ('grade', models.CharField(max_length=60)),
                ('civilID', models.IntegerField()),
                ('eduDistrict', models.CharField(max_length=60)),
                ('nationality', models.CharField(max_length=60)),
                ('examDate', models.DateField(max_length=60)),
                ('birthDate', models.DateField(max_length=60)),
                ('age', models.CharField(max_length=60)),
                ('examiner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examiner_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rpdNOA_startT', models.DateTimeField(null=True)),
                ('rpdNOA_endT', models.DateTimeField(null=True)),
                ('rpdNOA_wrongAns', models.IntegerField(null=True)),
                ('rpdNOA_reason', models.CharField(max_length=60, null=True)),
                ('rpdNOB_startT', models.DateTimeField(null=True)),
                ('rpdNOB_endT', models.DateTimeField(null=True)),
                ('rpdNOB_wrongAns', models.IntegerField(null=True)),
                ('rpdNOB_reason', models.CharField(max_length=60, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='primary.student')),
            ],
        ),
        migrations.CreateModel(
            name='Examiner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('speciality', models.CharField(max_length=60)),
                ('organization', models.CharField(max_length=60)),
                ('stage', models.CharField(choices=[('PRIMARY', 'Primary School'), ('SECONDARY', 'Secondary School'), ('BOTH', 'Primary/Secondary')], default='PRIMARY', max_length=20)),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin_id', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
