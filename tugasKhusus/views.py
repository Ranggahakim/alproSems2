import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.conf import settings
from .forms import BabPengajaranForm, UserForm, FeedbackForm, KomponenPenilaianForm

from .models import generate_filename
from .models import Siswa, NilaiSiswa, Presensi, BabPengajaran, DaftarSiswaKelas, Kelas, Guru, MappingGuru, KomponenPenilaian, MataPelajaran, Karyawan, Kurikulum, User, Feedback

# Global Variable, User Info
global_isLogin = False
global_loginUser = None
global_userType = None


# You can delete These
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

# ---------------------------------------------------------------

# Function For Login, and render Login Page
def LoginPage(request):

    # Define Variable
    isUserNotExist = False      # Use when user is not exist
    isPasswordWrong = False     # Use when Password is wrong

    if request.method == 'POST':
    # Execute when press Submit Button

        userForm = UserForm(request.POST)     # Get value of form

        if userForm.is_valid():
            Input_username = userForm.instance.username     # Get value of Username Field 
            Input_password = userForm.instance.password     # Get value of Password Field

            try:
            # Try search user by username
                loginUser = User.objects.filter(username = Input_username).get()

            except:
            # Execute when User Not Exist
                isUserNotExist = True
                return HttpResponseRedirect("login?isUserNotExist=True")
            
            else:
            # Execute when user is Exist

                if loginUser.password == Input_password:
                # Execute if password is correct

                    # Change value of Is_login (global variable) to True
                    global global_isLogin
                    global_isLogin = True

                    # Insert value of User that login (global variable)
                    global global_loginUser
                    global_loginUser = loginUser
                    
                    # Redirect to tugasKhusus/InfoUser
                    return HttpResponseRedirect('InfoUser')
                
                else:
                #Execyte if Passwird us wrong
                    return HttpResponseRedirect("login?isPasswordWrong=True")

    else:
    # Execute when open /tugasKhusus/Login

        # idk what is this :))), but don't delete this (i'm afraid this is important) 
        if 'isUserNotExist' in request.GET:
            isUserNotExist = True
        if 'isPasswordWrong' in request.GET:
            isPasswordWrong = True

        
        userForm = UserForm         # Define variable for Form

        # These are important, just copy paste it
        context = {'userForm':userForm, 'isUserNotExist':isUserNotExist, 'isPasswordWrong':isPasswordWrong} # This is for define variable
    
        template = loader.get_template('login.html')            # this is for define html file that will be open
        return HttpResponse(template.render(context, request)) 


# Function to show Info of User
def InfoUser(request):
    
    listRole = {"Siswa": Siswa, "Guru": Guru, "Karyawan": Karyawan}     # Define list role of user

    userType = str()            # Define userType variable that has string dataType

    # Define variable with null value
    userData = None
    kelasSiswa = None
    daftarSiswaKelas = None
    kelasGuru = None

    for key, value in listRole.items():
    # Get role of user
        try:
            userData = value.objects.filter(nik = global_loginUser.nik).get()   # Try find user in each userType model (Siswa, Guru, and Karyawan)
            userType = str(key)
        except:
            continue
        else:
            break

    if userData == None:
    # If the user is exist in user model, but the data is not exist in userType model (Siswa, Guru, and Karyawan)

        userType = 'not found'                  # Change UserType to 'not found'
        return HttpResponseRedirect('login')    # Back to login Page

    global global_userType      # Get global variable of UserType
    global_userType = userType  # Change value of userType

    if userType == "Siswa":
    # Execute when userType is Siswa

        kelasSiswa = DaftarSiswaKelas.objects.filter(siswa = global_loginUser.nik).get().Kelas.nama     # Get kelas of siswa

    if userType == "Guru":
    # Execute when userType is Guru
        
        try:
        # Try to find kelas when guru is walas

            kelasGuru = Kelas.objects.filter(wali_kelas = global_loginUser.nik).get()           # Try to get kelas when wali kelas is loginUser 
            daftarSiswaKelas = DaftarSiswaKelas.objects.filter(Kelas = kelasGuru.id).all()      # Try to get all siswa from that kelas

        except:
        # Execute if Guru is not walas
            print("Guru bukan seorang walas")


    context = {'userData':userData, 'userType':userType, "kelasSiswa": kelasSiswa, "kelasGuru":kelasGuru, "daftarSiswaKelas": daftarSiswaKelas}
    template = loader.get_template('Info_User.html')

    return HttpResponse(template.render(context, request))


# Function to view nilai of siswa
def NilaiSiswaFunction(request):
   
    if global_userType == "Siswa" and global_isLogin == True:
    # Execute if user is login and he/she is siswa

        nilai = NilaiSiswa.objects.filter(siswa = global_loginUser.nik ).all()      # Get all nilai of user

        context = {"siswa": Siswa.objects.filter(nik = global_loginUser.nik).get(), "nilai": nilai, "userType": global_userType}
        
        template = loader.get_template('nilai_Siswa_Page.html')
        return HttpResponse(template.render(context, request))
            
    else: 
       return HttpResponseRedirect('/tugasKhusus/InfoUser')      # Back to Info User
   

# Function to view Presensi Page
def Presensi_Function(request):

    if global_userType == "Guru" and global_isLogin == True:
    # Execute if user is login and he/she is guru

        mapping = MappingGuru.objects.filter(guru__nik = global_loginUser.nik).all()     # Get all kelas from mapping model when guru is teach on it
        
        context = {"userType": global_userType, "mapping":mapping, 'nikGuru':str(global_loginUser.nik)}

        template = loader.get_template('Presensi_Page.html')
        return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User
    

# Function to view list of pertemuan on that kelas
def PresensiDetail_Function(request, nikGuru, kelasId, namaKelas, kodeMapel):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct

        try:
        # Try to find all data of daftar pertemuan
            daftarPertemuan = BabPengajaran.objects.filter(kelas__id = kelasId, mata_pelajaran__kode = kodeMapel).all()

        except:
            daftarPertemuan = None

        context = {"userType": global_userType, "id":kelasId, "namaKelas":namaKelas, "mapel":kodeMapel, "daftarPertemuan":daftarPertemuan, "nikGuru":nikGuru}

        template = loader.get_template('PresensiDetail_Page.html')
        return HttpResponse(template.render(context, request))
        
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User


# Function to insert presensi
def InsertPresensi_Function(request, nikGuru, kelasId, namaKelas, kodeMapel):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct

        if request.method == "POST":
        # Execute when press submit button
         
            bpForm = BabPengajaranForm(request.POST, request.FILES)     # Get value of form, and the FILE IS FOR PICTURE
            
            DaftarSiswa = DaftarSiswaKelas.objects.filter(Kelas__id = kelasId).all()    # Get value of Daftar siswa on that Kelas

            if bpForm.is_valid():
                
                bpForm.instance.kelas = Kelas.objects.filter(nama = namaKelas).get()                    # Insert kelas to form value
                bpForm.instance.mata_pelajaran = MataPelajaran.objects.filter(kode = kodeMapel).get()   # Inser mapel to form value

            
                bpForm.save(commit=True)        # Save data

                for x in DaftarSiswa:
                # Save presensi data of all Siswa on that kelas
                    Presensi(mata_pelajaran = MataPelajaran.objects.filter(kode=kodeMapel).get(), siswa = Siswa.objects.filter(nik=x.siswa.nik).get(), pertemuan_ke = bpForm.instance, presensi = int(request.POST.get('presensi_' + x.siswa.nik))).save()
                
                return redirect(f"/tugasKhusus/Presensi/{nikGuru} {kelasId} {namaKelas} {kodeMapel}")
            
        else:
        # Execute when open insert presensi page
        
            bpForm = BabPengajaranForm

        mapping = DaftarSiswaKelas.objects.filter(Kelas__id = kelasId).all()        # Get all siswa from that kelas
        
        context = {"userType": global_userType, "mapping":mapping, "id":kelasId, "namaKelas":namaKelas, "mapel":kodeMapel, 'bpForm':bpForm}

        template = loader.get_template('MasukkanPresensi_Page.html')
        return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User


# Function to update presensi   
def UpdatePresensi_Function(request, nikGuru, pertemuanId, idMapel):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct    

        savedPresensi = BabPengajaran.objects.filter(id = pertemuanId, mata_pelajaran_id = idMapel).get()   # Get data of presensi

        if request.method == "POST":
        # Execute when press submit
            
            bpForm = BabPengajaranForm(request.POST, request.FILES, instance=savedPresensi)     # Get value of form, and the FILE IS FOR PICTURE, and get previous data     
            
            DaftarSiswa = Presensi.objects.filter(mata_pelajaran = savedPresensi.mata_pelajaran, pertemuan_ke = savedPresensi.id).all()     # Get Presensi data of siswa

            if bpForm.is_valid():
                
                if not bpForm.cleaned_data['foto']:
                # i forget what is this for hehe
                    bpForm.instance.foto =  savedPresensi.foto
                    return HttpResponse(savedPresensi.foto)
                # ------------------------------------------------------

                bpForm.save(commit=True)    # Save data

                for x in DaftarSiswa:
                # Update presensi data of all siswa on that kelas
                    x.presensi = int(request.POST.get('presensi_' + x.siswa.nik))
                    x.save()    # Save presensi data of siswa
                
                return redirect(f"/tugasKhusus/Presensi/{nikGuru} {savedPresensi.kelas.id} {savedPresensi.kelas.nama} {savedPresensi.mata_pelajaran.kode}")

            else:
            # Execute if bpFom is not valid (i hope it's always valid)    
                return HttpResponse(str(bpForm))
            
        else:
        # Execute when open page to update presensi
        
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
            # Get saved data

        mapping = Presensi.objects.filter(mata_pelajaran = savedPresensi.mata_pelajaran, pertemuan_ke = savedPresensi.id).all() # Get presensi data of siswa on that kelas

        context = {"userType": global_userType, "mapping":mapping, "namaKelas":savedPresensi.kelas.nama, "mapel":savedPresensi.mata_pelajaran.kode, 'bpForm':bpForm, 'foto':savedPresensi.foto}

        template = loader.get_template('MasukkanPresensi_Page.html')
        return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User

    
# Function to delete presensi
def DeletePresensi_Function(request, nikGuru, pertemuanId, idMapel):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct

        savedPresensi = BabPengajaran.objects.filter(id = pertemuanId, mata_pelajaran_id = idMapel).get()   # Get data of presensi

        DaftarSiswa = Presensi.objects.filter(mata_pelajaran = savedPresensi.mata_pelajaran, pertemuan_ke = savedPresensi.id).all()     # Get presensi data of siswa

        for x in DaftarSiswa:
        # Delete presensi from siswa
            x.delete()

        savedPresensi.delete()

        return redirect(f"/tugasKhusus/Presensi/{nikGuru} {savedPresensi.kelas.id} {savedPresensi.kelas.nama} {savedPresensi.mata_pelajaran.kode}")    
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User
   

# Function to view Presensi Page
def Penilaian_Function(request):

    if global_userType == "Guru" and global_isLogin == True:
    # Execute if user is login and he/she is guru

        mapping = MappingGuru.objects.filter(guru__nik = global_loginUser.nik).distinct('mata_pelajaran')     # Get all kelas from mapping model when guru is teach on it
        
        context = {"userType": global_userType, "mapping":mapping, 'nikGuru':str(global_loginUser.nik)}

        template = loader.get_template('Penilaian_Page.html')
        return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User


# Function to view list of pertemuan on that kelas
def PenilaianDetail_Function(request, kodeMapel, nikGuru):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct

        try:
        # Try to find all data of Komponen Penilaian
            komponenPenilaian = KomponenPenilaian.objects.filter(guru__nik = nikGuru, mata_pelajaran__kode = kodeMapel).all()

        except:
            komponenPenilaian = None

        context = {"userType": global_userType, "nikGuru":nikGuru, "kodeMapel":kodeMapel, "komponenPenilaian":komponenPenilaian}

        template = loader.get_template('PenilaianDetail_Page.html')
        return HttpResponse(template.render(context, request))
        
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User


# Function to insert presensi
def InsertKomponenPenilaian_Function(request, kodeMapel, nikGuru):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct

        if request.method == "POST":
        # Execute when press submit button
         
            kpForm = KomponenPenilaianForm(request.POST)     # Get value of form

            if kpForm.is_valid():
                
                kpForm.instance.guru = Guru.objects.filter(nik = nikGuru).get()                    # Insert kelas to form value
                kpForm.instance.mata_pelajaran = MataPelajaran.objects.filter(kode = kodeMapel).get()   # Inser mapel to form value

            
                kpForm.save(commit=True)        # Save data

                return redirect(f"/tugasKhusus/Penilaian/{kodeMapel} {nikGuru}")
            
        else:
        # Execute when open insert presensi page
        
            kpForm = KomponenPenilaianForm
        
        context = {"userType": global_userType,"mapel":kodeMapel, 'kpForm':kpForm}

        template = loader.get_template('MasukkanKomponenPenilaian_Page.html')
        return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User


# Function to view list of pertemuan on that kelas
def KomPenilaian_Function(request, kodeMapel, nikGuru, namaKomPenilaian, idKomPenilaian):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct

        try:
        # Try to find all data of Kelas from Mapping Guru
            listMapping = MappingGuru.objects.filter(guru__nik = nikGuru, mata_pelajaran__kode = kodeMapel).all()

        except:
            listMapping = None

        context = {"userType": global_userType, "nikGuru":nikGuru, "kodeMapel":kodeMapel, "namaKomPenilaian":namaKomPenilaian, "idKomPenilaian":idKomPenilaian, "listMapping":listMapping}

        template = loader.get_template('KomPenilaian_Page.html')
        return HttpResponse(template.render(context, request))
        
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User


# Function to view list of pertemuan on that kelas
def KomPenilaianDetail_Function(request, kodeMapel, nikGuru, namaKomPenilaian, idKomPenilaian, namaKelas, idKelas):

    if global_userType == "Guru" and global_isLogin == True and global_loginUser.nik == nikGuru:
    # Execute if user is login, and he/she is guru, and the nik is correct

        if request.method == "POST":

            daftarSiswa = DaftarSiswaKelas.objects.filter(Kelas__id = idKelas).all()

            for x in daftarSiswa:
                
                try:
                    nilaiSiswa = NilaiSiswa.objects.filter(siswa = Siswa.objects.filter(nik = x.siswa.nik).get(), komponen_penilaian = KomponenPenilaian.objects.filter(id = idKomPenilaian).get()).get()
                    nilaiSiswa.nilai = int(request.POST.get('nilai_' + x.siswa.nik))
                    nilaiSiswa.save()
                except:
                    NilaiSiswa(siswa = Siswa.objects.filter(nik = x.siswa.nik).get(), komponen_penilaian = KomponenPenilaian.objects.filter(id = idKomPenilaian).get(), nilai = int(request.POST.get('nilai_' + x.siswa.nik))).save()

            return redirect(f"/tugasKhusus/Penilaian/{kodeMapel} {nikGuru}/{namaKomPenilaian} {idKomPenilaian}")

        else:

            try:
            # Try to find all data of Komponen Penilaian
                daftarSiswa = DaftarSiswaKelas.objects.filter(Kelas__id = idKelas).all()

            except:
                daftarSiswa = None
            
            try:
                nilaiSiswa = NilaiSiswa.objects.filter(komponen_penilaian__id = idKomPenilaian).all()
            except: 
                nilaiSiswa = None
            

            context = {"userType": global_userType, "nikGuru":nikGuru, "kodeMapel":kodeMapel, "namaKomPenilaian":namaKomPenilaian, "idKomPenilaian":idKomPenilaian, "daftarSiswa":daftarSiswa, "namaKelas":namaKelas, "idKelas":idKelas, "nilaiSiswa":nilaiSiswa}

            template = loader.get_template('KomPenilaianDetail_Page.html')
            return HttpResponse(template.render(context, request))
        
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')     # Back to Info User

    
# Function to insert Feedback
def InsertFeedback(request):
    
    if global_isLogin == True:
    # Execute if user is login

        if request.method == 'POST':
        # Execute if press submit button

            fbForm = FeedbackForm(request.POST)     # Get value of form

            if fbForm.is_valid():

                fbForm.instance.nik = global_loginUser

                fbForm.save()       # Save feedback data

                return redirect("/tugasKhusus/InfoUser")    # Back to Info User
        else:
            fbForm = FeedbackForm()

        context = {'fbForm':fbForm, 'loginUser':global_loginUser, 'userType':global_userType}

        template = loader.get_template('InsertFeedback.html')
        return HttpResponse(template.render(context, request))
    
    else:
        return HttpResponseRedirect('/tugasKhusus/InfoUser')        # Back to Info User


# Function when press log out
def LogOut(request):
    global global_isLogin, global_loginUser, global_userType
    global_isLogin = False
    global_loginUser = None
    global_userType = None

    return HttpResponseRedirect('login')       # Back to login page