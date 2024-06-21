# Generated by Django 5.0.6 on 2024-06-20 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel', '0003_trip_image_delete_tripimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='image',
        ),
        migrations.AlterField(
            model_name='trip',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='TripImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='trip_images/')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='travel.trip')),
            ],
        ),
    ]