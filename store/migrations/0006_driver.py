# Generated by Django 5.0.2 on 2024-04-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_address_locations_order_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=20)),
                ('car_registration', models.CharField(max_length=20)),
                ('car_make', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='driver_images')),
            ],
        ),
    ]
