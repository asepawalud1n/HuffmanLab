# 🗜️ Huffman Image Compression System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplikasi web untuk kompresi citra menggunakan algoritma **Huffman Coding** (lossless compression). Sistem ini dibuat sebagai proyek praktikum **Pengolahan Citra Digital**.

## 📋 Daftar Isi

- [Fitur Utama](#fitur-utama)
- [Teknologi](#teknologi)
- [Struktur Proyek](#struktur-proyek)
- [Instalasi](#instalasi)
- [Cara Menjalankan](#cara-menjalankan)
- [Panduan Penggunaan](#panduan-penggunaan)
- [Dokumentasi](#dokumentasi)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Kontributor](#kontributor)

---

## ✨ Fitur Utama

### 1. Kompresi Single Image
- Upload satu gambar (JPG/PNG/BMP)
- Konversi ke grayscale otomatis
- Kompresi menggunakan Huffman Coding
- Download hasil: `compressed.bin`, `codes.json`, `size.txt`
- Statistik lengkap: ukuran, rasio, penghematan

### 2. Dekompresi
- Upload file hasil kompresi (3 files)
- Dekode bitstream ke pixel array
- Rekonstruksi gambar lossless
- Download gambar hasil decode

### 3. Batch Dataset Processing
- Upload multiple images sekaligus
- Proses otomatis semua gambar
- Tabel hasil kompresi
- Statistik dataset: mean, median, max, min ratio
- Download CSV hasil

### 4. Visualisasi & Analisis
- Grafik interaktif dengan Chart.js:
  - Bar chart: Original vs Compressed size
  - Line chart: Compression ratios
  - Pie chart: Total comparison
- Fullscreen mode untuk charts
- Animasi smooth pada grafik

### 5. UI Premium
- Dark mode modern dan elegan
- Drag & drop file upload
- Responsive design
- Typography: Inter font
- Smooth animations

---

## 🛠️ Teknologi

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Web framework
- **OpenCV 4.8** - Image processing
- **NumPy 1.24** - Array operations
- **Werkzeug 3.0** - WSGI utilities

### Frontend
- **HTML5**
- **CSS3** (Custom dark theme)
- **JavaScript (ES6+)**
- **Chart.js 4.4** - Data visualization
- **Google Fonts (Inter)**

### Algoritma
- **Huffman Coding** - Lossless compression
- **Min-Heap** - Priority queue untuk tree building
- **DFS** - Traversal untuk code generation

---

## 📁 Struktur Proyek

```
HuffmanLab/
├── app.py                      # Flask application (main entry point)
├── huffman.py                  # Huffman Coding implementation
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation (this file)
│
├── templates/                  # HTML templates (Jinja2)
│   ├── index.html             # Home page
│   ├── result.html            # Single compression result
│   └── dataset_result.html    # Dataset results with charts
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Premium dark mode stylesheet
│   ├── js/
│   │   └── main.js            # JavaScript (drag-drop, interactions)
│   ├── uploads/               # Uploaded images (temporary)
│   ├── compressed/            # Compressed files output
│   └── decompressed/          # Decompressed images output
│
└── docs/                       # Documentation
    ├── TEORI_HUFFMAN_CODING.md   # Complete theory & explanation
    ├── DIAGRAM_SISTEM.md         # Flowchart, DFD, ERD
    ├── LAPORAN_ANALISIS.md       # Analysis report
    └── KESIMPULAN.md             # Conclusions & recommendations
```

---

## 🚀 Instalasi

### Prerequisites

Pastikan Anda sudah menginstall:
- **Python 3.8 atau lebih baru**
- **pip** (Python package manager)
- **Git** (optional, untuk clone repository)

### Langkah Instalasi

#### 1. Clone atau Download Repository

**Menggunakan Git:**
```bash
git clone https://github.com/yourusername/HuffmanLab.git
cd HuffmanLab
```

**Atau download ZIP:**
- Download ZIP dari repository
- Extract ke folder `HuffmanLab`
- Buka terminal di folder tersebut

#### 2. Buat Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Anda akan melihat `(venv)` di terminal, artinya virtual environment aktif.

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Dependencies yang akan diinstall:
- Flask==3.0.0
- opencv-python==4.8.1.78
- numpy==1.24.3
- Pillow==10.1.0
- Werkzeug==3.0.1

**Waktu instalasi:** ~2-5 menit (tergantung koneksi internet)

#### 4. Verifikasi Instalasi

```bash
python -c "import flask, cv2, numpy; print('All dependencies installed successfully!')"
```

Jika tidak ada error, instalasi berhasil! ✅

---

## ▶️ Cara Menjalankan

### 1. Start Flask Server

Pastikan Anda berada di folder `HuffmanLab` dan virtual environment aktif.

```bash
python app.py
```

Output yang akan muncul:
```
============================================================
🚀 Huffman Image Compression Web App
============================================================
📌 Server: http://localhost:5000
📌 Tekan CTRL+C untuk stop server
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 2. Akses di Browser

Buka browser dan kunjungi:
```
http://localhost:5000
```

atau

```
http://127.0.0.1:5000
```

### 3. Stop Server

Tekan `CTRL + C` di terminal untuk menghentikan server.

---

## 📖 Panduan Penggunaan

### A. Kompresi Satu Gambar

#### Langkah-langkah:

1. **Buka halaman utama** (`http://localhost:5000`)
2. **Pilih gambar:**
   - Klik area "Upload Satu Gambar", atau
   - Drag & drop gambar ke area upload
3. **Klik "Kompresi Gambar"**
4. **Tunggu proses** (beberapa detik)
5. **Lihat hasil:**
   - Statistik kompresi (ukuran, rasio, penghematan)
   - Perbandingan gambar asli vs grayscale
   - Download button untuk:
     - `compressed.bin` (file terkompresi)
     - `codes.json` (kode Huffman)
     - `size.txt` (dimensi gambar)

#### Contoh Output:

```
Ukuran Asli: 125.5 KB (1,024,000 bits)
Ukuran Kompresi: 82.3 KB (671,232 bits)
Rasio Kompresi: 1.53:1
Penghematan: 34.5%
```

### B. Dekompresi Gambar

#### Langkah-langkah:

1. **Scroll ke section "Dekompresi Gambar"**
2. **Upload 3 file** hasil kompresi:
   - `compressed.bin`
   - `codes.json`
   - `size.txt`
3. **Klik "Dekompresi"**
4. **Gambar akan otomatis terdownload**

#### Verifikasi Lossless:
- Bandingkan gambar hasil decode dengan grayscale asli
- Harus **identik pixel-by-pixel**

### C. Kompresi Dataset (Multiple Images)

#### Langkah-langkah:

1. **Scroll ke section "Kompresi Dataset"**
2. **Pilih multiple images:**
   - Klik dan pilih beberapa gambar sekaligus, atau
   - Drag & drop multiple files
3. **Klik "Kompresi Dataset"**
4. **Tunggu proses** (waktu ∝ jumlah gambar)
5. **Lihat hasil:**
   - **Dashboard Statistik:**
     - Mean ratio
     - Median ratio
     - Max/Min ratio
     - Total penghematan
   - **Grafik Interaktif:**
     - Bar chart (size comparison)
     - Line chart (ratios)
     - Pie chart (total)
   - **Tabel Detail** semua file
6. **Download CSV** untuk analisis lanjutan

#### Tips Dataset:
- Gunakan 5-20 gambar untuk hasil optimal
- Variasi jenis gambar (logo, foto, diagram) untuk analisis menarik
- File size per gambar: 100 KB - 5 MB

---

## 📚 Dokumentasi

### Dokumentasi Lengkap Tersedia di Folder `docs/`:

1. **TEORI_HUFFMAN_CODING.md**
   - Pengertian Huffman Coding
   - Sejarah dan latar belakang
   - Cara kerja algoritma
   - Huffman pada citra digital
   - Tahapan encoding & decoding
   - Kelebihan dan kekurangan
   - Perbandingan dengan metode lain
   - Aplikasi dunia nyata

2. **DIAGRAM_SISTEM.md**
   - Flowchart sistem
   - Data Flow Diagram (DFD Level 0, 1, 2)
   - Entity Relationship Diagram (ERD)
   - Arsitektur sistem (3-Tier, MVC)
   - Component & Deployment diagram

3. **LAPORAN_ANALISIS.md**
   - Analisis hasil kompresi dataset
   - Interpretasi grafik
   - Pembahasan rasio kompresi
   - Kapan Huffman optimal/tidak optimal
   - Studi kasus

4. **KESIMPULAN.md**
   - Kesimpulan proyek
   - Saran pengembangan
   - Alternative algorithms
   - Future improvements

---

## 🧪 Testing

### Manual Testing

#### Test Case 1: Single Image Compression

**Input:**
- Gambar: `test_logo.png` (100×100, hitam-putih)
- Format: PNG

**Expected Output:**
- Rasio: ~7-8:1 (karena hanya 2 unique pixels)
- File `.bin`, `.json`, `.txt` ter-generate
- Gambar decode identik dengan grayscale

**Cara Test:**
```bash
# 1. Upload test_logo.png
# 2. Klik "Kompresi Gambar"
# 3. Verifikasi output files exist
# 4. Download 3 files
# 5. Upload untuk dekompresi
# 6. Compare hasil decode dengan grayscale asli
```

#### Test Case 2: Dataset Compression

**Input:**
- 10 gambar berbeda (logo, foto, diagram)

**Expected Output:**
- Tabel dengan 10 rows
- Statistik: mean, median, max, min
- 3 charts ter-render
- CSV downloadable

**Cara Test:**
```bash
# 1. Pilih 10 gambar
# 2. Klik "Kompresi Dataset"
# 3. Verifikasi semua gambar terproses
# 4. Check charts loaded
# 5. Download CSV dan buka di Excel
```

### Unit Testing (Optional)

Buat file `test_huffman.py`:

```python
import unittest
from huffman import HuffmanCoding
import numpy as np

class TestHuffmanCoding(unittest.TestCase):
    def test_compression_lossless(self):
        # Create test data
        data = np.array([1, 2, 3, 1, 2, 1], dtype=np.uint8)

        # Compress
        huffman = HuffmanCoding()
        # ... (implement test)

        # Decompress
        # ... (implement test)

        # Assert lossless
        # self.assertTrue(np.array_equal(original, decoded))

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python -m unittest test_huffman.py
```

---

## 🔧 Troubleshooting

### Problem 1: Module not found

**Error:**
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
# Pastikan virtual environment aktif
# Re-install dependencies
pip install -r requirements.txt
```

### Problem 2: Port already in use

**Error:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Ganti port di app.py (line terakhir):
app.run(debug=True, host='0.0.0.0', port=5001)  # Ganti 5000 → 5001
```

### Problem 3: OpenCV error

**Error:**
```
cv2.error: OpenCV(4.x) ... error
```

**Solution:**
```bash
# Reinstall OpenCV
pip uninstall opencv-python
pip install opencv-python==4.8.1.78
```

### Problem 4: Upload file too large

**Error:**
```
413 Request Entity Too Large
```

**Solution:**
- Edit `app.py`, line 31:
```python
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
```

### Problem 5: Chart not showing

**Issue:** Grafik tidak muncul di dataset result page

**Solution:**
1. Check browser console (F12) untuk JavaScript errors
2. Pastikan koneksi internet (Chart.js dari CDN)
3. Refresh page (Ctrl+R)

---

## 🎯 Fitur Lanjutan (Optional)

### 1. Deployment ke Production

**Menggunakan Gunicorn:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Menggunakan Docker:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 2. Database Integration

Jika ingin menyimpan history kompresi:
- Gunakan SQLite atau PostgreSQL
- Buat model untuk `Image`, `Compression`, `HuffmanCode`
- Implementasikan CRUD operations

### 3. Async Processing

Untuk dataset besar, gunakan Celery:
```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379')

@celery.task
def compress_image_async(filepath):
    # Kompresi di background
    pass
```

---

## 👥 Kontributor

- **Nama:** [Nama Anda]
- **NIM:** [NIM Anda]
- **Mata Kuliah:** Pengolahan Citra Digital
- **Dosen:** [Nama Dosen]
- **Tahun:** 2025

---

## 📄 License

MIT License - Bebas digunakan untuk keperluan edukasi dan non-komersial.

---

## 🙏 Acknowledgments

- David A. Huffman - Penemu algoritma Huffman Coding (1952)
- OpenCV Community - Computer vision library
- Flask Team - Web framework yang mudah digunakan
- Chart.js - Beautiful interactive charts

---

## 📧 Support

Jika ada pertanyaan atau issue:
- Buka issue di GitHub repository
- Email: [email@example.com]
- Diskusi dengan dosen/asisten lab

---

## 🔗 Links

- [Huffman Coding - Wikipedia](https://en.wikipedia.org/wiki/Huffman_coding)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Chart.js Documentation](https://www.chartjs.org/)

---

**Happy Coding! 🚀**

---

*Last updated: 2025*
*Version: 1.0.0*
