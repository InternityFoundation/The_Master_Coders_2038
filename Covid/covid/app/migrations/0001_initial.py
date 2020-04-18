# Generated by Django 2.2.6 on 2019-12-31 17:48

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
            name='available_items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Hostel', models.CharField(max_length=20)),
                ('item_name', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('hostel_num', models.IntegerField(default=1)),
                ('quantity', models.IntegerField(default=10)),
            ],
        ),
        migrations.CreateModel(
            name='Hostel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('hostel_num', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0)),
                ('phone', models.IntegerField(default=0)),
                ('name', models.CharField(default='student', max_length=20)),
                ('email', models.EmailField(default='@thapar.edu', max_length=100)),
                ('Hostel', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='app.Hostel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProperOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_timestamp', models.DateTimeField(auto_now_add=True)),
                ('order_price', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=10)),
                ('order_done', models.BooleanField(default=False)),
                ('hos', models.CharField(max_length=10, null=True)),
                ('order_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('already_ordered', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, editable=False, max_digits=4)),
                ('quantity', models.IntegerField(default=1)),
                ('hostell', models.CharField(max_length=10, null=True)),
                ('total', models.DecimalField(decimal_places=0, default=0.0, editable=False, max_digits=4)),
                ('add_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('in_order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='app.ProperOrder')),
                ('itemtype', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.available_items')),
            ],
        ),
    ]