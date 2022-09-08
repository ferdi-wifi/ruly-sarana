from django.contrib import admin
from .models import Transaksi,TempPenyewa, Jenis, Donatur, Petugas, Sarana,Penyewa,DetailPenyewa

admin.site.register(Jenis)
admin.site.register(Donatur)
admin.site.register(Petugas)
admin.site.register(Sarana)
admin.site.register(Penyewa)
admin.site.register(DetailPenyewa)
admin.site.register(TempPenyewa)
admin.site.register(Transaksi)
