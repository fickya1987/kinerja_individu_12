import streamlit as st
import pandas as pd
import plotly.graph_objs as go

uploaded_file = st.file_uploader("Upload file kinerja_file.csv", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Nama-nama kolom pada file Anda:", df.columns.tolist())
    
    # --- Mapping otomatis ---
    kolom_kategori = [col for col in df.columns if "kategori" in col.lower()][0]
    kolom_group = [col for col in df.columns if "group" in col.lower()][0]
    
    df.rename(columns={kolom_kategori: 'Kategori', kolom_group: 'Group'}, inplace=True)
    df['Kategori'] = df['Kategori'].astype(str).str.strip().str.title()
    
    kategori_order = ["Cukup", "Baik", "Sangat Baik"]
    groups = df['Group'].unique()

    def plot_group_kategori(df, group_name):
        sub = df[df['Group'] == group_name]
        kategori_counts = sub['Kategori'].value_counts().reindex(kategori_order, fill_value=0)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=kategori_order,
            y=kategori_counts.values,
            mode='lines+markers',
            line=dict(shape='spline', width=6, color="#2582E2"),
            marker=dict(size=24, color="#26C485", line=dict(color="#2582E2", width=2)),
            fill='tozeroy',
            name=group_name
        ))
        fig.update_layout(
            title=f"Distribusi Kategori Performa - {group_name}",
            xaxis_title="Kategori Performa",
            yaxis_title="Jumlah Pegawai",
            xaxis=dict(tickvals=kategori_order, tickfont=dict(size=20)),
            yaxis=dict(tickfont=dict(size=20)),
            font=dict(size=18, family="Arial"),
            plot_bgcolor="#f5f6fa",
            paper_bgcolor="#f5f6fa",
            margin=dict(l=40, r=40, t=60, b=40),
            height=440,
            showlegend=False,
        )
        return fig

    st.title("Distribusi Normal Kategori Performa Pegawai SDM Pelindo")
    for group in groups:
        st.plotly_chart(plot_group_kategori(df, group), use_container_width=True)
    st.subheader("Rekap Jumlah Pegawai per Kategori")
    st.dataframe(df.groupby(['Group', 'Kategori']).size().unstack(fill_value=0)[kategori_order])
else:
    st.info("Silakan upload file kinerja_file.csv untuk memulai visualisasi.")
