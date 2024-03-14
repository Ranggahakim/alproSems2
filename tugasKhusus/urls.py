from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('main', views.Main, name = "Main Page"),
    path("login", views.LoginPage, name="Login Page"),
    path("InfoSiswa", views.AuthProcess, name="Info-Siswa-Page"),
]