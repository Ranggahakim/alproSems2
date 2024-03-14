from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Siswa, NilaiSiswa, Presensi, BabPengajaran, DaftarSiswaKelas, Kelas, Guru, KomponenPenilaian, MataPelajaran, Karyawan, Kurikulum, User, Feedback

def index(request):
    return HttpResponse("Hello, world. You're at the Tugas Khusus index.")

def Main(request):
    allSiswa = Siswa.objects.all().values()
    allNilai = NilaiSiswa.objects.all()
    allPresensi = Presensi.objects.all()
    allBabPengajaran = BabPengajaran.objects.all()
    allSiswaKelas = DaftarSiswaKelas.objects.all()
    allKelas = Kelas.objects.all()
    allGuru = Guru.objects.all()
    allKomponenPenilaian = KomponenPenilaian.objects.all()
    allMataPelajaran = MataPelajaran.objects.all()
    allKaryawan = Karyawan.objects.all()
    allKurikulum = Kurikulum.objects.all()
    allUser = User.objects.all()
    allFeedback = Feedback.objects.all()
    
    template = loader.get_template('main.html')
    
    context = {'allSiswa': allSiswa, 
               'allNilai': allNilai,
               'allPresensi': allPresensi,
               'allBabPengajaran': allBabPengajaran,
               'allSiswaKelas': allSiswaKelas,
               'allKelas':allKelas,
               'allGuru':allGuru,
               'allKomponenPenilaian':allKomponenPenilaian,
               'allMataPelajaran':allMataPelajaran,
               'allKaryawan':allKaryawan,
               'allKurikulum':allKurikulum,
               'allUser':allUser,
               'allFeedback':allFeedback}
    
    return HttpResponse(template.render(context, request))

def LoginPage(request):
    allSiswa = Siswa.objects.all().values()

    template = loader.get_template('login.html')

    context = {'allSiswa': allSiswa}


    return HttpResponse(template.render(context, request))

def AuthProcess(request):
    
    if request.method == "POST":

        Input_nik = request.POST.get('nik')

        #return HttpResponse(Input_nik)
        try:
            loginSiswa = Siswa.objects.filter(nik = Input_nik).get()
        except:
            return HttpResponse("GAGAL!")
        else:
            #return HttpResponse(loginSiswa)
            return HttpResponse(Info_SiswaPage(loginSiswa, request))
    else:
        return HttpResponseRedirect('login')



def Info_SiswaPage(siswa, request):

    namaKelas = DaftarSiswaKelas.objects.filter(siswa= siswa.nik).get().Kelas.nama

    context = {'Siswa': siswa, 'namaKelas':namaKelas}
    template = loader.get_template('Info_Siswa.html')

    return HttpResponse(template.render(context, request))
    
    
    #return HttpResponse(idKelasSiswa.Kelas.nama)