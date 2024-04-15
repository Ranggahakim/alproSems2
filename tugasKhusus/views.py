import os


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.conf import settings
from .forms import BabPengajaranForm

from .models import generate_filename
from .models import Siswa, NilaiSiswa, Presensi, BabPengajaran, DaftarSiswaKelas, Kelas, Guru, MappingGuru, KomponenPenilaian, MataPelajaran, Karyawan, Kurikulum, User, Feedback

global_isLogin = False
global_loginUser = None
global_userType = None

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

        Input_username = request.POST.get('username')
        Input_password = request.POST.get('password')

        #return HttpResponse(Input_nik)
        try:
            loginUser = User.objects.filter(username = Input_username).get()
        except:
            return HttpResponse("User tidak ditemukan!")
        else:
            #return HttpResponse(loginSiswa)
            if loginUser.password == Input_password:
                
                global global_isLogin
                global_isLogin = True

                global global_loginUser
                global_loginUser = loginUser
                
                
                return HttpResponse(InfoUser(loginUser, request))
            else:
                return HttpResponseRedirect('login')
    else:
        if global_isLogin == True:
            return HttpResponse(InfoUser(global_loginUser, request))
        else:
            return HttpResponseRedirect('login')



def InfoUser(user, request):
    
    listRole = {"Siswa": Siswa, "Guru": Guru, "Karyawan": Karyawan}

    userType = str()
    kelasSiswa = None
    daftarSiswaKelas = None
    kelasGuru = None

    for key, value in listRole.items():
        try:
            userData = value.objects.filter(nik = user.nik).get()
            userType = str(key)
        except:
            continue
        else:
            break

    if userData == None:
        userType = 'not found'

    global global_userType
    global_userType = userType

    if userType == "Siswa":
        kelasSiswa = DaftarSiswaKelas.objects.filter(siswa = user.nik).get().Kelas.nama

    if userType == "Guru":
        try:
            kelasGuru = Kelas.objects.filter(wali_kelas = user.nik).get()
            daftarSiswaKelas = DaftarSiswaKelas.objects.filter(Kelas = kelasGuru.id).all()
        except:
            print("Guru bukan seorang walas")



    context = {'userData':userData, 'userType':userType, "kelasSiswa": kelasSiswa, "kelasGuru":kelasGuru, "daftarSiswaKelas": daftarSiswaKelas}
    template = loader.get_template('Info_User.html')

    return HttpResponse(template.render(context, request))


def NilaiSiswaFunction(request):
   
   if global_userType == "Siswa" and global_isLogin == True:
        
    nilai = NilaiSiswa.objects.filter(siswa = global_loginUser.nik ).all()

    context = {"siswa": Siswa.objects.filter(nik = global_loginUser.nik).get(), "nilai": nilai, "userType": global_userType}
    
    template = loader.get_template('nilai_Siswa_Page.html')
    return HttpResponse(template.render(context, request))
        
    # return HttpResponse(mapel)
   else: 
       return HttpResponseRedirect('InfoUser')

def Presensi_Function(request):

    if global_userType == "Guru" and global_isLogin == True:

        mapping = MappingGuru.objects.filter(guru__nik = global_loginUser.nik).all()
        
        context = {"userType": global_userType, "mapping":mapping}

        template = loader.get_template('Presensi_Page.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')

def PresensiDetail_Function(request, id, namaKelas, namaMapel):

    if global_userType == "Guru" and global_isLogin == True:
        submitted = False
        if request.method == "POST":
            
            bpForm = BabPengajaranForm(request.POST, request.FILES)
            
            DaftarSiswa = DaftarSiswaKelas.objects.filter(Kelas__id = id).all()
        


            if bpForm.is_valid():
                
                bpForm.instance.kelas = Kelas.objects.filter(nama = namaKelas).get()
                bpForm.instance.mata_pelajaran = MataPelajaran.objects.filter(kode = namaMapel).get()

            
                bpForm.save(commit=True)

                for x in DaftarSiswa:
                    Presensi(mata_pelajaran = MataPelajaran.objects.filter(kode=namaMapel).get(), siswa = Siswa.objects.filter(nik=x.siswa.nik).get(), pertemuan_ke = bpForm.instance, presensi = int(request.POST.get('presensi_' + x.siswa.nik))).save()
                
                return HttpResponseRedirect('?submitted=True')
            
            
                # return HttpResponse(bpForm.cleaned_data['id'])
        else:
        
            bpForm = BabPengajaranForm
            
            if 'sumbitted' in request.GET:
                submitted = True

        mapping = DaftarSiswaKelas.objects.filter(Kelas__id = id).all()
        
        context = {"userType": global_userType, "mapping":mapping, "id":id, "namaKelas":namaKelas, "mapel":namaMapel, 'bpForm':bpForm, 'submitted':submitted}

        template = loader.get_template('PresensiDetail_Page.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')

def MasukkanPresensi(request):

    if global_userType == "Guru" and global_isLogin == True:


        context = {"userType": global_userType}

        template = loader.get_template('MasukkanPresensi_Page.html')
        return HttpResponse(template.render(context, request))

    else: 
       return HttpResponseRedirect('InfoUser')


def InsertPresensi(request, id, mapel):

    if global_userType == "Guru" and global_isLogin == True and request.method == "POST":

        DaftarSiswa = DaftarSiswaKelas.objects.filter(Kelas__id = id).all()
        

        for x in DaftarSiswa:
            Presensi(mata_pelajaran = MataPelajaran.objects.filter(id=mapel).get(), siswa = Siswa.objects.filter(nik=x.siswa.nik).get(), pertemuan_ke = request.POST.get('pertemuan'), presensi = request.POST.get(x.siswa.nik)).save()

        

        
        return HttpResponse("Data Sudah Disimpan")

    else: 
       return HttpResponseRedirect('InfoUser')



def LogOut(request):
    global global_isLogin, global_loginUser, global_userType
    global_isLogin = False
    global_loginUser = None
    global_userType = None

    # return HttpResponse("User tidak ditemukan!")

    # return reverse("Login-Page")

    return HttpResponseRedirect('login')