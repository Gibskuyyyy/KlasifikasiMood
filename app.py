import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from io import BytesIO
import os
import calendar

# Load model
model = joblib.load('best_logistic_regression_model.pkl')

# Set halaman
st.set_page_config(page_title="Mood Tracker", page_icon="🧠", layout="wide")

# Mapping mood
emoji_dict = {
    'joy': '😊', 'sadness': '😢', 'anger': '😡',
    'fear': '😱', 'love': '❤️', 'neutral': '😐'
}

motivasi_dict = {
    'joy': "Mood kamu sedang senang, terus pertahankan ya!",
    'sadness': "Sedih itu wajar, jangan lupa istirahat dan self-care ya!",
    'anger': "Tenangkan diri dulu ya, semuanya akan baik-baik saja.",
    'fear': "Tidak apa-apa takut, tapi kamu lebih kuat dari yang kamu kira.",
    'love': "Cinta ada di sekelilingmu, sebarkan energi positif!",
    'neutral': "Mood kamu netral, tetap semangat ya!"
}

mood_score_map = {
    'joy': 0.9, 'love': 0.8, 'neutral': 0.0,
    'sadness': -0.6, 'fear': -0.7, 'anger': -0.8
}

label_indo = {
    'joy': 'Senang', 'sadness': 'Sedih', 'anger': 'Marah',
    'fear': 'Takut', 'love': 'Cinta', 'neutral': 'Netral'
}

# ===== LOGIN DENGAN SESSION STATE =====
if 'username' not in st.session_state:
    with st.container():
        st.markdown("""
            <div style='background-color:#f0f4ff;padding:2rem 1rem;border-radius:12px;text-align:center'>
                <h2 style='color:#6C63FF'>👤 Selamat Datang di Mood Tracker</h2>
                <p style='color:gray'>Masukkan nama atau ID kamu untuk memulai</p>
            </div>
        """, unsafe_allow_html=True)

        username_input = st.text_input("🆔 Nama/ID Kamu", placeholder="contoh: gibran", key="login_username")
        if st.button("🔓 Masuk") and username_input:
            st.session_state.username = username_input.strip().lower()
            st.rerun()
    st.stop()  # Jangan lanjutkan app sebelum login

# Setelah login
username = st.session_state.username

username = username.strip().lower()
history_file = f"history_{username}.csv"

# Inisialisasi file jika belum ada
if not os.path.exists(history_file):
    df_empty = pd.DataFrame(columns=["Waktu", "Teks", "Mood", "Emoji", "Score"])
    df_empty.to_csv(history_file, index=False)

# Header
st.markdown("<h1 style='text-align: center; color: #6C63FF;'>🧠 Mood Tracker</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Prediksi & Visualisasi Mood Harian</h4>", unsafe_allow_html=True)
st.markdown("---")

# Input
user_input = st.text_area("📝 Masukkan teks di sini:", placeholder="Contoh: Hari ini aku merasa bahagia...")

# Prediksi
if st.button("🔍 Prediksi Mood"):
    if user_input.strip():
        prediction = model.predict([user_input])[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        emoji = emoji_dict.get(prediction, '🤔')
        score = mood_score_map.get(prediction.lower(), 0.0)
        mood_indo = label_indo.get(prediction, prediction)

        new_entry = pd.DataFrame({
            "Waktu": [timestamp], "Teks": [user_input],
            "Mood": [prediction], "Emoji": [emoji], "Score": [score]
        })

        df_existing = pd.read_csv(history_file)
        df_updated = pd.concat([df_existing, new_entry], ignore_index=True)
        df_updated.to_csv(history_file, index=False)

        st.markdown("### 🎯 Hasil Prediksi:")
        st.markdown(f"<h1 style='text-align: center;'>{emoji}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{mood_indo}</h2>", unsafe_allow_html=True)
        st.info(motivasi_dict.get(prediction, "Tetap semangat ya!"))
    else:
        st.warning("Silakan masukkan teks terlebih dahulu.")

    st.markdown(f"✅ Sedang login sebagai: **{username.title()}**")
    if st.button("🔄 Ganti Pengguna"):
        del st.session_state.username
        st.rerun()


# Tabs
try:
    df = pd.read_csv(history_file)
    if df.empty:
        st.info("📭 Belum ada data histori. Silakan mulai prediksi terlebih dahulu.")
    else:
        df['Tanggal'] = pd.to_datetime(df['Waktu']).dt.date
        df['Minggu'] = pd.to_datetime(df['Tanggal']).dt.to_period('W').apply(lambda r: r.start_time)

        tab1, tab2, tab3 = st.tabs(["📜 Riwayat", "🗓️ Kalender", "📈 Grafik"])

        with tab1:
            st.markdown("### 📜 Riwayat Mood")
            min_date, max_date = df['Tanggal'].min(), df['Tanggal'].max()
            start, end = st.date_input("Filter tanggal:", [min_date, max_date])
            df_filtered = df[(df['Tanggal'] >= start) & (df['Tanggal'] <= end)]

            search_term = st.text_input("🔍 Cari kata dalam teks:")
            if search_term:
                df_filtered = df_filtered[df_filtered['Teks'].str.contains(search_term, case=False, na=False)]

            st.dataframe(df_filtered[::-1][['Waktu', 'Teks', 'Mood', 'Emoji', 'Score']])
            st.download_button(
                "📥 Download Riwayat sebagai CSV",
                data=df.to_csv(index=False),
                file_name="riwayat_mood.csv",
                mime="text/csv"
            )
            # Tombol reset histori
            if os.path.exists(history_file):
                if st.button("🗑️ Reset histori saya"):
                    os.remove(history_file)
                    st.success("Histori berhasil direset.")
                    st.stop()

        with tab2:
            st.markdown("### 🗓️ Kalender Mood Interaktif")
            st.caption("📌 Klik tanggal untuk lihat detail. Warna mewakili intensitas mood. Hover tampilkan info.")

            # Pastikan kolom 'Tanggal' bertipe datetime
            df['Tanggal'] = pd.to_datetime(df['Waktu']).dt.date
            df['Tanggal'] = pd.to_datetime(df['Tanggal'])

            # Dropdown bulan dan tahun
            available_years = sorted(df['Tanggal'].dt.year.unique(), reverse=True)
            selected_year = st.selectbox("📆 Pilih tahun:", available_years)
            selected_month = st.selectbox("📅 Pilih bulan:", list(range(1, 13)), format_func=lambda x: calendar.month_name[x])

            df_bulan = df[(df['Tanggal'].dt.year == selected_year) & (df['Tanggal'].dt.month == selected_month)]

            if df_bulan.empty:
                st.info("Tidak ada data untuk bulan ini.")
            else:
                df_avg = df_bulan.groupby('Tanggal').agg({
                    'Score': 'mean',
                    'Emoji': lambda x: x.mode().iloc[0] if not x.mode().empty else ''
                }).reset_index()

                df_avg['Hari'] = df_avg['Tanggal'].dt.day
                df_avg['Tooltip'] = df_avg.apply(
                    lambda row: f"{row['Tanggal'].strftime('%d %B %Y')}<br>Score: {row['Score']:.2f}<br>Emoji: {row['Emoji']}", axis=1)

                # Buat matriks kalender
                calendar_matrix = [[None for _ in range(7)] for _ in range(6)]
                tooltips_matrix = [[None for _ in range(7)] for _ in range(6)]
                emoji_matrix = [[None for _ in range(7)] for _ in range(6)]

                first_day = datetime(selected_year, selected_month, 1)
                start_weekday = first_day.weekday()
                total_days = calendar.monthrange(selected_year, selected_month)[1]

                row, col = 0, start_weekday
                for day in range(1, total_days + 1):
                    date = datetime(selected_year, selected_month, day).date()
                    match = df_avg[df_avg['Tanggal'].dt.date == date]
                    score = match['Score'].values[0] if not match.empty else 0
                    tooltip = match['Tooltip'].values[0] if not match.empty else ""
                    emoji = match['Emoji'].values[0] if not match.empty else ""

                    calendar_matrix[row][col] = score
                    tooltips_matrix[row][col] = tooltip
                    emoji_matrix[row][col] = f"<b>{day}</b><br>{emoji}"

                    col += 1
                    if col > 6:
                        col = 0
                        row += 1

                # Warna berdasarkan skor
                def get_color(score):
                    if score >= 0.7: return "#16a34a"
                    elif score >= 0.4: return "#60a5fa"
                    elif score >= -0.1: return "#facc15"
                    elif score >= -0.5: return "#f87171"
                    else: return "#991b1b"

                fill_colors = [[get_color(score) if score is not None else "white" for score in row] for row in calendar_matrix]

                fig = go.Figure(data=go.Table(
                    header=dict(values=["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"],
                                fill_color="#E2E8F0", align="center", font=dict(size=14, color="black")),
                    cells=dict(
                        values=list(zip(*emoji_matrix)),
                        fill_color=list(zip(*fill_colors)),
                        align="center",
                        height=55,
                        font=dict(size=16)
                    )))


                fig.update_layout(
                    margin=dict(t=20, l=0, r=0, b=0),
                    title=dict(
                        text=f"Kalender Mood - {calendar.month_name[selected_month]} {selected_year}",
                        x=0.5, xanchor='center', font=dict(size=20)
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

                # Klik tanggal untuk lihat detail
                st.markdown("### 🔎 Detail Mood Harian")
                selected_day = st.selectbox("📅 Pilih tanggal:", sorted(df_bulan['Tanggal'].dt.day.unique()))
                tanggal_terpilih = datetime(selected_year, selected_month, selected_day).date()
                detail_df = df[df['Tanggal'].dt.date == tanggal_terpilih]

                if detail_df.empty:
                    st.info("Tidak ada entri pada tanggal tersebut.")
                else:
                    st.dataframe(detail_df[['Waktu', 'Teks', 'Mood', 'Emoji', 'Score']])

        with tab3:
            st.markdown("### 📈 Grafik Mood Harian")
            st.caption("Tooltip interaktif & tren mingguan juga tersedia.")

            summary = df.groupby(['Tanggal', 'Mood']).size().reset_index(name="Jumlah")
            fig3 = px.line(summary, x='Tanggal', y='Jumlah', color='Mood', markers=True,
                           title="Jumlah Mood per Hari", hover_data=["Mood", "Jumlah", "Tanggal"])
            st.plotly_chart(fig3, use_container_width=True)

            st.markdown("### 📅 Tren Mingguan")
            weekly_summary = df.groupby(['Minggu', 'Mood']).size().reset_index(name='Jumlah')
            fig4 = px.line(weekly_summary, x='Minggu', y='Jumlah', color='Mood', markers=True,
                           title="Tren Mood Mingguan", hover_data=["Mood", "Jumlah"])
            st.plotly_chart(fig4, use_container_width=True)

            st.markdown("### 📊 Statistik Total Mood")
            total_stats = df['Mood'].value_counts().reset_index()
            total_stats.columns = ['Mood', 'Jumlah']
            total_stats['Persen'] = 100 * total_stats['Jumlah'] / total_stats['Jumlah'].sum()
            st.dataframe(total_stats)

except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca histori: {e}")
