# Generated by Django 5.1.3 on 2024-11-19 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lims_app', '0005_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='news_images/'),
        ),
        migrations.AlterField(
            model_name='reader',
            name='reader_address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='reader',
            name='reader_contact',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='reader',
            name='reader_name',
            field=models.CharField(max_length=255),
        ),
    ]
