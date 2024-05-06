import os


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.conf import settings
from .forms import BabPengajaranForm, UserForm, FeedbackForm

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
    isUserNotExist = False
    isPasswordWrong = False

    if request.method == 'POST':
    
        userForm = UserForm(request.POST)

        if userForm.is_valid():
            Input_username = userForm.instance.username
            Input_password = userForm.instance.password

            # return HttpResponse(Input_username)
            try:
                loginUser = User.objects.filter(username = Input_username).get()
            except:
                isUserNotExist = True
                return HttpResponseRedirect("login?isUserNotExist=True")
            else:
                #return HttpResponse(loginSiswa)
                if loginUser.password == Input_password:
                    
                    global global_isLogin
                    global_isLogin = True

                    global global_loginUser
                    global_loginUser = loginUser
                    
                    
                    return HttpResponseRedirect('InfoUser')
                else:
                    return HttpResponseRedirect("login?isPasswordWrong=True")

    else:
        if 'isUserNotExist' in request.GET:
            isUserNotExist = True
        if 'isPasswordWrong' in request.GET:
            isPasswordWrong = True

        userForm = UserForm
        context = {'userForm':userForm, 'isUserNotExist':isUserNotExist, 'isPasswordWrong':isPasswordWrong}

        template = loader.get_template('login.html')
        return HttpResponse(template.render(context, request))


def InfoUser(request):
    
    listRole = {"Siswa": Siswa, "Guru": Guru, "Karyawan": Karyawan}

    userType = str()
    user = global_loginUser

    userData = None
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
        return HttpResponseRedirect('login')

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
        
        context = {"userType": global_userType, "mapping":mapping, 'nikGuru':str(global_loginUser.nik)}

        template = loader.get_template('Presensi_Page.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')
    
def PresensiDetail_Function(request, nikGuru, kelasId, namaKelas, kodeMapel):
    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:

        try:
            daftarPertemuan = BabPengajaran.objects.filter(kelas__id = kelasId, mata_pelajaran__kode = kodeMapel).all()
        except:
            daftarPertemuan = None

        context = {"userType": global_userType, "id":kelasId, "namaKelas":namaKelas, "mapel":kodeMapel, "daftarPertemuan":daftarPertemuan, "nikGuru":nikGuru}

        template = loader.get_template('PresensiDetail_Page.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')



def InsertPresensi_Function(request, nikGuru, kelasId, namaKelas, kodeMapel):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:

        if request.method == "POST":
            
            bpForm = BabPengajaranForm(request.POST, request.FILES)
            
            DaftarSiswa = DaftarSiswaKelas.objects.filter(Kelas__id = kelasId).all()

            if bpForm.is_valid():
                
                bpForm.instance.kelas = Kelas.objects.filter(nama = namaKelas).get()
                bpForm.instance.mata_pelajaran = MataPelajaran.objects.filter(kode = kodeMapel).get()

            
                bpForm.save(commit=True)

                for x in DaftarSiswa:
                    Presensi(mata_pelajaran = MataPelajaran.objects.filter(kode=kodeMapel).get(), siswa = Siswa.objects.filter(nik=x.siswa.nik).get(), pertemuan_ke = bpForm.instance, presensi = int(request.POST.get('presensi_' + x.siswa.nik))).save()
                
                return HttpResponseRedirect('?submitted=True')
            
            
                # return HttpResponse(bpForm.cleaned_data['id'])
        else:
        
            bpForm = BabPengajaranForm

        mapping = DaftarSiswaKelas.objects.filter(Kelas__id = kelasId).all()
        
        context = {"userType": global_userType, "mapping":mapping, "id":kelasId, "namaKelas":namaKelas, "mapel":kodeMapel, 'bpForm':bpForm}

        template = loader.get_template('MasukkanPresensi_Page.html')
        return HttpResponse(template.render(context, request))
        # return HttpResponse(namaKelas)
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')
    
def UpdatePresensi_Function(request, nikGuru, pertemuanId, idMapel):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:

        savedPresensi = BabPengajaran.objects.filter(id = pertemuanId, mata_pelajaran_id = idMapel).get()
        # savedPresensi = BabPengajaran.objects.filter(id = 9, mata_pelajaran_id = 2).values()

        # return HttpResponse(savedPresensi)

        if request.method == "POST":
            
            bpForm = BabPengajaranForm(request.POST, request.FILES, instance=savedPresensi)
            
            DaftarSiswa = Presensi.objects.filter(mata_pelajaran = savedPresensi.mata_pelajaran, pertemuan_ke = savedPresensi.id).all()

            if bpForm.is_valid():
                if not bpForm.cleaned_data['foto']:
                    bpForm.instance.foto =  savedPresensi.foto

                    return HttpResponse(savedPresensi.foto)

                bpForm.save(commit=True)

                for x in DaftarSiswa:
                    x.presensi = int(request.POST.get('presensi_' + x.siswa.nik))
                    x.save()
                
                return redirect(f"/tugasKhusus/Presensi/{nikGuru} {savedPresensi.kelas.id} {savedPresensi.kelas.nama} {savedPresensi.mata_pelajaran.kode}")

            else:    
                return HttpResponse(str(bpForm))
        else:
        
            bpForm = BabPengajaranForm(initial={
                'id':pertemuanId,
                'pertemuan_ke':savedPresensi.pertemuan_ke,
                'tanggal': savedPresensi.tanggal,
                'status': savedPresensi.status,
                'materi': savedPresensi.materi,
                'catatan_tambahan': savedPresensi.catatan_tambahan,
                'kelas': savedPresensi.kelas,
                'mata_pelajaran': savedPresensi.mata_pelajaran,
                'foto': savedPresensi.foto
                })

        mapping = Presensi.objects.filter(mata_pelajaran = savedPresensi.mata_pelajaran, pertemuan_ke = savedPresensi.id).all()

        context = {"userType": global_userType, "mapping":mapping, "namaKelas":savedPresensi.kelas.nama, "mapel":savedPresensi.mata_pelajaran.kode, 'bpForm':bpForm, 'foto':savedPresensi.foto}

        template = loader.get_template('MasukkanPresensi_Page.html')
        return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')

    
def DeletePresensi_Function(request, nikGuru, pertemuanId, idMapel):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:

        savedPresensi = BabPengajaran.objects.filter(id = pertemuanId, mata_pelajaran_id = idMapel).get()

        DaftarSiswa = Presensi.objects.filter(mata_pelajaran = savedPresensi.mata_pelajaran, pertemuan_ke = savedPresensi.id).all()

        for x in DaftarSiswa:
            x.delete()

        savedPresensi.delete()

        return redirect(f"/tugasKhusus/Presensi/{nikGuru} {savedPresensi.kelas.id} {savedPresensi.kelas.nama} {savedPresensi.mata_pelajaran.kode}")    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')

def InsertFeedback(request):
    
    if global_isLogin == True:
        if request.method == 'POST':

            fbForm = FeedbackForm(request.POST)

            if fbForm.is_valid():

                fbForm.instance.nik = global_loginUser

                fbForm.save()

                return redirect("/tugasKhusus/InfoUser")
        else:
            fbForm = FeedbackForm()

        context = {'fbForm':fbForm, 'loginUser':global_loginUser}

        template = loader.get_template('InsertFeedback.html')
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')

def LogOut(request):
    global global_isLogin, global_loginUser, global_userType
    global_isLogin = False
    global_loginUser = None
    global_userType = None

    # return HttpResponse("User tidak ditemukan!")

    # return reverse("Login-Page")

    return HttpResponseRedirect('login')