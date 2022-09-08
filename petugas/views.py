
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import tolakhalaman_ini, ijinkan_pengguna
from django.contrib import messages
from administrator.models import TempPenyewa, DetailPenyewa,Jenis, Donatur, Petugas, Sarana, Penyewa, DetailPenyewa, Transaksi
from administrator.forms import TransaksiUbahForm, JenisForm, DonaturForm, PenyewaForm, SaranaForm, UserForm, PetugasForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import datetime


@tolakhalaman_ini
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cocokan = authenticate(request, username=username, password=password)
        if cocokan is None:
            messages.error(request, 'Usernama dan Password salah')
            return redirect('login_page')
        if cocokan is not None:
            login(request, cocokan)
            return redirect('beranda_admin')
    context = {
        'judul': 'Halaman Login',
        'menu': 'login',
    }
    return render(request, 'login.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def beranda(request):
    id_petugas = request.user.petugas.id
    petugas = Petugas.objects.get(id=id_petugas)
    user = User.objects.get(id=petugas.user.id)
    form = PetugasForm(instance=petugas)
    formuser = UserForm(instance=user)
    if request.method == 'POST':
        formsimpan = PetugasForm(request.POST,request.FILES, instance=petugas)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('beranda')
    context = {
       'judul': 'Halaman Beranda Petugas',
        'menu': 'beranda',
        'form':form,
        'formuser':formuser
    }
    return render(request, 'beranda.html', context)


@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def transaksipeminjaman(request):
    id_petugas = request.user.petugas.id
    petugas = Petugas.objects.get(id=id_petugas)
    sarana = Sarana.objects.all().order_by('id')
    penyewa = Penyewa.objects.all().order_by('id')
    temp = TempPenyewa.objects.filter(petugas__id=petugas.id).order_by('id')
    hitungtemp = TempPenyewa.objects.filter(petugas__id=petugas.id).count()
    context = {
       'judul': 'Halaman Beranda Peminjaman',
        'menu': 'peminjaman',
        'sarana':sarana,
        'temp':temp,
        'hitungtemp':hitungtemp,
        'penyewa':penyewa,
      
    }
    return render(request, 'peminjaman.html', context)
@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def transaksipengembalian(request):
    id_petugas = request.user.petugas.id
    petugas = Petugas.objects.get(id=id_petugas)
    transaksi = Transaksi.objects.filter(petugas__id=petugas.id).order_by('-id')
    context = {
       'judul': 'Halaman Beranda Pengembalian',
        'menu': 'pengembalian',
        'transaksi':transaksi,
    }
    return render(request, 'pengembalian.html', context)
@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def simpankeranjang(request):
    
    if request.method == "POST":
        id = request.POST.get('id')
        stok = request.POST['stok']
        jumlah = request.POST['jumlah']
        id_petugas = request.user.petugas.id
        petugas = Petugas.objects.get(id=id_petugas)
        sarana = Sarana.objects.get(pk=id)

        cek_temp = TempPenyewa.objects.filter(petugas=petugas, sarana=sarana).count()
        if cek_temp > 0:
            temp =TempPenyewa.objects.get(petugas=petugas, sarana=sarana)
            temp.jumlah+=int(jumlah)
            temp.save()

            sarana.stok_sarana-=int(jumlah)
            sarana.save()
            return JsonResponse({'status': 'Save' })
        else:
            sarana.stok_sarana-=int(jumlah)
            sarana.save()

            temp = TempPenyewa.objects.create(petugas=petugas, sarana=sarana, jumlah = jumlah )
            temp.save()
            return JsonResponse({'status': 'Save' })
    else:
        return JsonResponse({'status': 0 })
@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def hapuskeranjang(request):
    
    if request.method == "POST":
        id = request.POST.get('sid')
        pus = TempPenyewa.objects.get(pk=id)
        pus.delete()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})
def qrcode(request, token_aktifasi):
    data = get_object_or_404(Sarana, token_aktifasi_sarana=token_aktifasi)
    context = {
        'judul': 'Halaman Qcode',
        'data':data,
    }
    return render(request, 'qrcode.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login_page')

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def simpantransaksi(request):
    
    if request.method == "POST":
       
        tgl_pinjam = request.POST['tgl_pinjam']
        penyewa = request.POST['penyewa']
        id_petugas = request.user.petugas.id
       
        id_transaksi = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        petugas = Petugas.objects.get(id=id_petugas)

        idpenyewa = Penyewa.objects.get(id=penyewa)

        transaksi = Transaksi.objects.create(id_transaksi = id_transaksi ,penyewa = idpenyewa, petugas = petugas, tanggal_pinjam= tgl_pinjam, keterangan='Terpinjam')
        transaksi.save()

        temp = TempPenyewa.objects.order_by('-id').filter(petugas_id=petugas.id)
        for r in temp:
            instance_detail= DetailPenyewa(
                id_transaksi = id_transaksi,
                sarana = r.sarana,
                jumlah = r.jumlah,
            )
            instance_detail.save()
        temp.delete()
       
        return JsonResponse({'status': 'Save' })
    else:
        return JsonResponse({'status': 0 })

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def penyewa(request):
    penyewa = Penyewa.objects.all()
    context = {
        'judul': 'Halaman Penyewa',
        'menu': 'penyewa',
        'data':penyewa,
    }
    return render(request, 'penyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def formpenyewa(request):
    form = PenyewaForm()
    if request.method == 'POST':
        formsimpan = PenyewaForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('penyewa')
    context = {
        'judul': 'Form Penyewa',
        'menu': 'penyewa',
        'form':form
    }
    return render(request, 'formpenyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def editpenyewa(request, pk):
    penyewa = Penyewa.objects.get(pk=pk)
    form = PenyewaForm(instance=penyewa)
    if request.method == 'POST':
        formsimpan = PenyewaForm(request.POST, instance=penyewa)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('penyewa')
    context = {
        'judul': 'Form Edit Penyewa',
        'menu': 'penyewa',
        'form':form
    }
    return render(request, 'formpenyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def deletepenyewa(request, pk):

    
    hapus = Penyewa.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('penyewa')

    context = {
        'judul': 'Form Hapus Penyewa',
        'menu': 'penyewa',
        'hapus':hapus  
    }
    return render(request, 'hapuspenyewa.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def transaksikembali(request, transaksi):
    data = get_object_or_404(Transaksi, id_transaksi=transaksi)

    transaksi = Transaksi.objects.get(id_transaksi=data.id_transaksi)
    form =TransaksiUbahForm(instance=transaksi)
    if request.method == 'POST':
        detail = DetailPenyewa.objects.order_by('-id').filter(id_transaksi=data.id_transaksi)
        for row in detail:
            sarana = Sarana.objects.get(id=row.sarana.id)
            sarana.stok_sarana+=int(row.jumlah)
            sarana.save()
        formsimpan = TransaksiUbahForm(request.POST, instance=transaksi)
        if formsimpan.is_valid():
            simpan = formsimpan.save()
            simpan.keterangan= 'Kembali'
            simpan.save()
            return redirect('transaksipengembalian')
    context = {
        'judul': 'Form Ubah Keterangan Kembali',
        'menu': 'pengembalian',
        'data':data,
        'form':form,
        
    }
    return render(request, 'formpengembalian.html', context)

@login_required(login_url='login_page')
@ijinkan_pengguna(yang_diizinkan=['petugas']) 
def transaksidetail(request, transaksi):
    data = get_object_or_404(Transaksi, id_transaksi=transaksi)
    detail = DetailPenyewa.objects.filter(id_transaksi=data.id_transaksi)
    
    context = {
        'judul': 'Form Detail Keterangan Kembali',
        'menu': 'pengembalian',
        'data':data,
        'detail':detail,
       
        
    }
    return render(request, 'detailpeminjaman.html', context)