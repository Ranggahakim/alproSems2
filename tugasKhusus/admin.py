from django.contrib import admin

# Register your models here.
from .models import Siswa, NilaiSiswa, Presensi, BabPengajaran, DaftarSiswaKelas, Kelas, Guru, KomponenPenilaian, MataPelajaran, Karyawan, Kurikulum, User, Feedback

admin.site.register(Siswa)
admin.site.register(NilaiSiswa)
admin.site.register(Presensi)
admin.site.register(BabPengajaran)
admin.site.register(DaftarSiswaKelas)
admin.site.register(Kelas)
admin.site.register(Guru)
admin.site.register(KomponenPenilaian)
admin.site.register(MataPelajaran)
admin.site.register(Karyawan)
admin.site.register(Kurikulum)
admin.site.register(User)
admin.site.register(Feedback)