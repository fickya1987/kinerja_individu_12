import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, skew
import seaborn as sns

st.set_page_config(page_title="Kurva Distribusi Normal Per Group", layout="wide")
st.title("Kurva Distribusi Normal & Volume Pegawai per Group - KPI SDM Pelindo")

uploaded_file = st.file_uploader("Upload file KPI SDM (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = [c.strip() for c in df.columns]
    st.write("Kolom pada data:", df.columns.tolist())

    kategori_map = {'Cukup': 1, 'Baik': 2, 'Sangat Baik': 3}
    group_col = 'Group'         # Edit sesuai nama kolom file Anda
    kategori_col = 'Kategori Performa'
    nama_col = 'Nama'
    posisi_col = 'Posisi'

    if all(col in df.columns for col in [group_col, kategori_col, nama_col, posisi_col]):
        df['Skor_Performa'] = df[kategori_col].map(kategori_map)

        for group, subdf in df.groupby(group_col):
            st.header(f"Group: {group}")

            # Tampilkan nama & posisi
            st.write("**Daftar Nama & Posisi:**")
            st.dataframe(subdf[[nama_col, posisi_col, kategori_col]], hide_index=True, use_container_width=True)

            data = subdf['Skor_Performa'].dropna()
            if len(data) < 2:
                st.info("Data pegawai kurang untuk analisis distribusi normal.")
                continue

            # Analisis skewness
            mean = data.mean()
            median = data.median()
            modus = data.mode().values[0] if not data.mode().empty else None
            skewness = skew(data)
            if skewness < -0.5:
                status = "Skewed Left (Negatif)"
            elif skewness > 0.5:
                status = "Skewed Right (Positif)"
            else:
                status = "Normal (Simetris)"

            # Histogram volume & normal curve (scaled to match bar heights)
            counts, bins = np.histogram(data, bins=[0.5,1.5,2.5,3.5])
            bin_centers = [1, 2, 3]

            fig, ax = plt.subplots(figsize=(7, 4))
            ax.bar(bin_centers, counts, width=0.6, alpha=0.3, color="royalblue", edgecolor="black", label="Volume Pegawai")

            # Fit distribusi normal dan skala ke volume
            mu, std = norm.fit(data)
            x = np.linspace(1, 3, 100)
            pdf = norm.pdf(x, mu, std)
            pdf_scaled = pdf * len(data) * (bins[1] - bins[0])
            ax.plot(x, pdf_scaled, 'r-', linewidth=2, label=f'Normal Fit\nμ={mu:.2f}, σ={std:.2f}')

            ax.axvline(mean, color='blue', linestyle='--', label=f'Mean={mean:.2f}')
            ax.axvline(median, color='orange', linestyle=':', label=f'Median={median:.2f}')
            if modus:
                ax.axvline(modus, color='green', linestyle='-.', label=f'Mode={modus:.2f}')

            ax.set_xticks([1,2,3])
            ax.set_xticklabels(['Cukup','Baik','Sangat Baik'], fontsize=12)
            ax.set_xlabel("Kategori Performa")
            ax.set_ylabel("Volume (Jumlah Pegawai)")
            ax.set_title(f"Kurva Distribusi Normal & Volume Pegawai - {group}")
            ax.legend()
            st.pyplot(fig)

            # Analisis Skewness
            st.write(f"""
                **Analisis Distribusi (Skewness):**
                - **Mean**: {mean:.2f}
                - **Median**: {median:.2f}
                - **Mode**: {modus:.2f if modus else "-"}
                - **Skewness**: {skewness:.2f} → **{status}**
            """)
    else:
        st.warning("Pastikan file memiliki kolom 'Group', 'Kategori Performa', 'Nama', dan 'Posisi'.")
else:
    st.info("Silakan upload file CSV terlebih dahulu.")
