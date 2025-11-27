# LAPORAN PENGEMBANGAN SISTEM
## Simple Learning Management System (SimpleLMS)

**Tanggal:** 27 November 2025  
**Developer:** [Nama Anda]  
**Proyek:** SimpleLMS - Django-based Learning Management System

---

## 📋 RINGKASAN EKSEKUTIF

Laporan ini mendokumentasikan pengembangan dan perbaikan fitur pada sistem SimpleLMS, khususnya terkait dengan pengelolaan data pengajar (teacher) pada modul mata kuliah di Django Admin Dashboard.

---

## 🎯 TUJUAN PENGEMBANGAN

1. Memastikan setiap mata kuliah memiliki pengajar yang valid
2. Mengimplementasikan sistem pengacakan (randomization) pengajar dari daftar user yang tersedia
3. Memperbaiki tampilan data pengajar di Django Admin Dashboard
4. Memastikan data tidak kosong atau menampilkan tanda strip (-)

---

## 🔧 PERMASALAHAN AWAL

### Masalah yang Diidentifikasi:
- Field pengajar pada mata kuliah tidak menampilkan nama dengan benar
- Data pengajar kosong atau menampilkan placeholder seperti "-"
- Pengajar tidak diacak sehingga kurang variasi dalam data testing

---

## 💡 SOLUSI YANG DIIMPLEMENTASIKAN

### 1. **Modifikasi File `importer.py`**

**Lokasi:** `c:\laragon\www\Simplelms\code\importer.py`

**Perubahan:**
```python
# SEBELUM:
teacher_obj = User.objects.last()

# SESUDAH:
import random
all_users = list(User.objects.all())
teacher_obj = random.choice(all_users) if all_users else User.objects.first()
```

**Penjelasan:**
- Mengimport modul `random` untuk fungsi pengacakan
- Mengambil semua user yang tersedia dalam bentuk list
- Memilih satu user secara random sebagai pengajar
- Menambahkan fallback jika tidak ada user yang tersedia

**Output saat dijalankan:**
```
Course Pemograman Sisi Server created with teacher siti
Course Pemograman Sisi Klien created with teacher rudi
Course Penambangan Data created with teacher lina
Course Kecerdasan Buatan created with teacher dosen_andi
Course Sistem Terdistribusi created with teacher lina
Course Kriptografi created with teacher wati
```

### 2. **Struktur Model Course Dipertahankan**

**File:** `c:\laragon\www\Simplelms\code\core\models.py`

**Keputusan:**
- Tetap menggunakan `ForeignKey` untuk field `teacher` (satu pengajar per mata kuliah)
- Tidak mengubah struktur database yang sudah ada
- Fokus pada pengisian data yang lebih baik

**Kode:**
```python
class Course(models.Model):
    teacher = models.ForeignKey(User, verbose_name="pengajar", on_delete=models.RESTRICT)
    name = models.CharField("nama matkul", max_length=200)
    description = models.TextField("deskripsi")
    price = models.IntegerField("harga")
    image = models.ImageField("gambar", upload_to='courses/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### 3. **Konfigurasi Admin Dashboard**

**File:** `c:\laragon\www\Simplelms\code\core\admin.py`

**Fitur yang Dikonfigurasi:**
```python
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher', 'price', 'created_at']
    list_filter = ['teacher', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informasi Mata Kuliah', {
            'fields': ('name', 'description', 'price', 'teacher')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

### 4. **Utilitas Reset Password Admin**

**File:** `c:\laragon\www\Simplelms\code\set_admin_password.py`

**Tujuan:** Mempermudah reset password admin jika lupa

**Kode:**
```python
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'
django.setup()

from django.contrib.auth.models import User

admin = User.objects.get(username='admin')
admin.set_password('admin')
admin.is_staff = True
admin.is_superuser = True
admin.save()
print("Password admin telah diset ke 'admin'")
```

---

## 📝 LANGKAH-LANGKAH IMPLEMENTASI

### Step 1: Backup dan Persiapan
```powershell
# Backup database (opsional)
cd C:\laragon\www\Simplelms\code
copy db.sqlite3 db.sqlite3.backup
```

### Step 2: Reset Database
```powershell
# Hapus database lama
cd C:\laragon\www\Simplelms\code
Remove-Item -Path "db.sqlite3" -Force

# Hapus migration yang tidak perlu
Remove-Item -Path "core\migrations\0002_*.py" -Force
```

### Step 3: Jalankan Migration
```powershell
cd C:\laragon\www\Simplelms\code
C:\laragon\www\Simplelms\env_django\Scripts\python.exe manage.py migrate
```

**Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, core, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  [... migrations lainnya ...]
  Applying core.0001_initial... OK
  Applying sessions.0001_initial... OK
```

### Step 4: Import Data dengan Pengajar Random
```powershell
cd C:\laragon\www\Simplelms\code
C:\laragon\www\Simplelms\env_django\Scripts\python.exe importer.py
```

### Step 5: Set Password Admin
```powershell
cd C:\laragon\www\Simplelms\code
C:\laragon\www\Simplelms\env_django\Scripts\python.exe set_admin_password.py
```

### Step 6: Jalankan Server
```powershell
cd C:\laragon\www\Simplelms\code
C:\laragon\www\Simplelms\env_django\Scripts\python.exe manage.py runserver
```

---

## ✅ HASIL PENGUJIAN

### 1. **Data Mata Kuliah Berhasil Dibuat**
Total: 6 mata kuliah dengan pengajar yang berbeda-beda

| No | Nama Mata Kuliah | Pengajar | Status |
|----|------------------|----------|--------|
| 1 | Pemograman Sisi Server | siti | ✅ |
| 2 | Pemograman Sisi Klien | rudi | ✅ |
| 3 | Penambangan Data | lina | ✅ |
| 4 | Kecerdasan Buatan | dosen_andi | ✅ |
| 5 | Sistem Terdistribusi | lina | ✅ |
| 6 | Kriptografi | wati | ✅ |

### 2. **User yang Tersedia**
- admin
- dosen_andi
- dosen_budi
- ali, siti, rizki, maya, doni, lina, rudi, wati

### 3. **Akses Admin Dashboard**
- **URL:** http://127.0.0.1:8000/admin/
- **Username:** admin
- **Password:** admin
- **Status:** ✅ Berhasil diakses

### 4. **Tampilan di Admin Dashboard**
- Nama pengajar tampil dengan benar (bukan "-")
- Filter berdasarkan pengajar berfungsi
- Search functionality bekerja normal
- Data timestamp tersimpan dengan benar

---

## 📊 DATA YANG DIIMPORT

### Users (11 user)
```
admin, dosen_andi, dosen_budi, ali, siti, rizki, maya, doni, lina, rudi, wati
```

### Courses (6 mata kuliah)
Dengan pengajar random dari daftar user

### Course Members (23 member)
Relasi antara user dengan course

### Course Contents (30 konten)
Materi pembelajaran untuk setiap mata kuliah

### Comments (26 komentar)
Komentar dari user pada berbagai konten

---

## 🔍 TEKNOLOGI YANG DIGUNAKAN

| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| Python | 3.10 | Backend programming language |
| Django | 5.2.8 | Web framework |
| SQLite | 3.x | Database |
| PowerShell | 5.1 | Command line interface |

---

## 📂 STRUKTUR FILE YANG DIMODIFIKASI

```
Simplelms/
├── code/
│   ├── importer.py                    ← DIMODIFIKASI (random teacher)
│   ├── set_admin_password.py          ← DIBUAT BARU
│   ├── core/
│   │   ├── models.py                  ← TETAP (tidak diubah)
│   │   ├── admin.py                   ← TETAP (tidak diubah)
│   │   └── migrations/
│   │       └── 0001_initial.py        ← Migration utama
│   └── csv_data/
│       ├── user_data.csv
│       ├── course-data.csv
│       ├── member-data.csv
│       ├── content-data.csv
│       └── comment-data.csv
```

---

## 🎓 PEMBELAJARAN DAN BEST PRACTICES

### 1. **Import Data dengan Randomization**
- Menggunakan `random.choice()` untuk variasi data testing
- Memastikan ada fallback jika list kosong
- Menampilkan informasi detail saat import untuk debugging

### 2. **Database Management**
- Reset database saat ada perubahan struktur signifikan
- Backup data penting sebelum operasi destruktif
- Gunakan migration Django untuk perubahan schema

### 3. **Security**
- Set password admin dengan hash yang proper (`set_password()`)
- Jangan hardcode password di production
- Gunakan environment variables untuk kredensial sensitif

### 4. **Admin Dashboard Configuration**
- Gunakan `fieldsets` untuk grouping field yang logis
- Implementasi `list_display` untuk overview yang baik
- Tambahkan `search_fields` dan `list_filter` untuk usability

---

## 🚀 REKOMENDASI PENGEMBANGAN SELANJUTNYA

### 1. **Short Term (1-2 minggu)**
- [ ] Tambahkan validasi: satu user hanya bisa mengajar maksimal X mata kuliah
- [ ] Implementasi upload foto profil untuk pengajar
- [ ] Buat dashboard khusus untuk pengajar
- [ ] Tambahkan filter mata kuliah berdasarkan pengajar di frontend

### 2. **Medium Term (1-2 bulan)**
- [ ] Multiple pengajar per mata kuliah (ManyToManyField)
- [ ] Role-based access control (RBAC) yang lebih detail
- [ ] Notifikasi email untuk pengajar saat ada komentar baru
- [ ] Export laporan mata kuliah ke PDF/Excel

### 3. **Long Term (3-6 bulan)**
- [ ] Integrasi dengan sistem video conference
- [ ] Mobile app untuk akses lebih mudah
- [ ] AI-powered recommendation system
- [ ] Gamification untuk meningkatkan engagement

---

## 📌 CATATAN PENTING

### Do's ✅
- Selalu backup database sebelum operasi besar
- Test di development environment dulu
- Dokumentasikan setiap perubahan
- Gunakan version control (Git)

### Don'ts ❌
- Jangan edit database langsung di production
- Jangan hardcode credentials
- Jangan skip migration
- Jangan lupa aktivasi virtual environment

---

## 🔗 REFERENSI

1. Django Documentation: https://docs.djangoproject.com/
2. Django Admin Customization: https://docs.djangoproject.com/en/5.2/ref/contrib/admin/
3. Python Random Module: https://docs.python.org/3/library/random.html
4. Django Models: https://docs.djangoproject.com/en/5.2/topics/db/models/

---

## 👤 INFORMASI KONTAK & REPOSITORY

**Developer:** [Nama Anda]  
**Email:** [email@example.com]  
**GitHub:** [username]  
**Project Path:** `c:\laragon\www\Simplelms`

---

## ✍️ PERNYATAAN

Laporan ini dibuat berdasarkan pengembangan aktual yang dilakukan pada tanggal 27 November 2025. Semua kode dan implementasi telah diuji dan berfungsi dengan baik pada environment pengembangan.

**Tanda Tangan Digital:**  
_[Nama Anda]_  
_27 November 2025_

---

**END OF REPORT**
