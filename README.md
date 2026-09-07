# Data Preparation & Pipeline Project — Automobile Dataset

Individual Assignment — AI Engineering Bootcamp (Data Engineering: Pipeline & Preparation)

## 1. Deskripsi Dataset
   Dataset berisi informasi mengenai berbagai karakteristik kendaraan, seperti merek kendaraan, tipe bahan bakar, jenis body, sistem penggerak, spesifikasi mesin, horsepower, harga, dan informasi transaksi.

## 2. Sumber Dataset
   File dataset yang digunakan terdiri dari:
   1. automobileEDA_dirty_training.csv — dataset utama yang digunakan sebagai input pipeline.
   2. automobileEDA.csv — dataset original yang digunakan sebagai referensi.
   3. automobile_processed.csv — dataset clean/processed yang digunakan sebagai referensi atau pembanding hasil.

## 3. Struktur folder project
  data-pipeline-assignment/
  ├── data/
  │   ├── raw/
  │   │   └── automobileEDA_dirty_training.csv
  │   └── processed/
  │       └── automobileEDA_processed.csv
  ├── src/
  │   └── pipeline.py
  ├── documentation/
  │   └── data-flow-diagram.png
  ├── README.md
  └── requirements.txt

## 4. Kondisi awal dataset
- **Jumlah data awal**: 205 baris, 30 kolom.

## 5. Permasalahan yang ditemukan
- **Kolom dengan missing values**: total 17
    stroke               4
    horsepower           3
    price                3
    num-of-doors         2
    make                 2
    transaction_date     2
    horsepower-binned    1
- **Baris duplikat**: 4 baris.
- **Kolom dengan tipe data belum sesuai**: transaction_date: bertipe string, padahal seharusnya bertipe datetime. Formatnya pun   tidak konsisten antar baris, misalnya 2025-01-01, 02/01/2025, 01-03-2025, dan 04-Jan-2025 muncul dalam kolom yang sama.
- **Penulisan kategori yang belum konsisten**: contoh
  - Kolom make
    `alfa-romero` - `ALFA-ROMERO`
    `Audi` - `audi`
    `dodge  ` spasi
  - kolom body-style 
    `sedan` - `SEDAN` - `Sedan`
  - kolom drive-wheels 
    `rwd` - `RWD`
  - kolom fuel-system 
    `mpfi` - `MPFI` - `Mpfi`
  - kolom transaction_date memiliki 4 format tanggal berbeda dan tidak konsisten
     `YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`, dan `DD-Mon-YYYY`.

## 5. Cleaning yang dilakukan beserta alasannya
**Jumlah data sebelum dan sesudah cleaning:**
SEBELUM CLEANING
Jumlah data (baris, kolom): (205, 30)
Total missing values      : 17
Jumlah baris duplikat     : 4

SESUDAH CLEANING
Jumlah data (baris, kolom): (201, 30)
Total missing values      : 3
Jumlah baris yang dihapus : 4

Kolom yang di cleaning (penulisan tidak konsisten diseragamkan pakai diseragamkan pakai .str.strip().str.lower() karena konsistensi data)
- make = diseragamkan dan diisi modus
- num-of-doors =	diisi modus
- body-style	= diseragamkan
- drive-wheels	= diseragamkan
- fuel-system = diseragamkan
- stroke = diisi median
- horsepower = diisi median
- price =	diisi median
- transaction_date = format campuran (2025-01-01, 02/01/2025, 04-Jan-2025, dll) → dikonversi jadi tipe datetime dan format di seragamkan dengan format DD/MM/YYY karna ini data datetime
- Menghapus Duplicate Records

**transaction_date missing tidak dihapus dan tidak diisi karna value tidak bisa ditebak karena ini tanggal transaksi**
**jadi sampai tahap ini masih ada 3 missing values 2 transaction date masih null dan horsepower-binned karena nilainya tidak bisa ditebak**

## 6. Data Transformation 
Pada tahap data transformation, dilakukan beberapa transformasi untuk mengubah data menjadi bentuk yang lebih terstruktur dan mudah digunakan untuk analisis.

a. Min-Max Scaling pada horsepower
  horsepower => horsepower_scaled = Min-Max Scaling rentang 0-1 
b. Frequency Encoding pada make
  make => make_freq = yang menunjukkan kemunculannya pada tiap tiap merk mobil
c. One-Hot Encoding kolom kategorikal
  body-style
  drive-wheels
  aspiration
  engine-type
  engine-location
  fuel-system

## 7. Contoh hasil sebelum dan sesudah transformasi
**Min-Max Scaling**
horsepower	horsepower_scaled
  111	          0.294393
  111	          0.294393
  154	          0.495327
  102	          0.252336
  115	          0.313084

**Frequency Encoding**  
make	        make_freq
alfa-romero	      3
alfa-romero	      3
alfa-romero	      3
audi	            7
audi	            7

**One-Hot Encoding**
Setiap kategori diubah menjadi kolom numerik terpisah dengan nilai: 
0 untuk data tidak termasuk dalam kategori
1 = data termasuk dalam kategori
- body-style
- drive-wheels
- aspiration
- engine-type
- engine-location
- fuel-system
## 8. Jumlah data sebelum dan sesudah diproses
- Jumlah data sebelum processing = 205 baris
- Jumlah data setelah cleaning = 201 baris
- Jumlah baris yang dihapus = 4 baris
- Jumlah kolom sebelum processing =	30 kolom
  Pada tahap transformation, jumlah kolom bertambah karena dilakukan penambahan kolom hasil Min-Max Scaling, Frequency Encoding, dan One-Hot Encoding.

## 9. Cara menginstal dependency
- Buat venv:
  `python -m venv venv`
- Aktifkan virtual environment:
  `venv\Scripts\activate`
- Install dependency:
  `pip install -r requirements.txt`

## 10. Cara menjalankan pipeline.py
- cd data-pipeline-assignment
- Jalankan pipeline: `python src/pipeline.py`

## 11. Penjelasan singkat mengenai alur ETL
a. Dataset dibaca dari data/raw/automobileEDA_dirty_training.csv menggunakan Pandas load_data()
b. Data diperiksa, dibersihkan, dan ditransformasikan melalui:
    - inspect_data()
    - clean_data()
    - transform_data()
c. Dataset hasil processing disimpan melalui:
    save_data() => data/processed/automobileEDA_processed.csv

## 12. Lokasi processed dataset
data/processed/automobileEDA_processed.csv
