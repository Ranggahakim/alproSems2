# Generated by Django 4.2.11 on 2024-04-22 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tugasKhusus', '0007_alter_babpengajaran_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='babpengajaran',
            name='foto',
            field=models.ImageField(upload_to='uploads/', verbose_name='Foto Pengajaran'),
        ),
    ]