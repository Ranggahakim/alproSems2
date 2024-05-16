from django.urls import path

from . import views

from django.contrib.staticfiles.urls import static
# from django.contrib.staticfiles.urls import 


urlpatterns = [
    # You can delete These
    path("", views.index, name="index"),
    path('main', views.Main, name = "Main-Page"),

    # Login Page
    path("login", views.LoginPage, name="Login-Page"),
    path("InfoUser", views.InfoUser, name="Info-User"),
    
    # View Nilai when UserType == Siswa
    path("NilaiSiswa", views.NilaiSiswaFunction, name="Nilai-Siswa"),
    
    # Presensi when UserType == Guru
    path("Presensi", views.Presensi_Function, name="Presensi"),
    path("Presensi/<str:nikGuru> <int:kelasId> <str:namaKelas> <str:kodeMapel>", views.PresensiDetail_Function),
    path("Presensi/<str:nikGuru> <int:kelasId> <str:namaKelas> <str:kodeMapel>/InsertPresensi", views.InsertPresensi_Function),
    path("Presensi/<str:nikGuru> <int:pertemuanId> <str:idMapel>/UpdatePresensi", views.UpdatePresensi_Function),
    path("Presensi/<str:nikGuru> <int:pertemuanId> <str:idMapel>/DeletePresensi", views.DeletePresensi_Function),
    
    # Penilaian when UserType == Guru
    path("Penilaian", views.Penilaian_Function),
    path("Penilaian/<str:kodeMapel> <str:nikGuru>", views.PenilaianDetail_Function),
    path("Penilaian/<str:kodeMapel> <str:nikGuru>/InsertKomponenPenilaian", views.InsertKomponenPenilaian_Function),
    
    # Insert nilai when UserType == Guru
    path("Penilaian/<str:kodeMapel> <str:nikGuru>/<str:namaKomPenilaian> <str:idKomPenilaian>", views.KomPenilaian_Function),
    path("Penilaian/<str:kodeMapel> <str:nikGuru>/<str:namaKomPenilaian> <str:idKomPenilaian>/<str:namaKelas> <str:idKelas>", views.KomPenilaianDetail_Function),

    # Insert Feedback when semua UserType
    path("InsertFeedback", views.InsertFeedback, name="Insert-Feedback"),

    # Log Out
    path("LogOut", views.LogOut, name = "Log-Out")
]