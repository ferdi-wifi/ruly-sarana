from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login_page, name='login_page'),
    path('', views.beranda, name='beranda'),
    path('qrcode/<str:token_aktifasi>/', views.qrcode, name='qrcode'),
     path('logout', views.logoutPage, name='logout'),

    path('transaksi-peminjaman', views.transaksipeminjaman, name='transaksipeminjaman'),
   
    path('simpankeranjang', views.simpankeranjang, name='simpankeranjang'),
    path('hapuskeranjang', views.hapuskeranjang, name='hapuskeranjang'),
    path('simpantransaksi', views.simpantransaksi, name='simpantransaksi'),

    path('penyewa/', views.penyewa, name='penyewa'),
    path('form-penyewa/', views.formpenyewa, name='formpenyewa'),
    path('edit-penyewa/<str:pk>', views.editpenyewa, name='editpenyewa'),
    path('delete-penyewa/<str:pk>', views.deletepenyewa, name='deletepenyewa'),


    path('transaksi-pengembalian', views.transaksipengembalian, name='transaksipengembalian'),
    path('transaksi-kembali/<str:transaksi>', views.transaksikembali, name='transaksikembali'),
    path('transaksi-detail/<str:transaksi>', views.transaksidetail, name='transaksidetail'),

    

]
  
