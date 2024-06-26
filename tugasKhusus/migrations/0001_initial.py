# Generated by Django 5.0.3 on 2024-03-12 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Siswa',
            fields=[
                ('nik', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('nama', models.CharField(max_length=255)),
                ('nis', models.CharField(max_length=16)),
                ('gender', models.BooleanField(default=True)),
                ('tempat_lahir', models.CharField(max_length=255)),
                ('tanggal_lahir', models.DateTimeField(verbose_name='Tanggal Lahir')),
                ('alamat', models.CharField(max_length=255)),
                ('no_telepon', models.CharField(max_length=32)),
                ('agama', models.CharField(max_length=50)),
                ('tahun_masuk', models.CharField(max_length=4, verbose_name='Tahun Masuk')),
                ('wali', models.CharField(max_length=255, verbose_name='Nama Wali Siswa')),
                ('alamat_wali', models.CharField(max_length=255, verbose_name='Alamat Wali Siswa')),
                ('no_telepon_wali', models.CharField(max_length=32, verbose_name='No Telepon Wali')),
                ('ayah', models.CharField(max_length=255, verbose_name='Ayah Siswa')),
                ('ibu', models.CharField(max_length=255, verbose_name='Ibu Siswa')),
            ],
        ),
        migrations.CreateModel(
            name='NilaiSiswa',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='ID Nilai Siswa')),
                ('komponen_penilaian', models.IntegerField(verbose_name='Komponen Penilaian')),
                ('nilai', models.IntegerField(verbose_name='Nilai Siswa')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tugasKhusus.siswa')),
            ],
        ),
    ]
