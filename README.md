# Django Product Management System

Aplikasi manajemen produk ini dibangun menggunakan **Django** sebagai backend (REST API) dan **PostgreSQL** sebagai database. Aplikasi ini memiliki fitur untuk **sinkronisasi otomatis** dari API eksternal dan tampilan antarmuka web yang bersih.

---

## 🛠️ Prasyarat (Prerequisites)

Sebelum memulai, pastikan komputer Anda sudah terinstal:
1.  **Python 3.10+**: [Download di sini](https://www.python.org/downloads/)
2.  **PostgreSQL**: [Download di sini](https://www.postgresql.org/download/)
3.  **Git**: (Opsional) Untuk clone repository.

---

## 🚀 Panduan Instalasi (Step-by-Step)

Ikuti langkah-langkah ini secara berurutan mulai dari nol.

### Langkah 1: Persiapkan Folder Project
Buka terminal (Command Prompt/PowerShell) dan arahkan ke folder di mana Anda ingin menyimpan project ini.
```bash
# Contoh jika file ada di d:\code_git\django
cd d:\code_git\django
```

### Langkah 2: Buat & Aktifkan Virtual Environment
Virtual environment berguna agar library project tidak tercampur dengan Python sistem.
```bash
# 1. Buat virtual environment bernama 'venv'
python -m venv venv

# 2. Aktifkan virtual environment
# Untuk Windows:
venv\Scripts\activate

# Untuk Mac/Linux:
# source venv/bin/activate
```
*(Tanda `(venv)` akan muncul di terminal Anda)*

### Langkah 3: Install Library
Install semua dependensi yang dibutuhkan (Django, DRF, Driver Postgres, dll).
```bash
pip install django djangorestframework psycopg2-binary requests
```

### Langkah 4: Konfigurasi Database PostgreSQL
1.  Buka **pgAdmin** atau terminal PostgreSQL.
2.  Buat database baru bernama `api_product_db`.
3.  Buka file project: `d:\code_git\django\api_product\settings.py`.
4.  Cari bagian `DATABASES` (sekitar baris 77) dan sesuaikan `USER` dan `PASSWORD` dengan milik Anda.

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'api_product_db',       # Nama database yang baru dibuat
           'USER': 'postgres',             # <-- GANTI DENGAN USERNAME ANDA
           'PASSWORD': 'password_anda',    # <-- GANTI DENGAN PASSWORD ANDA
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

### Langkah 5: Jalankan Migrasi
Langkah ini akan membuat tabel-tabel yang diperlukan di database PostgreSQL Anda.
```bash
# Membuat file migrasi
python manage.py makemigrations

# Menerapkan ke database
python manage.py migrate
```

### Langkah 6: Buat Akun Admin (Superuser)
Akun ini digunakan untuk login ke web dan admin panel.
```bash
python manage.py createsuperuser
```
*Username: `admin`*
*Email: (biarkan kosong)*
*Password: `admin123` (atau sesuai keinginan)*

### Langkah 7: Sinkronisasi Data (PENTING!)
Jalankan perintah ini untuk mengambil data produk dari API eksternal dan menyimpannya ke database lokal Anda.
```bash
python manage.py sync_products
```
*Script ini akan otomatis login ke API FastPrint menggunakan username/password dinamis dan menyimpan data Produk, Kategori, dan Status.*

### Langkah 8: Jalankan Aplikasi
Sekarang server siap dijalankan.
```bash
python manage.py runserver
```

### Langkah 9: Akses Aplikasi
Buka browser dan kunjungi:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

-   **Halaman Utama**: Daftar Produk (CRUD) dengan tampilan Admin.
-   **Login**: Klik tombol "Login to Admin" di pojok kanan atas.
    -   *User: `admin`*
    -   *Pass: `admin123`*

---

## ⚙️ Informasi Teknis

### Struktur API Endpoint
-   List Produk: `/api/produk/`
-   List Kategori: `/api/kategori/`
-   List Status: `/api/status/`

### Logika Sinkronisasi (`sync_products.py`)
File: `products/management/commands/sync_products.py`
Script ini menangani autentikasi dinamis (Username format `tesprogrammerDDMMYYC...`) dan pemetaan data JSON ke Model Django.

---

**Selamat Mencoba!**
Jika terjadi error "TemplateSyntaxError" atau masalah tampilan, pastikan Anda refresh halaman atau restart server.
