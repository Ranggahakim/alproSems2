# Generated by Django 4.2.11 on 2024-03-26 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tugasKhusus', '0005_rename_kelasyangdiampuguru_mappingguru'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappingguru',
            name='mata_pelajaran',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tugasKhusus.matapelajaran'),
        ),
    ]
