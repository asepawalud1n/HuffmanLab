# TEORI HUFFMAN CODING UNTUK KOMPRESI CITRA

## 📚 Daftar Isi
1. [Pengertian Huffman Coding](#pengertian)
2. [Sejarah dan Latar Belakang](#sejarah)
3. [Cara Kerja Huffman Coding](#cara-kerja)
4. [Huffman Coding pada Citra Digital](#huffman-pada-citra)
5. [Tahapan Encoding dan Decoding](#tahapan)
6. [Kelebihan dan Kekurangan](#kelebihan-kekurangan)
7. [Perbandingan dengan Metode Lain](#perbandingan)
8. [Aplikasi dalam Dunia Nyata](#aplikasi)

---

## 1. Pengertian Huffman Coding {#pengertian}

**Huffman Coding** adalah algoritma kompresi data **lossless** (tanpa kehilangan data) yang dikembangkan oleh **David A. Huffman** pada tahun **1952** saat ia masih mahasiswa di MIT.

### Prinsip Dasar
Huffman Coding menggunakan **kode biner dengan panjang variabel** (*variable-length coding*) untuk merepresentasikan simbol/karakter. Prinsip utamanya:

- **Simbol yang sering muncul** → Kode pendek (misal: `0`, `10`)
- **Simbol yang jarang muncul** → Kode panjang (misal: `11010`, `111001`)

### Karakteristik Utama
1. **Lossless**: Data asli dapat dipulihkan 100% tanpa kehilangan informasi
2. **Prefix-Free Code**: Tidak ada kode yang menjadi prefix dari kode lain
3. **Optimal**: Menghasilkan rata-rata panjang kode terpendek untuk distribusi probabilitas tertentu
4. **Entropy Coding**: Memanfaatkan statistik frekuensi data

---

## 2. Sejarah dan Latar Belakang {#sejarah}

### Timeline Historis

| Tahun | Peristiwa |
|-------|-----------|
| **1952** | David Huffman menemukan algoritma Huffman Coding dalam tugasnya di MIT |
| **1950s** | Algoritma mulai digunakan dalam transmisi data |
| **1970s** | Diterapkan dalam kompresi file dan komunikasi digital |
| **1980s-90s** | Menjadi basis untuk format kompresi populer (JPEG, MP3, ZIP) |
| **2000s** | Terus digunakan dalam kompresi modern dan streaming |

### Konteks Penemuan
- Huffman adalah mahasiswa dalam kursus teori informasi Robert Fano di MIT
- Tugas: Temukan kode biner paling efisien
- Alternatif waktu itu: **Shannon-Fano Coding** (kurang optimal)
- Huffman menemukan solusi yang **terbukti optimal**

---

## 3. Cara Kerja Huffman Coding {#cara-kerja}

### A. Konsep Pohon Biner (Binary Tree)

Huffman Coding menggunakan **pohon biner** untuk membuat kode:

```
          [100]
         /      \
       [45]     [55]
       / \       / \
     [20][25] [30][25]
      A   B    C   D
```

**Aturan:**
- **Kiri** → bit `0`
- **Kanan** → bit `1`

**Contoh Kode:**
- A = `00` (45 → 20)
- B = `01` (45 → 25)
- C = `10` (55 → 30)
- D = `11` (55 → 25)

### B. Algoritma Pembangunan Pohon

#### Langkah-langkah:
1. **Hitung frekuensi** setiap simbol
2. **Buat node** untuk setiap simbol dengan frekuensinya
3. **Masukkan** semua node ke priority queue (min-heap)
4. **Loop** sampai tersisa 1 node:
   - Ambil 2 node dengan frekuensi terkecil
   - Gabungkan menjadi node baru (frekuensi = jumlah keduanya)
   - Masukkan kembali ke queue
5. **Node terakhir** = root pohon Huffman

#### Contoh Praktis:

**Data:** `AAABBBCCCD`

**Frekuensi:**
- A: 3
- B: 3
- C: 3
- D: 1

**Proses Pembangunan:**

```
Step 1: Queue = [D:1, A:3, B:3, C:3]

Step 2: Gabung D(1) + C(3) = DC(4)
        Queue = [A:3, B:3, DC:4]

Step 3: Gabung A(3) + B(3) = AB(6)
        Queue = [DC:4, AB:6]

Step 4: Gabung DC(4) + AB(6) = Root(10)
        Queue = [Root:10]

Pohon Final:
          Root(10)
         /         \
       DC(4)      AB(6)
       /  \        /  \
     D(1) C(3)   A(3) B(3)

Kode:
- D = 00
- C = 01
- A = 10
- B = 11
```

### C. Prefix-Free Property

**Definisi:** Tidak ada kode yang menjadi awalan (prefix) dari kode lain.

**Contoh:**
- ✅ Valid: `{0, 10, 11}` - Tidak ada yang prefix dari yang lain
- ❌ Invalid: `{0, 01, 011}` - `0` adalah prefix dari `01` dan `011`

**Keuntungan:**
- Decoding **tidak ambigu**
- Tidak perlu delimiter/separator

---

## 4. Huffman Coding pada Citra Digital {#huffman-pada-citra}

### A. Representasi Citra

**Citra Grayscale:**
- Setiap pixel: nilai 0-255 (8 bit)
- Ukuran asli: `width × height × 8 bits`

**Contoh:**
- Gambar 100×100 pixels
- Ukuran asli: `100 × 100 × 8 = 80,000 bits`

### B. Proses Kompresi Citra

#### 1. Preprocessing
```python
# Baca gambar
img = cv2.imread('image.jpg')

# Konversi ke grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Flatten menjadi 1D array
pixels = gray.flatten()  # [124, 125, 124, 200, ...]
```

#### 2. Analisis Frekuensi
```python
from collections import Counter

freq = Counter(pixels)
# {124: 500, 125: 350, 200: 100, ...}
```

#### 3. Pembangunan Pohon Huffman
```python
# Build Huffman tree
tree = build_huffman_tree(freq)

# Generate codes
codes = generate_codes(tree)
# {124: '10', 125: '110', 200: '11110', ...}
```

#### 4. Encoding
```python
# Encode setiap pixel
encoded = ''.join([codes[pixel] for pixel in pixels])
# '1011010111110...'
```

#### 5. Simpan ke File Binary
```python
# Konversi bitstring ke bytes
with open('compressed.bin', 'wb') as f:
    # Simpan bitstream
    for i in range(0, len(encoded), 8):
        byte = int(encoded[i:i+8], 2)
        f.write(bytes([byte]))
```

### C. Karakteristik Kompresi Citra

**Rasio Kompresi** bergantung pada:

1. **Distribusi Pixel:**
   - Gambar dengan banyak pixel yang sama → rasio tinggi
   - Gambar dengan distribusi merata → rasio rendah

2. **Jenis Gambar:**
   - Logo, kartun, diagram → rasio tinggi (banyak area uniform)
   - Foto alam, tekstur → rasio rendah (variasi tinggi)

**Contoh Perbandingan:**

| Jenis Gambar | Unique Pixels | Rasio Kompresi |
|--------------|---------------|----------------|
| Logo Hitam-Putih | 2 | 7-8:1 |
| Diagram Sederhana | 10-20 | 3-5:1 |
| Foto Landscape | 200-255 | 1.1-1.3:1 |
| Noise Random | 255 | ~1:1 (tidak efektif) |

---

## 5. Tahapan Encoding dan Decoding {#tahapan}

### A. Proses ENCODING

#### Flowchart Encoding:
```
┌─────────────────┐
│  Input Image    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Convert to Gray │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Flatten Array  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Count Frequency │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Build Huffman   │
│      Tree       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Codes  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Encode Pixels   │
│  to Bitstream   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save to .bin   │
│  Save codes.json│
│  Save size.txt  │
└─────────────────┘
```

#### Detail Setiap Step:

**Step 1: Input & Grayscale**
- Input: Gambar warna (RGB/BGR)
- Output: Gambar grayscale (1 channel, 0-255)
- Rumus: `Gray = 0.299R + 0.587G + 0.114B`

**Step 2: Flatten**
- Input: Array 2D (height × width)
- Output: Array 1D (height × width)
- Contoh: `[[1,2],[3,4]]` → `[1,2,3,4]`

**Step 3: Frequency Count**
- Input: Array pixel values
- Output: Dictionary {pixel: frequency}
- Algoritma: Counting / Hash Map

**Step 4: Build Tree**
- Input: Frequency table
- Output: Root node pohon Huffman
- Algoritma: Greedy dengan min-heap

**Step 5: Generate Codes**
- Input: Root tree
- Output: Dictionary {pixel: code}
- Algoritma: DFS traversal

**Step 6: Encode**
- Input: Pixel array + codes
- Output: Bitstring
- Kompleksitas: O(n) dimana n = jumlah pixel

**Step 7: Save Files**
- `compressed.bin`: Bitstream dalam bentuk bytes
- `codes.json`: Mapping pixel → kode (untuk decode)
- `size.txt`: Dimensi gambar (height, width)

### B. Proses DECODING

#### Flowchart Decoding:
```
┌─────────────────┐
│  Load Files:    │
│  - .bin         │
│  - codes.json   │
│  - size.txt     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Read Bitstream  │
│  from .bin      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Reverse Codes  │
│ code → pixel    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Decode Bitstream│
│  to Pixel Array │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Reshape to 2D   │
│ (height × width)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save Image     │
│   (lossless)    │
└─────────────────┘
```

#### Detail Decoding:

**Step 1: Load Files**
```python
# Load codes
with open('codes.json') as f:
    codes = json.load(f)
    reverse_codes = {v: int(k) for k, v in codes.items()}

# Load size
with open('size.txt') as f:
    height, width = map(int, f.read().split(','))

# Load binary
with open('compressed.bin', 'rb') as f:
    binary_data = f.read()
```

**Step 2: Bitstream Decoding**
```python
# Convert bytes to bitstring
bitstring = ''.join([bin(byte)[2:].zfill(8) for byte in binary_data])

# Decode
pixels = []
current_code = ""

for bit in bitstring:
    current_code += bit
    if current_code in reverse_codes:
        pixels.append(reverse_codes[current_code])
        current_code = ""
```

**Step 3: Reshape**
```python
# Convert to numpy array
pixel_array = np.array(pixels, dtype=np.uint8)

# Reshape
image = pixel_array.reshape((height, width))
```

**Step 4: Save**
```python
cv2.imwrite('decompressed.png', image)
```

### C. Kenapa Huffman Bersifat Lossless?

**Alasan Matematis:**

1. **Bijektif (One-to-One Mapping)**
   - Setiap pixel value memiliki **satu** kode unik
   - Setiap kode merepresentasikan **satu** pixel value
   - Tidak ada informasi yang hilang dalam pemetaan

2. **Prefix-Free Property**
   - Decoding tidak ambigu
   - Setiap kode dapat di-decode secara unik

3. **Reversible Process**
   - Encoding: pixel → code
   - Decoding: code → pixel (exact reverse)

**Bukti:**
```
Original:  [124, 125, 124, 200]
           ↓ (encode)
Encoded:   "10110110111110"
           ↓ (decode)
Decoded:   [124, 125, 124, 200]  ← SAMA PERSIS
```

---

## 6. Kelebihan dan Kekurangan {#kelebihan-kekurangan}

### A. KELEBIHAN

#### 1. Lossless Compression ✅
- **Keuntungan:** Data asli dapat dipulihkan 100%
- **Use Case:** Medical imaging, dokumen penting, arsip
- **Contoh:** Gambar 1000×1000 → kompresi → decompresi → **identik pixel-by-pixel**

#### 2. Optimal untuk Distribusi yang Diketahui ✅
- **Teorema:** Huffman menghasilkan kode terpendek untuk distribusi frekuensi yang diberikan
- **Bukti:** Shannon's Source Coding Theorem
- **Kondisi:** Saat probabilitas simbol diketahui dengan pasti

#### 3. Sederhana dan Efisien ✅
- **Kompleksitas:**
  - Build tree: O(n log n)
  - Encoding: O(n)
  - Decoding: O(n)
- **Memory:** O(unique symbols)

#### 4. Adaptif ✅
- Dapat digunakan untuk berbagai jenis data
- Tidak terbatas pada tipe data tertentu
- Dapat dikombinasikan dengan metode lain

#### 5. Prefix-Free ✅
- Decoding real-time tanpa lookahead
- Tidak perlu delimiter/separator
- Stream processing friendly

### B. KEKURANGAN

#### 1. Butuh Dua Pass ❌
- **Pass 1:** Hitung frekuensi
- **Pass 2:** Encoding
- **Dampak:** Tidak bisa streaming encoding real-time
- **Solusi:** Adaptive Huffman Coding

#### 2. Overhead Metadata ❌
- Harus menyimpan:
  - Huffman tree / code table
  - Image dimensions
- **Ukuran overhead:**
  - Codes table: ~2-5 KB (untuk 256 unique pixels)
  - Size info: ~10 bytes
- **Masalah:** Untuk file kecil, overhead bisa > data terkompresi

#### 3. Tidak Optimal untuk Data Uniform ❌
- **Contoh:** Gambar dengan distribusi pixel merata
- **Rasio:** Mendekati 1:1 (tidak ada kompresi signifikan)
- **Alasan:** Semua pixel punya frekuensi mirip → kode mirip panjangnya

#### 4. Tidak Memanfaatkan Redundansi Spasial ❌
- Huffman hanya lihat frekuensi individual
- Tidak melihat pola/pattern 2D
- **Contoh:** Area uniform di gambar tidak di-leverage

#### 5. Integer Bit Limitation ❌
- Panjang kode harus integer (1, 2, 3 bit...)
- **Teoritis optimal:** Entropy = log₂(1/p) bisa non-integer
- **Contoh:** Symbol dengan p=1/3 → optimal 1.58 bit, tapi Huffman beri 2 bit

### C. Perbandingan Trade-offs

| Aspek | Huffman | Arithmetic Coding | LZW | JPEG |
|-------|---------|-------------------|-----|------|
| Lossless | ✅ | ✅ | ✅ | ❌ |
| Rasio Kompresi | Sedang | Tinggi | Tinggi | Sangat Tinggi |
| Kecepatan | Cepat | Lambat | Cepat | Sedang |
| Kompleksitas | Rendah | Tinggi | Sedang | Tinggi |
| Overhead | Rendah | Sangat Rendah | Sedang | Rendah |

---

## 7. Perbandingan dengan Metode Lain {#perbandingan}

### A. Huffman vs Run-Length Encoding (RLE)

**Run-Length Encoding:**
- Encoding: `AAAABBBCC` → `4A3B2C`
- Optimal untuk: Data dengan banyak run (sequence berulang)

**Perbandingan:**

| Kriteria | Huffman | RLE |
|----------|---------|-----|
| **Prinsip** | Frekuensi simbol | Panjang run |
| **Optimal untuk** | Distribusi tidak merata | Run panjang |
| **Worst case** | Data uniform | Data alternating |
| **Contoh Baik** | Teks, audio | Bitmap, fax |

**Contoh:**
- Data: `AAABBBCCC`
  - Huffman: Build tree → encode (overhead)
  - RLE: `3A3B3C` (sangat efisien)

- Data: `ABCABCABC`
  - Huffman: Baik (frekuensi sama untuk A, B, C)
  - RLE: Buruk (`1A1B1C1A1B1C1A1B1C` → lebih besar!)

### B. Huffman vs LZW (Lempel-Ziv-Welch)

**LZW:**
- Digunakan di: GIF, TIFF, Unix compress
- Prinsip: Dictionary-based, pattern matching
- Adaptive: Dictionary dibangun saat encoding

**Perbandingan:**

| Kriteria | Huffman | LZW |
|----------|---------|-----|
| **Tipe** | Statistical | Dictionary |
| **Adaptif** | Static (perlu 2 pass) | Dynamic (1 pass) |
| **Redundansi** | Individual symbols | Patterns/sequences |
| **Rasio** | 1.1-2:1 | 2-4:1 |

**Kasus Penggunaan:**
- **Huffman:** Ketika distribusi frekuensi diketahui, file kecil
- **LZW:** File besar dengan pattern berulang, streaming

### C. Huffman vs Arithmetic Coding

**Arithmetic Coding:**
- Encode seluruh message sebagai satu angka floating-point
- Optimal secara teoritis (mendekati entropy limit)

**Perbandingan:**

| Kriteria | Huffman | Arithmetic |
|----------|---------|------------|
| **Bit per symbol** | Integer (1,2,3,...) | Fractional (1.5, 2.3,...) |
| **Optimality** | Near-optimal | Optimal |
| **Kompleksitas** | O(n log n) | O(n) tapi konstanta besar |
| **Implementasi** | Sederhana | Rumit (floating point) |
| **Overhead** | Code table | Probability model |

**Contoh:**
- Symbol dengan probability 1/3:
  - **Huffman:** 2 bits (ceil(log₂3))
  - **Arithmetic:** ~1.58 bits (optimal)

### D. Huffman vs JPEG

**JPEG:**
- Lossy compression
- Menggunakan DCT (Discrete Cosine Transform)
- Huffman sebagai **salah satu komponen** JPEG

**Alur JPEG:**
```
Image → DCT → Quantization → Huffman Encoding → Compressed
```

**Perbandingan:**

| Kriteria | Huffman (Pure) | JPEG |
|----------|---------------|------|
| **Lossless** | ✅ Yes | ❌ No |
| **Rasio** | 1.1-2:1 | 10-50:1 |
| **Quality** | Perfect | Configurable |
| **Use Case** | Archival | Photos, web |

---

## 8. Aplikasi dalam Dunia Nyata {#aplikasi}

### A. Format File yang Menggunakan Huffman

#### 1. **JPEG**
- Tahap: Entropy encoding setelah DCT dan quantization
- Variasi: DHT (Define Huffman Table)
- Rasio kontribusi: ~20-30% dari total kompresi

#### 2. **MP3**
- Bagian: Huffman untuk mengkompresi scale factors
- Kombinasi dengan: MDCT, psychoacoustic model
- Standard: ISO/IEC 11172-3

#### 3. **ZIP / DEFLATE**
- Algoritma: LZ77 + Huffman
- Digunakan di: .zip, .png, .gzip
- Efektivitas: Rasio 2-10:1

#### 4. **PNG**
- Tahap: Filtering → DEFLATE (LZ77 + Huffman)
- Lossless: ✅
- Rasio: 1.5-3:1 untuk photos, 10:1+ untuk graphics

#### 5. **FAX (CCITT Group 3/4)**
- Modified Huffman (MH)
- Kombinasi dengan: RLE
- Rasio: 5-15:1 untuk dokumen

### B. Bidang Aplikasi

#### 1. **Medical Imaging**
- **DICOM:** Format standar medical imaging
- **Requirement:** Lossless (untuk diagnosis akurat)
- **Huffman Role:** Lossless JPEG mode
- **Contoh:** CT scan, MRI, X-ray digital

#### 2. **Transmisi Data**
- **Modem:** V.42bis protocol
- **Satellite:** Data transmission
- **Networking:** HTTP compression (gzip)

#### 3. **Multimedia**
- **Video:** H.264, HEVC (sebagai komponen)
- **Audio:** MP3, AAC
- **Streaming:** Adaptive bitrate encoding

#### 4. **Archival & Backup**
- **Backup software:** System backups
- **Document management:** PDF compression
- **Database:** Log compression

### C. Implementasi Hardware

**FPGA/ASIC Implementation:**
- Real-time video encoding
- Network routers (packet compression)
- Storage controllers

**Optimizations:**
- Parallel tree building
- Lookup table for codes
- Pipelined encoding/decoding

---

## 📊 KESIMPULAN

### Kapan Menggunakan Huffman?

✅ **GUNAKAN** Huffman jika:
- Butuh kompresi **lossless**
- Distribusi frekuensi tidak uniform
- Implementasi sederhana lebih penting dari rasio maksimal
- Real-time decoding diperlukan
- File size kecil-menengah

❌ **JANGAN** gunakan Huffman jika:
- Lossy compression acceptable → JPEG, JPEG2000
- Data sangat uniform → tidak efektif
- Pattern/sequence redundancy dominan → LZW, LZ77
- Maximum compression critical → Arithmetic Coding, LZMA

### Formula Kunci

**Entropy (Shannon):**
```
H = -Σ p(x) log₂ p(x)
```

**Average Code Length (Huffman):**
```
L = Σ p(x) · length(code(x))
```

**Compression Ratio:**
```
Ratio = Original Size / Compressed Size
```

**Optimal Condition:**
```
L ≥ H  (Huffman mendekati entropy)
```

---

## 🔗 REFERENSI

1. Huffman, D. A. (1952). "A Method for the Construction of Minimum-Redundancy Codes". Proceedings of the IRE, 40(9), 1098-1101.

2. Cover, T. M., & Thomas, J. A. (2006). Elements of Information Theory (2nd ed.). Wiley-Interscience.

3. Salomon, D. (2007). Data Compression: The Complete Reference (4th ed.). Springer.

4. Sayood, K. (2017). Introduction to Data Compression (5th ed.). Morgan Kaufmann.

5. ISO/IEC 10918-1: JPEG Standard (Information technology — Digital compression and coding of continuous-tone still images)

---

**Prepared by:** Pengolahan Citra Digital Lab
**Last Updated:** 2025
**Version:** 1.0
