# QA Automation Project: Sauce Demo Testing

Proyek ini berisi rangkaian pengujian otomatis (*automated testing*) untuk aplikasi web e-commerce dummy, **Swag Labs (Sauce Demo)**, menggunakan Python, Pytest, dan Selenium WebDriver.

## Deskripsi Proyek
Tujuan utama proyek ini adalah melakukan *Regression Testing* untuk memastikan fungsionalitas aplikasi tetap stabil setelah adanya perubahan atau penambahan fitur. Fokus pengujian mencakup alur *login*, manajemen keranjang belanja, proses *checkout*, hingga validasi pesan kesalahan pada skenario negatif.

## Tech Stack
* **Language:** Python 3.11
* **Testing Framework:** Pytest
* **Automation Tool:** Selenium WebDriver
* **Browser:** Google Chrome

## Struktur Pengujian
Pengujian dibagi menjadi dua kategori utama dengan total 40 *test cases*:
1. **Positive Test Cases (20):** Memastikan fitur berjalan sesuai ekspektasi (misal: *login* berhasil, urutkan produk, proses *checkout* lancar).
2. **Negative Test Cases (20):** Memastikan sistem menangani input yang salah dengan benar (misal: *login* gagal, validasi form *checkout* yang kosong).

## Cara Menjalankan Pengujian
1. **Pastikan sudah menginstal *requirements*:**
   ```bash
   pip install pytest selenium

2. **Jalankan semua pengujian:**
   ```bash
   pytest -v test_saucedemo.py

3. **Jalankan pengujian tertentu (filter):**
   ```bash
   pytest -v test_saucedemo.py -k "test_pos_01"

✅ Hasil Pengujian
Seluruh 40 skenario pengujian telah berhasil dijalankan dengan hasil PASSED (100% Success Rate).