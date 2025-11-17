# DIAGRAM SISTEM - HUFFMAN IMAGE COMPRESSION

## 📚 Daftar Isi
1. [Flowchart Sistem](#flowchart)
2. [Data Flow Diagram (DFD)](#dfd)
3. [Entity Relationship Diagram (ERD)](#erd)
4. [Arsitektur Sistem](#arsitektur)

---

## 1. FLOWCHART SISTEM {#flowchart}

### A. Flowchart Kompresi Single Image

```
                    START
                      │
                      ▼
         ┌────────────────────────┐
         │  User Upload Gambar    │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │  Validasi File Type    │
         │  (JPG/PNG/BMP?)        │
         └───────────┬────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
        Valid?               Invalid
          │                     │
          │                     ▼
          │          ┌──────────────────┐
          │          │ Return Error 400 │
          │          │ "Invalid file"   │
          │          └──────────────────┘
          │                     │
          │                     ▼
          │                   END
          │
          ▼
  ┌──────────────────┐
  │  Save to Upload  │
  │     Folder       │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Read Image with  │
  │    OpenCV        │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Convert to       │
  │   Grayscale      │
  │ (BGR → GRAY)     │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Flatten to 1D    │
  │ Pixel Array      │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Hitung Frekuensi │
  │  Setiap Pixel    │
  │  (Counter)       │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Build Huffman   │
  │      Tree        │
  │  (Min Heap)      │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Generate Huffman │
  │      Codes       │
  │  (DFS Traversal) │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Encode Pixels   │
  │  to Bitstream    │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Save Files:     │
  │  • .bin          │
  │  • codes.json    │
  │  • size.txt      │
  │  • gray.png      │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Calculate Stats: │
  │  • Original Size │
  │  • Compressed    │
  │  • Ratio         │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Render result.   │
  │   html dengan    │
  │   statistik      │
  └─────────┬────────┘
            │
            ▼
          END
```

### B. Flowchart Dekompresi

```
                    START
                      │
                      ▼
         ┌────────────────────────┐
         │ User Upload 3 Files:   │
         │ • compressed.bin       │
         │ • codes.json           │
         │ • size.txt             │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ Validasi 3 File        │
         │     Lengkap?           │
         └───────────┬────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
        Valid?               Invalid
          │                     │
          │                     ▼
          │          ┌──────────────────┐
          │          │ Return Error 400 │
          │          │ "Missing files"  │
          │          └──────────────────┘
          │                     │
          │                     ▼
          │                   END
          │
          ▼
  ┌──────────────────┐
  │  Read codes.json │
  │  Parse ke Dict   │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Read size.txt   │
  │ Get height,width │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Read .bin File  │
  │ Load Binary Data │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Convert Bytes to │
  │    Bitstring     │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Reverse Codes:  │
  │ code → pixel val │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Decode Loop:    │
  │ Match codes →    │
  │ Append pixels    │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Convert to Numpy │
  │     Array        │
  │  (uint8)         │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Reshape to 2D    │
  │ (height × width) │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │  Save as PNG     │
  │   (lossless)     │
  └─────────┬────────┘
            │
            ▼
  ┌──────────────────┐
  │ Return File for  │
  │    Download      │
  └─────────┬────────┘
            │
            ▼
          END
```

### C. Flowchart Kompresi Dataset

```
                    START
                      │
                      ▼
         ┌────────────────────────┐
         │ User Upload Multiple   │
         │      Images            │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │  Validasi File Types   │
         │   Filter Valid Only    │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │  Initialize Results    │
         │      List = []         │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │   FOR EACH Image       │◄────┐
         └───────────┬────────────┘     │
                     │                  │
                     ▼                  │
         ┌────────────────────────┐     │
         │  Process Single Image: │     │
         │  • Grayscale           │     │
         │  • Flatten             │     │
         │  • Build Huffman       │     │
         │  • Encode              │     │
         │  • Save Files          │     │
         └───────────┬────────────┘     │
                     │                  │
                     ▼                  │
         ┌────────────────────────┐     │
         │ Calculate Stats untuk  │     │
         │    Image ini           │     │
         └───────────┬────────────┘     │
                     │                  │
                     ▼                  │
         ┌────────────────────────┐     │
         │ Append to Results List │     │
         └───────────┬────────────┘     │
                     │                  │
                     ▼                  │
         ┌────────────────────────┐     │
         │   More Images?         ├─YES─┘
         └───────────┬────────────┘
                     │ NO
                     ▼
         ┌────────────────────────┐
         │ Calculate Dataset      │
         │      Statistics:       │
         │  • Mean Ratio          │
         │  • Median Ratio        │
         │  • Max/Min Ratio       │
         │  • Total Savings       │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │  Prepare Chart Data:   │
         │  • Labels              │
         │  • Original Sizes      │
         │  • Compressed Sizes    │
         │  • Ratios              │
         └───────────┬────────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │ Render dataset_result. │
         │   html dengan:         │
         │  • Table               │
         │  • Stats Cards         │
         │  • Charts (Bar/Line/Pie)│
         └───────────┬────────────┘
                     │
                     ▼
                   END
```

---

## 2. DATA FLOW DIAGRAM (DFD) {#dfd}

### A. Context Diagram (DFD Level 0)

```
                               ┌──────────────┐
                               │              │
                   Upload      │              │   Compressed
                   Gambar ────►│              │   Files + Stats
                               │              ├──────────────►
                               │              │
                               │   HUFFMAN    │
                   Upload      │    IMAGE     │   Decompressed
                   3 Files ───►│ COMPRESSION  │   Image
                   (.bin,      │    SYSTEM    ├──────────────►
                   .json,      │              │
                   .txt)       │              │
                               │              │   CSV Export
                   Upload  ────►│              │   Dataset
                   Dataset     │              ├──────────────►
                               │              │
                               └──────────────┘
                                    USER
```

### B. DFD Level 1 - Kompresi Single Image

```
    USER
      │
      │ 1. Upload Image
      ▼
┌──────────────┐
│   PROCESS    │
│  1.1 Upload  │
│  & Validate  │
└──────┬───────┘
       │ Image File
       ▼
┌──────────────┐        ┌──────────────┐
│   PROCESS    │        │ DATA STORE   │
│1.2 Grayscale │───────►│ D1: Uploads  │
│ & Flatten    │        └──────────────┘
└──────┬───────┘
       │ Pixel Array
       ▼
┌──────────────┐
│   PROCESS    │
│ 1.3 Huffman  │
│   Encoding   │
└──────┬───────┘
       │ Codes + Bitstream
       ▼
┌──────────────┐        ┌──────────────┐
│   PROCESS    │        │ DATA STORE   │
│  1.4 Save    │───────►│D2: Compressed│
│  Compressed  │        └──────────────┘
└──────┬───────┘
       │ Stats
       ▼
┌──────────────┐
│   PROCESS    │
│ 1.5 Generate │
│   Report     │
└──────┬───────┘
       │ HTML Result
       ▼
     USER
```

### C. DFD Level 1 - Dekompresi

```
    USER
      │
      │ 1. Upload 3 Files
      ▼
┌──────────────┐        ┌──────────────┐
│   PROCESS    │        │ DATA STORE   │
│  2.1 Load    │◄───────│D2: Compressed│
│    Files     │        └──────────────┘
└──────┬───────┘
       │ Binary + Codes + Size
       ▼
┌──────────────┐
│   PROCESS    │
│ 2.2 Decode   │
│  Bitstream   │
└──────┬───────┘
       │ Pixel Array
       ▼
┌──────────────┐
│   PROCESS    │
│ 2.3 Reshape  │
│  & Save PNG  │
└──────┬───────┘
       │
       ▼
┌──────────────┐        ┌──────────────┐
│   PROCESS    │        │ DATA STORE   │
│  2.4 Store   │───────►│D3:Decompressed│
│  Result      │        └──────────────┘
└──────┬───────┘
       │ Image File
       ▼
     USER
```

### D. DFD Level 1 - Dataset Processing

```
    USER
      │
      │ 1. Upload Multiple Images
      ▼
┌──────────────┐
│   PROCESS    │
│  3.1 Batch   │
│  Validation  │
└──────┬───────┘
       │ Valid Images List
       ▼
┌──────────────┐        ┌──────────────┐
│   PROCESS    │        │ DATA STORE   │
│ 3.2 Loop:    │◄──────►│ D1: Uploads  │
│ Compress Each│        │ D2: Compressed│
│    Image     │        └──────────────┘
└──────┬───────┘
       │ Results Array
       ▼
┌──────────────┐
│   PROCESS    │
│ 3.3 Calculate│
│  Statistics  │
└──────┬───────┘
       │ Stats Data
       ▼
┌──────────────┐
│   PROCESS    │
│ 3.4 Generate │
│ Charts Data  │
└──────┬───────┘
       │ Chart Config
       ▼
┌──────────────┐
│   PROCESS    │
│ 3.5 Render   │
│    Report    │
└──────┬───────┘
       │ HTML + Charts
       ▼
     USER
```

### E. DFD Level 2 - Proses Huffman Encoding Detail

```
   Pixel Array
      │
      ▼
┌──────────────┐
│  PROCESS     │
│ 3.1 Count    │
│  Frequency   │
└──────┬───────┘
       │ Freq Table
       ▼
┌──────────────┐
│  PROCESS     │
│ 3.2 Create   │
│ Leaf Nodes   │
└──────┬───────┘
       │ Nodes List
       ▼
┌──────────────┐
│  PROCESS     │
│3.3 Build Min │
│     Heap     │
└──────┬───────┘
       │ Priority Queue
       ▼
┌──────────────┐
│  PROCESS     │
│ 3.4 Merge    │
│    Nodes     │
│  (Greedy)    │
└──────┬───────┘
       │ Huffman Tree
       ▼
┌──────────────┐
│  PROCESS     │
│ 3.5 Traverse │
│ Tree (DFS)   │
└──────┬───────┘
       │ Codes Dict
       ▼
┌──────────────┐
│  PROCESS     │
│ 3.6 Encode   │
│    Pixels    │
└──────┬───────┘
       │ Bitstream
       ▼
   Output
```

---

## 3. ENTITY RELATIONSHIP DIAGRAM (ERD) {#erd}

### Catatan ERD
Meskipun sistem ini **tidak menggunakan database**, kita dapat memodelkan entitas dan relasinya untuk memahami struktur data.

### A. ERD Konseptual

```
┌─────────────────┐           ┌─────────────────┐
│     IMAGE       │           │  COMPRESSION    │
│─────────────────│           │─────────────────│
│ • filename      │───────────│ • compressed_id │
│ • filepath      │ 1      1  │ • original_size │
│ • format        │───────────│ • compressed_sz │
│ • upload_time   │ menghasilkan• ratio       │
│ • dimensions    │           │ • timestamp     │
└─────────────────┘           └────────┬────────┘
                                       │
                                       │ 1
                                       │
                                       │ memiliki
                                       │
                                       │ 1
                              ┌────────┴────────┐
                              │  HUFFMAN_CODES  │
                              │─────────────────│
                              │ • pixel_value   │
                              │ • code          │
                              │ • frequency     │
                              └─────────────────┘
```

### B. ERD Detail dengan Atribut

```
┌─────────────────────────────┐
│          IMAGE              │
├─────────────────────────────┤
│ PK: image_id                │
│────────────────────────────│
│ • filename (VARCHAR)        │
│ • original_path (VARCHAR)   │
│ • file_format (ENUM)        │
│ • upload_timestamp (DATETIME)│
│ • height (INT)              │
│ • width (INT)               │
│ • total_pixels (INT)        │
│ • unique_pixels (INT)       │
└──────────┬──────────────────┘
           │
           │ 1:1
           │
┌──────────┴──────────────────┐
│      COMPRESSION_RESULT     │
├─────────────────────────────┤
│ PK: compression_id          │
│ FK: image_id                │
│─────────────────────────────│
│ • original_size_bits (BIGINT)│
│ • compressed_size_bits (BIGINT)│
│ • compression_ratio (FLOAT) │
│ • savings_percent (FLOAT)   │
│ • compression_time (FLOAT)  │
│ • timestamp (DATETIME)      │
│ • bin_path (VARCHAR)        │
│ • codes_path (VARCHAR)      │
│ • size_path (VARCHAR)       │
└──────────┬──────────────────┘
           │
           │ 1:N
           │
┌──────────┴──────────────────┐
│       HUFFMAN_CODE          │
├─────────────────────────────┤
│ PK: code_id                 │
│ FK: compression_id          │
│─────────────────────────────│
│ • pixel_value (TINYINT)     │
│ • huffman_code (VARCHAR)    │
│ • frequency (INT)           │
│ • code_length (TINYINT)     │
└─────────────────────────────┘


┌─────────────────────────────┐
│         DATASET             │
├─────────────────────────────┤
│ PK: dataset_id              │
│─────────────────────────────│
│ • dataset_name (VARCHAR)    │
│ • upload_timestamp (DATETIME)│
│ • total_images (INT)        │
│ • total_original_kb (FLOAT) │
│ • total_compressed_kb (FLOAT)│
│ • mean_ratio (FLOAT)        │
│ • median_ratio (FLOAT)      │
│ • max_ratio (FLOAT)         │
│ • min_ratio (FLOAT)         │
└──────────┬──────────────────┘
           │
           │ 1:N
           │
┌──────────┴──────────────────┐
│     DATASET_IMAGE           │
├─────────────────────────────┤
│ PK: dataset_image_id        │
│ FK: dataset_id              │
│ FK: image_id                │
│─────────────────────────────│
│ • sequence_number (INT)     │
└─────────────────────────────┘
```

### C. Kardinalitas Relasi

| Relasi | Entitas 1 | Kardinalitas | Entitas 2 | Deskripsi |
|--------|-----------|--------------|-----------|-----------|
| R1 | IMAGE | 1:1 | COMPRESSION_RESULT | Satu gambar memiliki satu hasil kompresi |
| R2 | COMPRESSION_RESULT | 1:N | HUFFMAN_CODE | Satu kompresi memiliki banyak kode Huffman |
| R3 | DATASET | 1:N | DATASET_IMAGE | Satu dataset berisi banyak gambar |
| R4 | IMAGE | N:M | DATASET | Satu gambar bisa ada di banyak dataset |

---

## 4. ARSITEKTUR SISTEM {#arsitektur}

### A. Arsitektur 3-Tier

```
┌─────────────────────────────────────────────┐
│         PRESENTATION TIER (Frontend)        │
├─────────────────────────────────────────────┤
│  • HTML Templates (Jinja2)                  │
│  • CSS (Premium Dark Mode)                  │
│  • JavaScript (Drag & Drop, Charts)         │
│  • Chart.js (Visualizations)                │
└──────────────────┬──────────────────────────┘
                   │ HTTP Requests
                   │ (GET/POST)
                   ▼
┌─────────────────────────────────────────────┐
│        APPLICATION TIER (Backend)           │
├─────────────────────────────────────────────┤
│  • Flask Framework                          │
│  • Routes & Endpoints:                      │
│    - / (index)                              │
│    - /compress                              │
│    - /decompress                            │
│    - /compress_dataset                      │
│    - /export_csv                            │
│  • Business Logic:                          │
│    - huffman.py (HuffmanCoding class)       │
│    - calculate_dataset_statistics()         │
│  • File Processing:                         │
│    - Image upload handling                  │
│    - File validation                        │
│    - Secure filename                        │
└──────────────────┬──────────────────────────┘
                   │ File I/O
                   │ OpenCV, NumPy
                   ▼
┌─────────────────────────────────────────────┐
│          DATA TIER (Storage)                │
├─────────────────────────────────────────────┤
│  • File System:                             │
│    - static/uploads/     (uploaded images)  │
│    - static/compressed/  (compressed files) │
│    - static/decompressed/ (decoded images)  │
│  • File Types:                              │
│    - .bin  (compressed bitstream)           │
│    - .json (Huffman codes)                  │
│    - .txt  (image dimensions)               │
│    - .png  (grayscale images)               │
│    - .csv  (dataset results)                │
└─────────────────────────────────────────────┘
```

### B. Arsitektur MVC (Model-View-Controller)

```
┌──────────────┐
│     USER     │
└──────┬───────┘
       │ Interacts
       ▼
┌──────────────────────────────────┐
│          VIEW (Templates)        │
├──────────────────────────────────┤
│ • index.html                     │
│ • result.html                    │
│ • dataset_result.html            │
│                                  │
│ Components:                      │
│ - Upload boxes                   │
│ - Forms                          │
│ - Tables                         │
│ - Charts                         │
│ - Statistics cards               │
└──────────┬───────────────────────┘
           │ Sends requests
           ▼
┌──────────────────────────────────┐
│      CONTROLLER (Flask Routes)   │
├──────────────────────────────────┤
│ app.py:                          │
│ • @app.route('/')                │
│ • @app.route('/compress')        │
│ • @app.route('/decompress')      │
│ • @app.route('/compress_dataset')│
│ • @app.route('/export_csv')      │
│                                  │
│ Functions:                       │
│ - compress_single()              │
│ - decompress()                   │
│ - compress_dataset()             │
│ - export_csv()                   │
└──────────┬───────────────────────┘
           │ Uses
           ▼
┌──────────────────────────────────┐
│        MODEL (Business Logic)    │
├──────────────────────────────────┤
│ huffman.py:                      │
│ • HuffmanNode class              │
│ • HuffmanCoding class            │
│   - _build_frequency_table()     │
│   - _build_huffman_tree()        │
│   - _generate_codes()            │
│   - compress_image()             │
│   - decompress_image()           │
│   - _save_binary()               │
│ • calculate_dataset_statistics() │
│                                  │
│ Libraries:                       │
│ - cv2 (OpenCV)                   │
│ - numpy                          │
│ - heapq                          │
│ - json                           │
└──────────────────────────────────┘
```

### C. Component Diagram

```
┌────────────────────────────────────────────────────┐
│                   FLASK APP                        │
│                                                    │
│  ┌──────────────┐    ┌──────────────┐             │
│  │   Routes     │───►│   Templates  │             │
│  │  (app.py)    │    │   (Jinja2)   │             │
│  └──────┬───────┘    └──────────────┘             │
│         │                                          │
│         │ uses                                     │
│         ▼                                          │
│  ┌──────────────┐                                  │
│  │   Huffman    │                                  │
│  │   Module     │                                  │
│  │ (huffman.py) │                                  │
│  └──────┬───────┘                                  │
│         │                                          │
└─────────┼──────────────────────────────────────────┘
          │ uses
          │
    ┌─────┴──────┬──────────┬──────────┐
    │            │          │          │
    ▼            ▼          ▼          ▼
┌─────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│  OpenCV │ │ NumPy  │ │  JSON  │ │  heapq │
│  (cv2)  │ │        │ │        │ │        │
└─────────┘ └────────┘ └────────┘ └────────┘
```

### D. Deployment Diagram

```
┌──────────────────────────────────────────┐
│         Client Browser                    │
│  ┌────────────────────────────────────┐  │
│  │  HTML + CSS + JavaScript           │  │
│  │  Chart.js                          │  │
│  └────────────────────────────────────┘  │
└──────────────┬───────────────────────────┘
               │ HTTP/HTTPS
               │ (Port 5000)
               ▼
┌──────────────────────────────────────────┐
│         Web Server (Flask Dev Server)    │
│  ┌────────────────────────────────────┐  │
│  │  Flask Application                 │  │
│  │  • WSGI Server                     │  │
│  │  • Python 3.x Runtime              │  │
│  └────────────────────────────────────┘  │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│         File System Storage              │
│  • /static/uploads/                      │
│  • /static/compressed/                   │
│  • /static/decompressed/                 │
│  • /static/css/                          │
│  • /static/js/                           │
│  • /templates/                           │
│  • /docs/                                │
└──────────────────────────────────────────┘
```

---

## 5. ALUR KERJA SISTEM

### Sequence Diagram: Single Image Compression

```
User         Browser      Flask      Huffman      FileSystem
 │             │            │           │             │
 │─Upload──────►            │           │             │
 │             │──POST────► │           │             │
 │             │  /compress │           │             │
 │             │            │           │             │
 │             │            │──validate─►             │
 │             │            │           │             │
 │             │            │──save────────────────►  │
 │             │            │           │             │
 │             │            │──compress►│             │
 │             │            │           │             │
 │             │            │           │─read────────►
 │             │            │           │             │
 │             │            │           │─grayscale───►
 │             │            │           │             │
 │             │            │           │─huffman─────►
 │             │            │           │             │
 │             │            │           │─save files──►
 │             │            │           │  .bin       │
 │             │            │           │  .json      │
 │             │            │           │  .txt       │
 │             │            │           │             │
 │             │            │◄──stats───│             │
 │             │            │           │             │
 │             │◄─render────│           │             │
 │             │  result.html           │             │
 │             │            │           │             │
 │◄─Display────│            │           │             │
 │  Results    │            │           │             │
```

---

## KESIMPULAN DIAGRAM

### Ringkasan:
1. **Flowchart** menunjukkan alur proses detail untuk kompresi, dekompresi, dan dataset
2. **DFD** menjelaskan aliran data antar proses dalam sistem
3. **ERD** memodelkan entitas dan relasi (meskipun tanpa database)
4. **Arsitektur** menggambarkan struktur 3-tier dan MVC sistem

### Karakteristik Sistem:
- **Stateless**: Tidak menyimpan session/state user
- **File-based**: Semua data disimpan di file system
- **Synchronous**: Proses kompresi blocking (tidak async)
- **Monolithic**: Satu aplikasi Flask yang handle semua

---

**Prepared by:** Pengolahan Citra Digital Lab
**Version:** 1.0
