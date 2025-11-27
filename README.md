# 📚 SimpleLMS - Simple Learning Management System

Sistem manajemen pembelajaran berbasis Django untuk mengelola mata kuliah, pengajar, siswa, konten pembelajaran, dan interaksi.

---

## 🚀 Quick Start

### Prasyarat
- Python 3.10+
- Virtual environment sudah disetup di `env_django/`
- PowerShell atau Command Prompt (Windows)

### Jalankan Server
```powershell
cd C:\laragon\www\Simplelms\code
C:\laragon\www\Simplelms\env_django\Scripts\python.exe manage.py runserver
```

Akses aplikasi di: **http://127.0.0.1:8000/**

### Login Admin Dashboard
- **URL:** http://127.0.0.1:8000/admin/
- **Username:** `admin`
- **Password:** `admin`

---

## 📦 Fitur Utama

### 1. **Manajemen Mata Kuliah**
- CRUD (Create, Read, Update, Delete) mata kuliah
- Setiap mata kuliah memiliki pengajar yang diacak secara otomatis
- Upload gambar untuk setiap mata kuliah
- Harga dan deskripsi mata kuliah

### 2. **Manajemen User**
- Role: Pengajar, Siswa, Asisten
- Authentication dan authorization
- User profile management

### 3. **Konten Pembelajaran**
- Upload video URL
- Upload file attachment
- Hierarchical content (parent-child relationship)
- Multiple content per course

### 4. **Interaksi**
- Sistem komentar pada konten
- Tracking completion untuk setiap siswa
- Course member management (enrollment)

---

## 🗂️ Struktur Project

```
Simplelms/
├── code/                          # Main application folder
│   ├── manage.py                  # Django management script
│   ├── db.sqlite3                 # Database SQLite
│   ├── importer.py                # Data import script (dengan random teacher)
│   ├── set_admin_password.py     # Reset admin password utility
│   │
│   ├── core/                      # Main app
│   │   ├── models.py              # Database models
│   │   ├── views.py               # Views/Controllers
│   │   ├── admin.py               # Admin configuration
│   │   ├── urls.py                # URL routing
│   │   └── migrations/            # Database migrations
│   │
│   ├── simplelms/                 # Project settings
│   │   ├── settings.py            # Django settings
│   │   ├── urls.py                # Main URL config
│   │   └── wsgi.py                # WSGI config
│   │
│   ├── csv_data/                  # Sample data untuk import
│   │   ├── user_data.csv
│   │   ├── course-data.csv
│   │   ├── member-data.csv
│   │   ├── content-data.csv
│   │   └── comment-data.csv
│   │
│   └── templates/                 # HTML templates
│       └── core/
│
├── env_django/                    # Virtual environment
│   └── Scripts/
│       └── python.exe
│
├── LAPORAN_PENGEMBANGAN.md       # Dokumentasi lengkap
├── LAPORAN_RINGKAS.md            # Laporan singkat
├── CHECKLIST_PENGEMBANGAN.md     # Checklist pengembangan
└── README.md                      # File ini
```

---

## 🛠️ Setup & Installation

### 1. Clone atau Download Project
```powershell
cd C:\laragon\www\
# Project sudah ada di Simplelms/
```

### 2. Aktivasi Virtual Environment (Opsional)
```powershell
cd C:\laragon\www\Simplelms
env_django\Scripts\activate
```

### 3. Install Dependencies (Jika Belum)
```powershell
pip install -r requirements.txt
```

### 4. Database Migration
```powershell
cd code
python manage.py migrate
```

### 5. Import Sample Data
```powershell
python importer.py
```

Output:
```
=== Mulai Import ===
Importing Users...
User admin created
User dosen_andi created
...
Importing Courses...
Course Pemograman Sisi Server created with teacher siti
...
=== Selesai ===
```

### 6. Set Password Admin
```powershell
python set_admin_password.py
```

### 7. Jalankan Server
```powershell
python manage.py runserver
```

---

## 📊 Data Models

### Course (Mata Kuliah)
- `teacher`: ForeignKey ke User (pengajar)
- `name`: Nama mata kuliah
- `description`: Deskripsi
- `price`: Harga
- `image`: Gambar/thumbnail
- `created_at`, `updated_at`: Timestamp

### CourseMember (Subscriber)
- `course_id`: Mata kuliah yang diikuti
- `user_id`: User yang mengikuti
- `role`: Peran (Siswa/Asisten)

### CourseContent (Konten)
- `course_id`: Mata kuliah terkait
- `name`: Judul konten
- `description`: Deskripsi
- `video_url`: URL video pembelajaran
- `file_attachment`: File attachment
- `parent_id`: Parent content (untuk hierarchical)

### Comment (Komentar)
- `content_id`: Konten yang dikomentari
- `user_id`: User yang berkomentar
- `comment`: Isi komentar

### Completion (Status Penyelesaian)
- `member_id`: Member yang menyelesaikan
- `content_id`: Konten yang diselesaikan
- `last_update`: Waktu penyelesaian

---

## 🎯 Fitur Khusus: Random Teacher

### Cara Kerja
Saat import data menggunakan `importer.py`, sistem akan:
1. Mengambil semua user yang tersedia
2. Memilih satu user secara random untuk setiap mata kuliah
3. Assign user tersebut sebagai pengajar

### Contoh Output
```
Course Pemograman Sisi Server created with teacher siti
Course Pemograman Sisi Klien created with teacher rudi
Course Penambangan Data created with teacher lina
```

### Kode
```python
import random
all_users = list(User.objects.all())
teacher_obj = random.choice(all_users) if all_users else User.objects.first()
```

---

## 🔧 Command Reference

### Development Commands

```powershell
# Jalankan server
python manage.py runserver

# Jalankan pada port tertentu
python manage.py runserver 8080

# Buat migration baru
python manage.py makemigrations

# Apply migration
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Django shell (untuk debugging)
python manage.py shell

# Collect static files
python manage.py collectstatic

# Import data dari CSV
python importer.py

# Reset password admin
python set_admin_password.py
```

### Database Commands

```powershell
# Reset database (hati-hati!)
Remove-Item db.sqlite3
python manage.py migrate
python importer.py

# Backup database
copy db.sqlite3 db.sqlite3.backup

# Restore database
copy db.sqlite3.backup db.sqlite3
```

---

## 🎨 Django Admin Features

### Course Admin
- **List View:** Nama, Pengajar, Harga, Tanggal Dibuat
- **Filters:** Filter by teacher, created date
- **Search:** Search by name, description
- **Fieldsets:** Grouped fields untuk kemudahan input

### CourseMember Admin
- **List View:** User, Course, Role, Date
- **Filters:** Role, course, date
- **Search:** Username, course name

### CourseContent Admin
- **List View:** Name, Course, Parent, Date
- **Filters:** Course, date
- **Search:** Name, description
- **Media Upload:** Video URL dan file attachment

### Comment Admin
- **List View:** User, Content, Preview, Date
- **Preview:** 50 karakter pertama dari komentar
- **Search:** Comment text, username

---

## 🔐 Security Notes

### Password Management
- Password di-hash menggunakan Django's authentication system
- Jangan hardcode password di production
- Gunakan environment variables untuk credentials

### Admin Access
- Default admin credentials untuk development:
  - Username: `admin`
  - Password: `admin`
- **⚠️ WAJIB GANTI DI PRODUCTION!**

### Database
- SQLite untuk development
- Untuk production, gunakan PostgreSQL atau MySQL
- Backup database secara berkala

---

## 🐛 Troubleshooting

### Server tidak bisa dijalankan
```powershell
# Pastikan di direktori yang benar
cd C:\laragon\www\Simplelms\code

# Cek apakah ada migration yang belum dijalankan
python manage.py migrate

# Cek error detail
python manage.py check
```

### Import data gagal
```powershell
# Pastikan CSV file ada
dir csv_data\

# Reset database dan coba lagi
Remove-Item db.sqlite3
python manage.py migrate
python importer.py
```

### Lupa password admin
```powershell
# Gunakan utility script
python set_admin_password.py

# Atau manual via shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> admin = User.objects.get(username='admin')
>>> admin.set_password('newpassword')
>>> admin.save()
>>> exit()
```

### Port sudah digunakan
```powershell
# Gunakan port lain
python manage.py runserver 8080

# Atau kill process yang menggunakan port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

## 📈 Performance Tips

1. **Database Optimization:**
   - Gunakan `select_related()` untuk ForeignKey
   - Gunakan `prefetch_related()` untuk ManyToMany
   - Add database indexes untuk field yang sering di-query

2. **Caching:**
   - Implementasi Redis untuk caching
   - Cache query results yang sering diakses
   - Use Django's cache framework

3. **Static Files:**
   - Collect static files: `python manage.py collectstatic`
   - Serve static files dengan web server (Nginx/Apache)
   - Use CDN untuk production

---

## 🚀 Deployment (Production Ready)

### Checklist Production:
- [ ] Set `DEBUG = False` di settings.py
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use production database (PostgreSQL/MySQL)
- [ ] Setup environment variables
- [ ] Collect static files
- [ ] Setup HTTPS/SSL
- [ ] Configure logging
- [ ] Setup backup strategy
- [ ] Use Gunicorn/uWSGI
- [ ] Setup Nginx/Apache reverse proxy
- [ ] Configure firewall
- [ ] Setup monitoring (Sentry, New Relic, etc)

---

## 📝 License

[Tentukan lisensi project Anda]

---

## 👥 Contributors

- **[Nama Anda]** - Initial work & Development

---

## 📞 Support

Jika ada pertanyaan atau masalah:
- Email: [email@example.com]
- GitHub Issues: [repository-url]
- Documentation: Lihat file LAPORAN_PENGEMBANGAN.md

---

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Admin Documentation](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/)
- [Python Official Documentation](https://docs.python.org/3/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)

---

**Last Updated:** 27 November 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready (Development)
