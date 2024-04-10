from django.db import models

# Create your models here.

class Siswa(models.Model):
    nik = models.CharField(max_length = 16, primary_key = True)
    nama = models.CharField(max_length = 255)
    nis = models.CharField(max_length = 16, unique=True)
    gender = models.BooleanField(default=True) #true = male, false = female
    tempat_lahir = models.CharField(max_length = 255)
    tanggal_lahir = models.DateTimeField("Tanggal Lahir")
    alamat = models.CharField(max_length = 255)
    no_telepon = models.CharField(max_length = 32)
    agama = models.CharField(max_length = 50)
    tahun_masuk = models.CharField(("Tahun Masuk"), max_length=4)
    wali = models.CharField(("Nama Wali Siswa"), max_length=255)
    alamat_wali = models.CharField(("Alamat Wali Siswa"), max_length=255)
    no_telepon_wali = models.CharField(("No Telepon Wali"), max_length=32)
    ayah = models.CharField(("Ayah Siswa"), max_length=255)
    ibu = models.CharField(("Ibu Siswa"), max_length=255)

class NilaiSiswa(models.Model):
    id = models.AutoField(("ID Nilai Siswa"), primary_key = True, auto_created = True, serialize = False)
    siswa = models.ForeignKey("Siswa", on_delete=models.CASCADE)
    komponen_penilaian = models.ForeignKey("KomponenPenilaian", on_delete=models.CASCADE)
    nilai = models.IntegerField(("Nilai Siswa"))

class Presensi(models.Model):
    id = models.AutoField(("ID Presensi"), primary_key=True, auto_created=True, serialize=False)
    mata_pelajaran = models.ForeignKey("MataPelajaran", on_delete=models.CASCADE)
    siswa = models.ForeignKey("Siswa", on_delete=models.CASCADE, to_field='nis')
    pertemuan_ke = models.ForeignKey("BabPengajaran", on_delete=models.CASCADE)
    presensi = models.IntegerField(("Integer Presensi?")) #=============================================== presensi jadi integer? ==========================================

class BabPengajaran(models.Model):
    id = models.AutoField(("ID Pengajaran"), primary_key = True, auto_created = True, serialize = False)
    kelas = models.ForeignKey("Kelas", on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey("MataPelajaran", on_delete=models.CASCADE)
    pertemuan_ke = models.IntegerField(("Pertemuan Ke-"))
    tanggal = models.DateField(("Tanggal Bab Pengajaran"))
    foto = models.CharField(("Foto Pengajaran"), max_length=50) #==================================================== foto jadi VarChar?===============================
    status = models.IntegerField(("Status Pengajaran"))
    materi = models.IntegerField(("Materi Pengajaran"))
    catatan_tambahan = models.CharField(("Catatan Tambahan Pengajaran"), max_length=255)

class DaftarSiswaKelas(models.Model):
    id = models.AutoField(("ID Daftar Siswa Kelas"), primary_key=True, auto_created=True, serialize=False)
    siswa = models.ForeignKey("Siswa", on_delete=models.CASCADE)
    Kelas = models.ForeignKey("Kelas", on_delete=models.CASCADE)

class Kelas(models.Model):
    id = models.AutoField(("ID Kelas"), primary_key=True, auto_created=True, serialize=False)
    nama = models.CharField(("Nama Kelas"), max_length=50)
    tahun = models.CharField(("Tahun adanya Kelas"), max_length=4)
    ketua_murid = models.ForeignKey("Siswa", on_delete=models.CASCADE)
    wali_kelas = models.ForeignKey("Guru", on_delete=models.CASCADE)

class MappingGuru(models.Model):
    id = models.AutoField(("ID Kelas Yang Diampu"),primary_key=True, auto_created=True, serialize=False)
    guru = models.ForeignKey("Guru", on_delete=models.CASCADE)
    mata_pelajaran = models.ForeignKey("MataPelajaran", on_delete=models.CASCADE, default=None)
    kelas = models.ForeignKey("Kelas", on_delete=models.CASCADE)


class Guru(models.Model):
    nik = models.CharField(("NIK Guru"), max_length=16, primary_key=True)
    nama = models.CharField(("Nama Guru"), max_length=255)
    nomor_induk_guru = models.CharField(("Nomor Induk Guru"), max_length=50)
    nomor_induk_pegawai = models.CharField(("Nomor Induk Pegawai"), max_length=50)
    gender = models.BooleanField("Gender Guru", default=True) # True = male, False = female
    tempat_lahir = models.CharField(("Tempat Lahir Guru"), max_length=255)
    tanggal_lahir = models.DateTimeField(("Tanggal Lahir Guru"))
    alamat = models.CharField(("Alamat Guru"), max_length=255)
    no_telepon = models.CharField(("No Telepon Guru"), max_length=32)
    agama = models.CharField(("Agama Guru"), max_length=50)
    tahun_masuk = models.CharField(("Tahun Masuk Guru"), max_length=4)

class KomponenPenilaian(models.Model):
    id = models.AutoField(("ID Komponen Penilaian"), primary_key = True, auto_created = True, serialize = False)
    nama = models.CharField(("Nama Komponen Penilaian"), max_length=255)
    mata_pelajaran = models.ForeignKey("MataPelajaran", on_delete=models.CASCADE)
    guru = models.ForeignKey("Guru", on_delete=models.CASCADE)
    bobot = models.IntegerField(("Bobot Komponen Penilaian"))

class MataPelajaran(models.Model):
    id = models.AutoField(("ID Mata Pelajaran"), primary_key = True, auto_created = True, serialize = False)
    kode = models.CharField(("Kode Mata Pelajaran"), max_length=50)
    nama = models.CharField(("Nama Mata Pelajaran"), max_length=255)
    kurikulum = models.ForeignKey("Kurikulum", on_delete=models.CASCADE)
    tahun_pelaksanaan = models.CharField(("Tahun Pelaksanaan Mata Pelajaran"), max_length=4)

class Karyawan(models.Model):
    nik = models.CharField(("NIK Karyawan"), max_length=16, primary_key=True)
    nama = models.CharField(("Nama Karyawan"), max_length=255)
    nomor_induk_pegawai = models.CharField(("NIP Karyawan"), max_length=50)
    gender = models.BooleanField("Gender Karyawan", default=True) # True = Male, False, female
    tempat_lahir = models.CharField(("Tempat Lahir Karyawan"), max_length=255)
    tanggal_lahir = models.DateField(("Tanggal Lahir Karyawan"))
    alamat = models.CharField(("Alamat Karyawan"), max_length=255)
    no_telepon = models.CharField(("No Telepon Karyawan"), max_length=50)
    agama = models.CharField(("Agama Karyawan"), max_length=50)
    tahun_masuk = models.CharField(("Tahun Masuk Karyawan"), max_length=4)

class Kurikulum(models.Model):
    id = models.AutoField(("ID Kurikulum"), primary_key = True, auto_created = True, serialize = False)
    nama = models.CharField(("Nama Kurikulum"), max_length=255)
    tahun_mulai_berlaku = models.CharField(("Tahun Kurikulum Mulai Berlaku"), max_length=4)

class User(models.Model):
    nik = models.CharField(("NIK User"), max_length=16, primary_key=True)
    username = models.CharField(("Username"), max_length=50)
    password = models.CharField(("Password"), max_length=50)

class Feedback(models.Model):
    id = models.AutoField(("ID Feedback"), auto_created = True, serialize = False, primary_key=True)
    nik = models.ForeignKey("User", on_delete=models.CASCADE)
    feedback = models.CharField(("Feedback"), max_length=255)
    date = models.DateTimeField(("Feedback date"), auto_now=False, auto_now_add=False)