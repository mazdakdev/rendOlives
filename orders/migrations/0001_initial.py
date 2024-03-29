# Generated by Django 3.2.3 on 2022-02-06 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=120)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_num', models.CharField(max_length=11)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(max_length=100)),
                ('ostan', models.CharField(max_length=100)),
                ('postal_code', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField()),
                ('extra_desc', models.TextField(blank=True, null=True)),
                ('country', models.CharField(max_length=100)),
                ('is_paid', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('در حال انجام', 'در حال انحام'), ('تکمیل شده', 'تکمیل شده'), ('لغو شده', 'لغو شده'), ('معلق', 'معلق')], default='در حال انجام', max_length=120)),
                ('method', models.CharField(choices=[('ارسال معمولی', 'ارسال معمولی'), ('ارسال رایگان', 'ارسال رایگان'), ('تیپاکس', 'تیپاکس')], default='ارسال معمولی', max_length=120)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
            ],
        ),
    ]
