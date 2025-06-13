
# 🧠 Mood Tracker  
Capstone Project – CC25-CR386

**Mood Tracker** adalah aplikasi berbasis web yang dapat mengklasifikasikan suasana hati pengguna dari input teks berbahasa Indonesia menggunakan algoritma *Logistic Regression*. Proyek ini dikembangkan sebagai bagian dari Capstone Project pada program DBS Foundation Coding Camp 2025.

---

## 🚀 Fitur

- Input teks bebas berbahasa Indonesia
- Klasifikasi mood otomatis (joy, sadness, anger, fear, love, neutral)
- Emoji dan motivasi sesuai hasil prediksi
- Penyimpanan histori prediksi ke CSV
- Kalender mood interaktif
- Grafik tren mingguan dan statistik total
- Visualisasi interaktif dengan Plotly dan Seaborn

---

## 📁 Struktur Proyek

```
klasifikasimood/
├── app.py
├── best_logistic_regression_model.pkl
├── history.csv
├── requirements.txt
└── README.md
```

---

## 🛠️ Cara Menjalankan Aplikasi

1. **Clone repositori:**

```bash
git clone https://github.com/Gibskuyyyy/KlasifikasiMood.git
cd KlasifikasiMood
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Jalankan aplikasi Streamlit:**

```bash
streamlit run app.py
```

4. **Akses aplikasi melalui browser:**

```
http://localhost:8501
```

---

## 📦 Dataset

Dataset yang digunakan berasal dari opini publik berbahasa Indonesia dan dapat diakses melalui:

🔗 [Emotion Dataset from Indonesian Public Opinion](https://github.com/Ricco48/Emotion-Dataset-from-Indonesian-Public-Opinion)

Dataset ini telah diproses ulang melalui tahap *cleaning*, *stemming*, dan *stopword removal* menggunakan library Sastrawi.

---

## 📡 Deployment

Aplikasi ini telah dideploy dan dapat diakses secara publik melalui:

🔗 https://klasifikasimood.streamlit.app/

---

## 🧪 Teknologi yang Digunakan

- **Machine Learning**: Logistic Regression (scikit-learn)
- **NLP**: Sastrawi (stemming & stopword), TF-IDF
- **Frontend & Backend**: Streamlit
- **Visualisasi**: Plotly, Seaborn
- **Dataset**: Opini publik Bahasa Indonesia

---

## 👨‍💻 Tim Pengembang

- Anissa Shanniyah Aprilia (ML) – Universitas Bengkulu  
- Gibran Malik Naabih Andito (ML) – Universitas Kristen Satya Wacana

---

## 📌 Catatan

File `history.csv` digunakan untuk menyimpan histori prediksi mood pengguna. File ini akan otomatis dibuat saat aplikasi pertama dijalankan.

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan edukasi dan tidak digunakan sebagai alat diagnosis klinis.
