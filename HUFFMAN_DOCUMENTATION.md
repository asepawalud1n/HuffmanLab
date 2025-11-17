# Dokumentasi Lengkap: Huffman Image Compression

## 📋 Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Teori Huffman Coding](#teori-huffman-coding)
3. [Implementasi untuk Citra](#implementasi-untuk-citra)
4. [Algoritma Detail](#algoritma-detail)
5. [Kompleksitas](#kompleksitas)
6. [Kelebihan dan Kekurangan](#kelebihan-dan-kekurangan)
7. [Aplikasi](#aplikasi)

---

## 🎯 Pengenalan

### Apa itu Huffman Coding?
**Huffman Coding** adalah algoritma kompresi data lossless yang dikembangkan oleh **David A. Huffman** pada tahun **1952** saat ia masih mahasiswa MIT. Algoritma ini menggunakan pendekatan **greedy** untuk membangun kode prefix optimal berdasarkan frekuensi kemunculan simbol.

### Mengapa Lossless?
- **Tidak ada kehilangan data**: Gambar hasil dekompresi identik 100% dengan aslinya
- **Reversible**: Proses kompresi dapat dibalik sepenuhnya
- **Integrity preserved**: Cocok untuk aplikasi medis, arsip, dokumen penting

### Prinsip Dasar
1. **Variable-Length Encoding**: Simbol yang sering muncul mendapat kode pendek
2. **Prefix-Free Codes**: Tidak ada ambiguitas dalam decoding
3. **Statistical Coding**: Memanfaatkan distribusi probabilitas data
4. **Binary Tree**: Representasi hierarkis untuk encoding/decoding

---

## 🌳 Teori Huffman Coding

### Konsep Variable-Length Coding

**Fixed-Length vs Variable-Length:**

```
Fixed-Length (8 bit per pixel):
Pixel A (freq: 50%) → 00000001 (8 bits)
Pixel B (freq: 30%) → 00000010 (8 bits)
Pixel C (freq: 20%) → 00000011 (8 bits)

Variable-Length (Huffman):
Pixel A (freq: 50%) → 0 (1 bit)
Pixel B (freq: 30%) → 10 (2 bits)
Pixel C (freq: 20%) → 11 (2 bits)

Penghematan = 50%×(8-1) + 30%×(8-2) + 20%×(8-2) = 6.5 bits per pixel!
```

### Prefix-Free Property

**Properti Penting:**
- Tidak ada kode yang menjadi awalan (prefix) dari kode lain
- Memungkinkan decoding tanpa delimiter
- Dijamin oleh struktur binary tree

**Contoh:**
```
✓ Valid Prefix-Free Codes:
  A → 0
  B → 10
  C → 110
  D → 111

✗ Invalid (bukan prefix-free):
  A → 0
  B → 01  ← '0' adalah prefix dari '01'
  C → 011
```

### Pohon Huffman (Huffman Tree)

**Struktur:**
```
         [100]
        /     \
      [A:50]  [50]
             /    \
          [B:30] [C:20]

Codes:
A → 0    (kiri dari root)
B → 10   (kanan, lalu kiri)
C → 11   (kanan, lalu kanan)
```

**Properti:**
- Leaf nodes = simbol/pixel asli
- Internal nodes = gabungan frekuensi
- Path dari root ke leaf = kode biner

---

## 🖼️ Implementasi untuk Citra

### Mengapa Grayscale?

**Alasan Teknis:**
1. **Simplicity**: 1 channel (0-255) vs 3 channels (RGB)
2. **Frequency Table Size**: 256 unique values max vs 16.7 juta (RGB)
3. **Processing Speed**: 3x lebih cepat dari RGB
4. **Memory Efficient**: Huffman tree lebih kecil

**Konversi RGB → Grayscale:**
```python
Gray = 0.299×R + 0.587×G + 0.114×B

Penjelasan koefisien:
- 0.299 (Red): Mata manusia kurang sensitif terhadap merah
- 0.587 (Green): Mata manusia paling sensitif terhadap hijau
- 0.114 (Blue): Mata manusia paling kurang sensitif terhadap biru
```

### Proses Kompresi Citra

**Pipeline Lengkap:**

```
Input Image (RGB)
    ↓
Convert to Grayscale
    ↓
Flatten to 1D Array [p₁, p₂, ..., pₙ]
    ↓
Build Frequency Table {pixel: count}
    ↓
Build Huffman Tree (Priority Queue)
    ↓
Generate Codes {pixel: binary_code}
    ↓
Encode: Replace pixels with codes
    ↓
Pack to Binary (8 bits per byte)
    ↓
Save: .bin + codes.json + size.txt
```

---

## ⚙️ Algoritma Detail

### 1. Build Frequency Table

**Input**: Array of pixels `[128, 255, 128, 64, 255, 128]`

**Proses:**
```python
from collections import Counter

pixels = [128, 255, 128, 64, 255, 128]
freq_table = Counter(pixels)
# Result: {128: 3, 255: 2, 64: 1}
```

**Kompleksitas**: O(n) dimana n = jumlah pixel

---

### 2. Build Huffman Tree

**Algoritma (Greedy):**

```
1. Buat leaf node untuk setiap pixel dengan frekuensinya
2. Masukkan semua node ke min-heap (priority queue)
3. WHILE heap.size > 1:
     a. node_left = heap.pop() (node dengan freq terkecil)
     b. node_right = heap.pop() (node dengan freq kedua terkecil)
     c. new_node = Node(freq = left.freq + right.freq)
     d. new_node.left = node_left
     e. new_node.right = node_right
     f. heap.push(new_node)
4. RETURN heap.pop() (root of tree)
```

**Contoh Step-by-Step:**

```
Initial Heap: [(64,1), (255,2), (128,3)]

Step 1: Pop (64,1) dan (255,2)
        Create merged node: (3)
                           /   \
                        (64,1) (255,2)
        Heap: [(128,3), (merged,3)]

Step 2: Pop (128,3) dan (merged,3)
        Create root: (6)
                    /    \
                (128,3)  (3)
                        /   \
                     (64,1) (255,2)
        Heap: [(root,6)]

Result: Root dengan total freq = 6
```

**Kompleksitas**: O(n log n) dimana n = unique pixels

---

### 3. Generate Codes (DFS Traversal)

**Algoritma:**

```python
def generate_codes(node, code="", codes={}):
    if node is None:
        return

    # Leaf node (pixel value)
    if node.pixel is not None:
        codes[node.pixel] = code if code else "0"
        return

    # Traverse left → add '0'
    generate_codes(node.left, code + "0", codes)

    # Traverse right → add '1'
    generate_codes(node.right, code + "1", codes)

    return codes
```

**Hasil untuk Tree di atas:**
```
128 → 0
64  → 10
255 → 11
```

**Kompleksitas**: O(n) untuk traversal semua nodes

---

### 4. Encode Image

**Proses:**

```python
Original pixels: [128, 255, 128, 64, 255, 128]
Codes: {128: '0', 255: '11', 64: '10'}

Encoded string:
128 → 0
255 → 11
128 → 0
64  → 10
255 → 11
128 → 0

Result: "011010110" (9 bits)

Original size: 6 pixels × 8 bits = 48 bits
Compressed size: 9 bits
Compression ratio: 48/9 = 5.33:1
Savings: 81.25%
```

**Kompleksitas**: O(n) dimana n = jumlah pixel

---

### 5. Pack to Binary

**Masalah**: Bitstring "011010110" perlu disimpan sebagai bytes

**Solusi:**

```python
bitstring = "011010110"

# Padding untuk habis dibagi 8
padding = 8 - (len(bitstring) % 8) = 8 - 1 = 7
bitstring_padded = "011010110" + "0000000" = "0110101100000000"

# Simpan info padding di byte pertama
padding_byte = bytes([7])

# Konversi setiap 8 bit ke 1 byte
byte1 = int("01101011", 2) = 107
byte2 = int("00000000", 2) = 0

# Tulis ke file
file.write(padding_byte + byte1 + byte2)
```

**File Structure:**
```
[Padding Info][Compressed Data...]
[1 byte      ][variable bytes    ]
```

---

### 6. Decode (Dekompresi)

**Algoritma:**

```python
1. Baca file binary
2. Extract padding info (byte pertama)
3. Konversi bytes → bitstring
4. Hapus padding bits
5. Build reverse_codes dari codes.json
6. Decode bitstring:
   current_code = ""
   For each bit in bitstring:
       current_code += bit
       If current_code in reverse_codes:
           output.append(reverse_codes[current_code])
           current_code = ""
7. Reshape array ke ukuran asli
8. Simpan sebagai gambar
```

**Contoh:**

```
Bitstring: "011010110"
Reverse codes: {'0': 128, '11': 255, '10': 64}

Step-by-step:
bit='0' → code='0' → MATCH! → output=[128]
bit='1' → code='1'
bit='1' → code='11' → MATCH! → output=[128, 255]
bit='0' → code='0' → MATCH! → output=[128, 255, 128]
bit='1' → code='1'
bit='0' → code='10' → MATCH! → output=[128, 255, 128, 64]
bit='1' → code='1'
bit='1' → code='11' → MATCH! → output=[128, 255, 128, 64, 255]
bit='0' → code='0' → MATCH! → output=[128, 255, 128, 64, 255, 128]

Final: [128, 255, 128, 64, 255, 128] ✓ Sama dengan asli!
```

---

## 📊 Kompleksitas Algoritma

### Time Complexity

| Operasi | Kompleksitas | Penjelasan |
|---------|--------------|------------|
| Build Frequency Table | O(n) | Scan semua n pixels |
| Build Huffman Tree | O(k log k) | k = unique pixels (max 256) |
| Generate Codes | O(k) | Traversal tree dengan k leaf nodes |
| Encode Image | O(n) | Replace n pixels dengan codes |
| Decode Image | O(m) | m = panjang bitstring |
| **Total Kompresi** | **O(n + k log k)** | Didominasi oleh n |
| **Total Dekompresi** | **O(m)** | Linear terhadap compressed size |

**Catatan**: Untuk citra grayscale, k ≤ 256, sehingga k log k = konstanta kecil

### Space Complexity

| Struktur | Space | Penjelasan |
|----------|-------|------------|
| Frequency Table | O(k) | k = unique pixels (max 256) |
| Huffman Tree | O(k) | 2k-1 total nodes |
| Codes Dictionary | O(k) | Mapping pixel → code |
| Encoded Bitstring | O(n × L_avg) | L_avg = rata-rata panjang kode |
| **Total** | **O(n + k)** | Didominasi oleh n |

---

## ✅ Kelebihan dan Kekurangan

### Kelebihan

1. **Lossless Compression**
   - Tidak ada kehilangan informasi
   - Perfect reconstruction
   - Ideal untuk medical imaging, scientific data

2. **Optimal untuk Distribusi Tertentu**
   - Optimal jika distribusi frekuensi diketahui
   - Guaranteed minimal average code length

3. **Simple & Fast**
   - Algoritma relatif sederhana
   - Implementasi efisien
   - O(n) encoding/decoding

4. **No External Dictionary**
   - Codes generated dari data itu sendiri
   - Self-contained compression

5. **Widely Used**
   - Basis untuk JPEG, PNG, ZIP, GZIP
   - Battle-tested algorithm

### Kekurangan

1. **Overhead Metadata**
   - Harus menyimpan Huffman codes dictionary
   - Size.txt untuk dimensi image
   - Bisa signifikan untuk image kecil

2. **Kurang Optimal untuk Uniform Distribution**
   - Jika semua pixel equally likely → no compression
   - Worst case: data acak → bisa lebih besar!

3. **Integer Bit Lengths**
   - Kode harus integer bit (1, 2, 3, ...)
   - Arithmetic coding bisa lebih optimal (fractional bits)

4. **No Spatial Redundancy**
   - Hanya memanfaatkan statistical redundancy
   - Tidak memanfaatkan pixel tetangga (spatial correlation)
   - Transform coding (DCT, Wavelet) lebih baik untuk natural images

5. **Single-Pass Only**
   - Perlu scan data 2× (frequency + encoding)
   - Tidak bisa streaming real-time

### Perbandingan dengan Algoritma Lain

| Algoritma | Type | Ratio | Speed | Complexity |
|-----------|------|-------|-------|------------|
| **Huffman** | Lossless | 2-4× | Fast | Low |
| **Arithmetic** | Lossless | 2-5× | Medium | Medium |
| **LZW (GIF)** | Lossless | 2-3× | Fast | Low |
| **JPEG** | Lossy | 10-50× | Fast | High |
| **PNG** | Lossless | 2-4× | Medium | Medium |
| **WebP** | Both | 5-30× | Fast | High |

---

## 🎯 Aplikasi Huffman Coding

### 1. Image Compression
- **Grayscale medical images**: X-Ray, CT Scan
- **Fax compression**: CCITT Group 3/4
- **PNG**: DEFLATE (Huffman + LZ77)

### 2. Video Compression
- **MPEG**: Entropy coding stage
- **H.264/H.265**: CABAC (Context-Adaptive Binary Arithmetic Coding)

### 3. File Compression
- **ZIP/GZIP**: DEFLATE algorithm
- **BZIP2**: Burrows-Wheeler + Huffman
- **7-Zip**: LZMA + Huffman

### 4. Network Protocols
- **HTTP/2**: Header compression (HPACK)
- **WebSockets**: Per-message deflate

### 5. Data Storage
- **Database compression**: MySQL, PostgreSQL
- **File systems**: NTFS, ZFS compression

---

## 🔬 Analisis Performa untuk Citra

### Faktor yang Mempengaruhi Compression Ratio

1. **Distribusi Pixel**
   ```
   High variance (many unique pixels) → Lower ratio
   Low variance (few unique pixels) → Higher ratio
   ```

2. **Image Type**
   - **Flat color images**: Ratio tinggi (5-10×)
   - **Natural photos**: Ratio rendah (1.5-2×)
   - **Text/diagrams**: Ratio tinggi (3-8×)
   - **Noise**: Ratio sangat rendah (<1×)

3. **Bit Depth**
   - 1-bit (binary): Excellent compression
   - 8-bit (grayscale): Good compression
   - 24-bit (RGB): Poor compression (too many unique values)

### Contoh Real-World Results

**Test Image: 512×512 grayscale**

| Image Type | Unique Pixels | Original Size | Compressed | Ratio | Savings |
|------------|---------------|---------------|------------|-------|---------|
| Solid color | 1 | 256 KB | 32 bytes | 8192× | 99.99% |
| Gradient | 256 | 256 KB | 128 KB | 2× | 50% |
| Natural photo | 245 | 256 KB | 180 KB | 1.42× | 30% |
| Random noise | 256 | 256 KB | 260 KB | 0.98× | -1.5% |

---

## 💡 Best Practices

### Kapan Menggunakan Huffman?

✅ **Good Use Cases:**
- Medical images (X-Ray, MRI)
- Scanned documents
- Computer-generated graphics
- Logos, diagrams, text
- Archive/backup (dengan LZ77)

❌ **Poor Use Cases:**
- Natural photographs (use JPEG)
- Already compressed data
- Random/encrypted data
- Real-time streaming (prefer simpler coding)

### Optimasi Implementasi

1. **Use efficient data structures**
   - `heapq` untuk priority queue (O(log n))
   - `dict` untuk O(1) lookup

2. **Minimize memory copies**
   - Process in-place when possible
   - Use generators for large data

3. **Parallel processing**
   - Frequency counting bisa diparalelkan
   - Batch processing untuk multiple images

4. **Caching**
   - Reuse Huffman tree untuk similar images
   - Pre-compute codes untuk standard palettes

---

## 📚 Referensi

1. **Original Paper**:
   Huffman, D. A. (1952). "A Method for the Construction of Minimum-Redundancy Codes". Proceedings of the IRE.

2. **Books**:
   - "Introduction to Data Compression" - Khalid Sayood
   - "The Data Compression Book" - Mark Nelson

3. **Standards**:
   - ISO/IEC 10918 (JPEG)
   - RFC 1951 (DEFLATE)
   - ITU-T T.81 (JPEG)

4. **Online Resources**:
   - [Wikipedia: Huffman Coding](https://en.wikipedia.org/wiki/Huffman_coding)
   - [Brilliant.org: Huffman Encoding](https://brilliant.org/wiki/huffman-encoding/)

---

## 🎓 Kesimpulan

**Huffman Coding** adalah algoritma kompresi lossless yang elegant dan efisien, sangat cocok untuk data dengan distribusi frekuensi yang tidak uniform. Meskipun bukan yang paling optimal untuk natural images, ia tetap menjadi building block fundamental dalam banyak algoritma kompresi modern.

**Key Takeaways:**
- ✅ Lossless, optimal untuk distribusi tertentu
- ✅ Simple, fast, widely applicable
- ✅ Basis untuk JPEG, PNG, ZIP, dll
- ❌ Memerlukan metadata (codes dictionary)
- ❌ Kurang optimal untuk uniform/random data
- ❌ Tidak memanfaatkan spatial correlation

**Untuk project ini**, Huffman coding diimplementasikan dengan:
- Konversi RGB → Grayscale
- Priority queue untuk build tree
- DFS traversal untuk generate codes
- Efficient binary packing
- Complete metadata preservation

---

**Dibuat dengan ❤️ untuk Pengolahan Citra Digital Lab**
