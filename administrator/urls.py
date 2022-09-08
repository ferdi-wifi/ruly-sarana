from django.urls import path
from . import views


urlpatterns = [
  path('', views.beranda_admin, name='beranda_admin'),

  path('jenis-admin/', views.jenis_admin, name='jenis_admin'),
  path('form-jenis/', views.formjenis_admin, name='formjenis_admin'),
  path('edit-jenis/<str:slug>', views.editjenis_admin, name='editjenis_admin'),
  path('delete-jenis/<str:pk>', views.deletejenis_admin, name='deletejenis_admin'),

  path('donatur-admin/', views.donatur_admin, name='donatur_admin'),
  path('form-donatur/', views.formdonatur_admin, name='formdonatur_admin'),
  path('edit-donatur/<str:pk>', views.editdonatur_admin, name='editdonatur_admin'),
  path('delete-donatur/<str:pk>', views.deletedonatur_admin, name='deletedonatur_admin'),


  path('penyewa-admin/', views.penyewa_admin, name='penyewa_admin'),
  path('form-penyewa/', views.formpenyewa_admin, name='formpenyewa_admin'),
  path('edit-penyewa/<str:pk>', views.editpenyewa_admin, name='editpenyewa_admin'),
  path('delete-penyewa/<str:pk>', views.deletepenyewa_admin, name='deletepenyewa_admin'),

  path('penyewa-admin/', views.penyewa_admin, name='penyewa_admin'),
  path('form-penyewa/', views.formpenyewa_admin, name='formpenyewa_admin'),
  path('edit-penyewa/<str:pk>', views.editpenyewa_admin, name='editpenyewa_admin'),
  path('delete-penyewa/<str:pk>', views.deletepenyewa_admin, name='deletepenyewa_admin'),

    path('sarana-admin/', views.sarana_admin, name='sarana_admin'),
  path('form-sarana/', views.formsarana_admin, name='formsarana_admin'),
  path('edit-sarana/<str:pk>', views.editsarana_admin, name='editsarana_admin'),
  path('delete-sarana/<str:pk>', views.deletesarana_admin, name='deletesarana_admin'),

  path('petugas-admin/', views.petugas_admin, name='petugas_admin'),
     path('form-petugas/', views.formpetugas_admin, name='formpetugas_admin'),
    path('edit-petugas/<str:pk>', views.editpetugas_admin, name='editpetugas_admin'),
    path('delete-petugas/<str:pk>', views.deletepetugas_admin, name='deletepetugas_admin'),

    path('transaksiadmin-pengembalian', views.transaksiadminpengembalian, name='transaksiadminpengembalian'),
    path('transaksiadmin-kembali/<str:transaksi>', views.transaksiadminkembali, name='transaksiadminkembali'),
    path('transaksiadmin-detail/<str:transaksi>', views.transaksiadmindetail, name='transaksiadmindetail'),


    path('transaksi-laporan', views.transaksilaporan, name='transaksilaporan'),
    path('export', views.export, name='export'),
  
  
  


    

]
  
