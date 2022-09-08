from django.shortcuts import render, redirect,get_object_or_404

from .models import Jenis, Donatur, Petugas, Sarana, Penyewa, DetailPenyewa, Transaksi
from .forms import JenisForm, DonaturForm, PenyewaForm, SaranaForm, UserForm, PetugasForm,TransaksiUbahForm

from django.db.models import Count, Q
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import uuid
from datetime import datetime, timedelta, time
today = datetime.now().date()
from django.contrib.auth.decorators import login_required
from petugas.decorators import ijinkan_pengguna,pilihan_login

from django.http import HttpResponse
from administrator.resources import SaranaResource
# Create your views here.

@login_required(login_url='login_page')
@pilihan_login
def beranda_admin (request):
    jmljenis = Jenis.objects.all().count()
    jmldoatur = Donatur.objects.all().count()
    jmlpetugas = Petugas.objects.all().count()
    jmlsarana = Sarana.objects.all().count()
    jmlpenyewa = Penyewa.objects.all().count()
   
    jmltransaksihariini = Transaksi.objects.filter(tanggal_pinjam=today).count()
    context = {
        'judul': 'Halaman Beranda',
        'menu': 'beranda',
        'jmljenis':jmljenis,
        'jmldoatur':jmldoatur,
        'jmlpetugas':jmlpetugas,
        'jmlsarana':jmlsarana,
        'jmlpenyewa':jmlpenyewa,
        'jmltransaksihariini':jmltransaksihariini,


    }
    return render(request, 'admin_beranda.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def jenis_admin(request):
    jenis = Jenis.objects.all()
    context = {
        'judul': 'Halaman Jenis',
        'menu': 'jenis',
        'data':jenis,
    }
    return render(request, 'admin_jenis.html', context)
@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def formjenis_admin(request):
    form = JenisForm()
    if request.method == 'POST':
        formsimpan = JenisForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('jenis_admin')
    context = {
        'judul': 'Form Jenis',
        'menu': 'jenis',
        'form':form
    }
    return render(request, 'admin_formjenis.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editjenis_admin(request, slug):
    jenis = Jenis.objects.get(slug=slug)
    form = JenisForm(instance=jenis)
    if request.method == 'POST':
        formsimpan = JenisForm(request.POST, instance=jenis)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('jenis_admin')
    context = {
        'judul': 'Form Edit Jenis',
        'menu': 'jenis',
        'form':form
    }
    return render(request, 'admin_formjenis.html', context)
@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deletejenis_admin(request, pk):
    hapus = Jenis.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('jenis_admin')

    context = {
        'judul': 'Form Hapus Jenis',
        'menu': 'jenis',
        'hapus':hapus  
    }
    return render(request, 'admin_hapusjenis.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def donatur_admin(request):
    donatur = Donatur.objects.all()
    context = {
        'judul': 'Halaman Donatur',
        'menu': 'donatur',
        'data':donatur,
    }
    return render(request, 'admin_donatur.html', context)
@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def formdonatur_admin(request):
    form = DonaturForm()
    if request.method == 'POST':
        formsimpan = DonaturForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('donatur_admin')
    context = {
        'judul': 'Form Donatur',
        'menu': 'donatur',
        'form':form
    }
    return render(request, 'admin_formdonatur.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editdonatur_admin(request, pk):
    donatur = Donatur.objects.get(pk=pk)
    form = DonaturForm(instance=donatur)
    if request.method == 'POST':
        formsimpan = DonaturForm(request.POST, instance=donatur)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('donatur_admin')
    context = {
        'judul': 'Form Edit Donatur',
        'menu': 'donatur',
        'form':form
    }
    return render(request, 'admin_formdonatur.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deletedonatur_admin(request, pk):

    
    hapus = Donatur.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('donatur_admin')

    context = {
        'judul': 'Form Hapus Donatur',
        'menu': 'donatur',
        'hapus':hapus  
    }
    return render(request, 'admin_hapusdonatur.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def penyewa_admin(request):
    penyewa = Penyewa.objects.all()
    context = {
        'judul': 'Halaman Penyewa',
        'menu': 'penyewa',
        'data':penyewa,
    }
    return render(request, 'admin_penyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def formpenyewa_admin(request):
    form = PenyewaForm()
    if request.method == 'POST':
        formsimpan = PenyewaForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('penyewa_admin')
    context = {
        'judul': 'Form Penyewa',
        'menu': 'penyewa',
        'form':form
    }
    return render(request, 'admin_formpenyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editpenyewa_admin(request, pk):
    penyewa = Penyewa.objects.get(pk=pk)
    form = PenyewaForm(instance=penyewa)
    if request.method == 'POST':
        formsimpan = PenyewaForm(request.POST, instance=penyewa)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('penyewa_admin')
    context = {
        'judul': 'Form Edit Penyewa',
        'menu': 'penyewa',
        'form':form
    }
    return render(request, 'admin_formpenyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deletepenyewa_admin(request, pk):

    
    hapus = Penyewa.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('penyewa_admin')

    context = {
        'judul': 'Form Hapus Penyewa',
        'menu': 'penyewa',
        'hapus':hapus  
    }
    return render(request, 'admin_hapuspenyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def sarana_admin(request):
    sarana = Sarana.objects.all()
    context = {
        'judul': 'Halaman Sarana',
        'menu': 'sarana',
        'data':sarana,
    }
    return render(request, 'admin_sarana.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def formsarana_admin(request):
    form = SaranaForm()
    auth_token = str(uuid.uuid4())
    if request.method == 'POST':
        formsimpan = SaranaForm(request.POST,request.FILES)
        if formsimpan.is_valid():
            simpan = formsimpan.save()
            simpan.token_aktifasi_sarana=auth_token
            simpan.save()
            return redirect('sarana_admin')
    context = {
        'judul': 'Form Sarana',
        'menu': 'sarana',
        'form':form
    }
    return render(request, 'admin_formsarana.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editsarana_admin(request, pk):
    sarana = Sarana.objects.get(pk=pk)
    form = SaranaForm(instance=sarana)
    if request.method == 'POST':
        formsimpan = SaranaForm(request.POST,request.FILES, instance=sarana)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('sarana_admin')
    context = {
        'judul': 'Form Edit Sarana',
        'menu': 'sarana',
        'form':form
    }
    return render(request, 'admin_formsarana.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deletesarana_admin(request, pk):

    
    hapus = Sarana.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('sarana_admin')

    context = {
        'judul': 'Form Hapus Sarana',
        'menu': 'sarana',
        'hapus':hapus  
    }
    return render(request, 'admin_hapussarana.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def petugas_admin(request):
    petugas = Petugas.objects.all()
    context = {
        'data': petugas,
        'judul': 'Halaman Petugas',
        'menu': 'petugas',
    }
    return render(request, 'admin_petugas.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def formpetugas_admin(request):
    form = PetugasForm()
    formuser = UserForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save()

        akses = Group.objects.get(name='petugas')
        user.groups.add(akses)

        formsimpan = PetugasForm(request.POST)
        if formsimpan.is_valid():
            data = formsimpan.save()
            data.user = user
            data.save()
            return redirect('petugas_admin')
    context = {
        'judul': 'Halaman Form Petugas',
        'menu': 'petugas',
        'form':form,
        'formuser':formuser
    }
    return render(request, 'admin_formpetugas.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editpetugas_admin(request, pk):
    petugas = Petugas.objects.get(id=pk)
    user = User.objects.get(id=petugas.user.id)
    form = PetugasForm(instance=petugas)
    formuser = UserForm(instance=user)
    if request.method == 'POST':
        formsimpan = PetugasForm(request.POST,request.FILES, instance=petugas)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('petugas_admin')
    context = {
       'judul': 'Halaman Form Edit Petugas',
        'menu': 'petugas',
        'form':form,
        'formuser':formuser
    }
    return render(request, 'admin_formpetugas.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deletepetugas_admin(request, pk):
    hapus = Petugas.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('petugas_admin')
    context = {
        'judul': 'Halaman Hapus Petugas',
        'menu': 'petugas',
        'hapus':hapus  
    }
    return render(request, 'admin_hapuspetugas.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def transaksiadminpengembalian(request):
    transaksiadmin = Transaksi.objects.order_by('-id')
    context = {
       'judul': 'Halaman Beranda Pengembalian',
        'menu': 'pengembalian',
        'transaksiadmin':transaksiadmin,
    }
    return render(request, 'admin_pengembalian.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def transaksiadminkembali(request, transaksi):
    data = get_object_or_404(Transaksi, id_transaksi=transaksi)

    transaksiadmin = Transaksi.objects.get(id_transaksi=data.id_transaksi)
    form =TransaksiUbahForm(instance=transaksiadmin)
    if request.method == 'POST':
        detail = DetailPenyewa.objects.order_by('-id').filter(id_transaksi=data.id_transaksi)
        for row in detail:
            sarana = Sarana.objects.get(id=row.sarana.id)
            sarana.stok_sarana+=int(row.jumlah)
            sarana.save()
        formsimpan = TransaksiUbahForm(request.POST, instance=transaksiadmin)
        if formsimpan.is_valid():
            simpan = formsimpan.save()
            simpan.keterangan= 'Kembali'
            simpan.save()
            return redirect('admin_transaksiadminpengembalian')
    context = {
        'judul': 'Form Ubah Keterangan Kembali',
        'menu': 'pengembalian',
        'data':data,
        'form':form,
        
    }
    return render(request, 'formpengembalian.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def transaksiadmindetail(request, transaksi):
    data = get_object_or_404(Transaksi, id_transaksi=transaksi)
    detail = DetailPenyewa.objects.filter(id_transaksi=data.id_transaksi)
    
    context = {
        'judul': 'Form Detail Keterangan Kembali',
        'menu': 'pengembalian',
        'data':data,
        'detail':detail,
       
        
    }
    return render(request, 'admin_detailpeminjaman.html', context)
@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def transaksilaporan(request):
   
    transaksi = Transaksi.objects.order_by('-id')
    context = {
        'judul': 'Data Laporan Transaksi',
        'menu': 'laporan',
        'data':transaksi,
     
       
        
    }
    return render(request, 'admin_laporantransaksi.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def export(request):
    sarana_resource = SaranaResource()
    dataset = sarana_resource.export()
    response = HttpResponse(dataset.xls, content_type = 'application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Data Transaksi Sarana.xls"'

    return response