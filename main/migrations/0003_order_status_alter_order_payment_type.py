# Generated by Django 4.0 on 2022-01-07 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.BooleanField(default=False, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('in-place', 'پرداخت در محل'), ('online', 'پرداخت آنلاین')], default='online', max_length=8, verbose_name='نوع پرداخت'),
        ),
    ]
