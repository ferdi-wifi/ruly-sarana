from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Jenis, Donatur, Petugas, Sarana, Penyewa, DetailPenyewa, Transaksi

class JenisForm(ModelForm):
    class Meta:
        model = Jenis
        fields=['nama','aktif']
    labels = {
            'nama': 'Nama Jenis:',
        } 

class DonaturForm(ModelForm):
    class Meta:
        model = Donatur
        fields=['nama_donatur','alamat_donatur','no_telp']
        widgets = {

            
            'no_telp': forms.TextInput(attrs={'class': 'form-control','placeholder':'628xxxxxxxxxx'}),

        }
    # labels = {
    #         'nama_donatur': 'Nama Jenis:',
    #     } 
class PenyewaForm(ModelForm):
    class Meta:
        model = Penyewa
        fields=['nama_penyewa','alamat_penyewa','no_telp']
        widgets = {

            
            'no_telp': forms.TextInput(attrs={'class': 'form-control','placeholder':'628xxxxxxxxxx'}),

        }
   
class TransaksiUbahForm(ModelForm):
    class Meta:
        model = Transaksi
        fields=['tanggal_kembali']
        widgets = {

            
            'tanggal_kembali': forms.TextInput(attrs={'class': 'form-control','type':'date'}),

        }
   

class SaranaForm(ModelForm):
    class Meta:
        model = Sarana
        fields=['jenis','donatur','status','lokasi_sarana','stok_sarana','nama_sarana','keterangan','gambar_sarana']
        widgets = {

            
            'no_telp': forms.TextInput(attrs={'class': 'form-control','placeholder':'628xxxxxxxxxx'}),

        }
    # labels = {
    #         'nama_donatur': 'Nama Jenis:',
    #     } 

class PetugasForm(ModelForm):
    class Meta:
        model = Petugas
        fields=['nama','wa','alamat','email']
        widgets = {
            'wa': forms.TextInput(attrs={'class': 'form-control','placeholder':'628xxxxxxxxxx'}),

        }
class UserForm(ModelForm):
    class Meta:
        model= User
        fields =['username']
        help_texts ={
            'username':''
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
        }
        labels = {
            'username': 'Username*',
        }


