from django.urls import path

from . import views

from django.contrib.staticfiles.urls import static
# from django.contrib.staticfiles.urls import 


urlpatterns = [
    path("", views.index, name="index"),
    path('main', views.Main, name = "Main-Page"),
    path("login", views.LoginPage, name="Login-Page"),
    path("InfoUser", views.InfoUser, name="Info-User"),
    path("NilaiSiswa", views.NilaiSiswaFunction, name="Nilai-Siswa"),
    path("Presensi", views.Presensi_Function, name="Presensi"),
    path("Presensi/<str:nikGuru> <int:kelasId> <str:namaKelas> <str:kodeMapel>", views.PresensiDetail_Function),
    path("Presensi/<str:nikGuru> <int:kelasId> <str:namaKelas> <str:kodeMapel>/InsertPresensi", views.InsertPresensi_Function),
    path("Presensi/<str:nikGuru> <int:pertemuanId> <str:idMapel>/UpdatePresensi", views.UpdatePresensi_Function),
    path("Presensi/<str:nikGuru> <int:pertemuanId> <str:idMapel>/DeletePresensi", views.DeletePresensi_Function),
    path("InsertFeedback", views.InsertFeedback, name="Insert-Feedback"),
    path("LogOut", views.LogOut, name = "Log-Out")
]