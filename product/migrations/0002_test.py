# Generated by Django 5.0.2 on 2024-02-19 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('descriptions', models.TextField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
