import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns

st.set_page_config(page_title="Kurva Distribusi Normal Performa SDM", layout="wide")

st.title("Kurva Distribusi Normal Kategori Performa SDM Pelindo")

uploaded_file = st.file_uploader("Upload file KPI SDM (CSV)", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df.columns = [c.strip() for c in df.columns]
    st.write("Kolom pada data:", df.columns.tolist())

    # Mapping kategori ke skor numerik
    kategori_map = {'Cukup': 1, 'Baik': 2, 'Sangat Baik': 3}
    group_col = 'Group'  # Ganti sesuai nama kolom di file
    kategori_col = 'Kategori Performa'  # Ganti sesuai nama kolom di file

    if group_col in df.columns and kategori_col in df.columns:
        df['Skor_Performa'] = df[kategori_col].map(kategori_map)

        fig, ax = plt.subplots(figsize=(10, 6))

        colors = sns.color_palette("husl", n_colors=df[group_col].nunique())

        for idx, (group, subdf) in enumerate(df.groupby(group_col)):
            data = subdf['Skor_Performa'].dropna()
            if len(data) < 2:
                continue
            mu, std = norm.fit(data)
            # Plot histogram
            sns.histplot(data, bins=[0.5,1.5,2.5,3.5], stat='density', kde=False, color=colors[idx], 
                         alpha=0.2, label=f"{group} (hist)", ax=ax)
            # Plot PDF (normal curve)
            x = np.linspace(1, 3, 100)
            p = norm.pdf(x, mu, std)
            ax.plot(x, p, '-', label=f"{group} (Normal Fit)", linewidth=3, color=colors[idx])
            # Mark mean
            ax.axvline(mu, linestyle='--', color=colors[idx], alpha=0.7)
            ax.text(mu, max(p)*0.8, f"μ={mu:.2f}\nσ={std:.2f}", color=colors[idx], fontsize=11, ha='center')

        ax.set_xticks([1,2,3])
        ax.set_xticklabels(['Cukup','Baik','Sangat Baik'], fontsize=13)
        ax.set_xlabel("Kategori Performa", fontsize=14)
        ax.set_ylabel("Density", fontsize=14)
        ax.set_title("Kurva Distribusi Normal (Bell Curve) per Group", fontsize=18, fontweight='bold')
        ax.legend(fontsize=12)
        st.pyplot(fig)
    else:
        st.warning("Kolom 'Group' dan/atau 'Kategori Performa' tidak ditemukan.")
else:
    st.info("Silakan upload file CSV terlebih dahulu.")

