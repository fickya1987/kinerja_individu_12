import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Setting style for a visually appealing plot
sns.set(style="whitegrid", palette="pastel", font_scale=1.2)

st.set_page_config(page_title="Distribusi Normal KPI SDM Pelindo", layout="wide")

st.title("Kurva Distribusi Normal Kategori Performa SDM Pelindo")

# Load data
uploaded_file = st.file_uploader("Upload file KPI SDM (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    # Standardize column names
    df.columns = [c.strip() for c in df.columns]

    # Pilih kolom yang relevan
    # Misal: 'Group', 'Kategori Performa' (namanya sesuaikan dengan file Anda)
    # Tampilkan nama kolom untuk memastikan
    st.write("Kolom yang tersedia:", df.columns.tolist())

    # Mapping kategori ke urutan X-Axis
    kategori_order = ['Cukup', 'Baik', 'Sangat Baik']

    # Pastikan kolom sesuai, silakan ubah jika nama kolom berbeda!
    group_col = 'Group'  # Ganti jika nama di file berbeda
    kategori_col = 'Kategori Performa'  # Ganti jika nama di file berbeda

    if group_col in df.columns and kategori_col in df.columns:
        # Hitung jumlah pegawai per group per kategori
        group_counts = df.groupby([group_col, kategori_col]).size().reset_index(name='Jumlah Pegawai')

        # Pivot agar mudah plot per group
        pivot_df = group_counts.pivot(index=kategori_col, columns=group_col, values='Jumlah Pegawai').fillna(0)
        pivot_df = pivot_df.reindex(kategori_order)

        st.subheader("Visualisasi Kurva Distribusi Normal per Group")

        fig, ax = plt.subplots(figsize=(10, 6))

        # Color palette
        colors = sns.color_palette("husl", len(pivot_df.columns))

        for i, group in enumerate(pivot_df.columns):
            # Interpolasi supaya kurva lebih smooth
            y = pivot_df[group].values
            x = range(len(kategori_order))
            # Smoothing, simple approach (bisa diganti dengan spline untuk lebih halus)
            sns.lineplot(x=x, y=y, marker='o', label=group, ax=ax, color=colors[i], linewidth=3)
            for (xi, yi) in zip(x, y):
                ax.text(xi, yi+0.5, int(yi), ha='center', va='bottom', fontsize=11, color=colors[i])

        ax.set_xticks(range(len(kategori_order)))
        ax.set_xticklabels(kategori_order, fontsize=14)
        ax.set_ylabel("Jumlah Pegawai", fontsize=13)
        ax.set_xlabel("Kategori Performa", fontsize=13)
        ax.set_title("Kurva Distribusi Normal Pegawai per Group", fontsize=17, fontweight='bold')
        ax.legend(title="Group", fontsize=12)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.warning("Nama kolom tidak ditemukan. Pastikan file memiliki kolom 'Group' dan 'Kategori Performa'.")
else:
    st.info("Silakan upload file CSV untuk memulai.")
