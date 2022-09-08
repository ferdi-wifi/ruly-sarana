from django.db import models

from ckeditor.fields import RichTextField
import qrcode 
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from django_resized import ResizedImageField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Jenis(models.Model):
    nama = models.CharField(max_length=200, blank=False, null=True)
    aktif = models.BooleanField(default=True)
    slug = models.SlugField(max_length=200, null=True, unique=True)
    
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.nama)
        return super().save(*args, **kwargs)
    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural ="Jenis Sarana"

class Donatur(models.Model):
    nama_donatur = models.CharField(max_length=200, blank=False, null=True)
    alamat_donatur = RichTextField(blank=True, null=True)
    no_telp = models.CharField(max_length=100, blank=False, null=True)
    def __str__(self):
        return self.nama_donatur
    class Meta:
        verbose_name_plural ="Data Donatur"

class Petugas(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    nama = models.CharField(max_length=200, blank=False, null=True)
    wa = models.CharField(max_length=200, blank=False, null=True,verbose_name="No Whatsapp")
    alamat = RichTextField(blank=True, null=True)
    email = models.EmailField(max_length=200, blank=False, null=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nama
    class Meta:
        verbose_name_plural ="Data Petugas"



class Sarana(models.Model):
    STATUS=(
        ('BAIK' , 'BAIK'),
        ('KURANG BAIK' , 'KURANG BANK'),
        ('RUSAK' , 'RUSAK'),
    )
    jenis = models.ForeignKey(Jenis, null=True, blank=False, on_delete=models.SET_NULL)
    donatur = models.ForeignKey(Donatur,  null=True, blank=False, on_delete=models.SET_NULL)
    lokasi_sarana =  models.CharField(max_length=200, blank=False, null=True)
    stok_sarana = models.PositiveBigIntegerField(blank=True, null=True)
    nama_sarana = models.CharField(max_length=200, blank=False, null=True)
    token_aktifasi_sarana = models.CharField(max_length=300, blank=True, null=True)
    gambar_sarana = ResizedImageField(size=[400, 500], quality=80, crop=['middle', 'center'] , upload_to='gambar/foto_petani', blank=True, null=True, verbose_name="Foto Sarana (400 x 500 pixel)*)")
    keterangan = RichTextField(blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True, choices=STATUS)
    qr_code = models.ImageField(upload_to='arsip/data_qrcode',null=True, blank=True)
    date_created= models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.nama_sarana
    class Meta:
        verbose_name_plural ="Data Sarana"
    def save(self,*args, **kwargs):
        # current_site = get_current_site()
        domain = 'localhost:8000'
        qrcode_img = qrcode.make(f'http://{domain}/qrcode/{self.token_aktifasi_sarana}/')
        canvas = Image.new('RGB', (450,440), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'{self.nama_sarana}-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

class Penyewa(models.Model):
    nama_penyewa = models.CharField(max_length=200, blank=False, null=True)
    alamat_penyewa = RichTextField(blank=True, null=True)
    no_telp = models.CharField(max_length=100, blank=False, null=True)
    def __str__(self):
        return self.nama_penyewa
    class Meta:
        verbose_name_plural ="Data Penyewa"

class DetailPenyewa(models.Model):
    id_transaksi = models.CharField(max_length=200, blank=True, null=True)
    sarana = models.ForeignKey(Sarana,  null=True, blank=False, on_delete=models.SET_NULL)
    jumlah = models.PositiveBigIntegerField(blank=True, null=True)

    def __str__(self):
        if not self.id_transaksi:
           return ""
        return str(f"{self.id_transaksi} ({self.sarana.nama_sarana}) ({self.jumlah})")
    class Meta:
        verbose_name_plural ="Data Detail Penyewa"
class TempPenyewa(models.Model):
    petugas = models.ForeignKey(Petugas,  null=True, blank=False, on_delete=models.SET_NULL)
    sarana = models.ForeignKey(Sarana,  null=True, blank=False, on_delete=models.SET_NULL)
    jumlah = models.PositiveBigIntegerField(blank=True, null=True)
    
    def __str__(self):
        if not self.petugas:
           return ""
        return str(f"{self.petugas.nama} ({self.sarana.nama_sarana}) ({self.jumlah})")
  
    class Meta:
        verbose_name_plural ="Temp Detail Penyewa"

class Transaksi(models.Model):
    KETERANGAN=(
        ('Terpinjam' , 'Terpinjam'),
        ('Kembali' , 'Kembali'),
    )
    penyewa = models.ForeignKey(Penyewa,  null=True, blank=False, on_delete=models.SET_NULL)
    petugas = models.ForeignKey(Petugas,  null=True, blank=False, on_delete=models.SET_NULL)
    id_transaksi = models.CharField(max_length=200, blank=True, null=True)
    tanggal_pinjam = models.DateField(null=True, blank=False)
    tanggal_kembali = models.DateField(null=True, blank=True)
    keterangan = models.CharField(max_length=200, blank=True, null=True, choices=KETERANGAN)
    date_created= models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        if not self.id_transaksi:
           return ""
        return str(f"{self.keterangan} ({self.penyewa.nama_penyewa})")
    class Meta:
        verbose_name_plural ="Transaksi"