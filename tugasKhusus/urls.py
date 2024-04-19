from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('main', views.Main, name = "Main-Page"),
    path("login", views.LoginPage, name="Login-Page"),
    path("InfoUser", views.InfoUser, name="Info-User"),
    path("NilaiSiswa", views.NilaiSiswaFunction, name="Nilai-Siswa"),
    path("Presensi", views.Presensi_Function, name="Presensi"),
    path("Presensi/<int:id> <str:namaKelas> <str:kodeMapel>", views.PresensiDetail_Function),
    path("Presensi/<int:id> <str:namaKelas> <str:kodeMapel>/InsertPresensi", views.InsertPresensi_Function),
    path("LogOut", views.LogOut, name = "Log-Out")
]