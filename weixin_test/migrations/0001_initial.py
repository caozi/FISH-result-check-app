# Generated by Django 2.2.4 on 2019-08-13 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_text', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(max_length=200, unique=True)),
                ('patient_name', models.CharField(max_length=200)),
                ('patient_age', models.IntegerField()),
                ('patient_gender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin_test.Gender')),
                ('patient_result', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='weixin_test.Result')),
                ('patient_test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='weixin_test.Test')),
            ],
        ),
    ]
