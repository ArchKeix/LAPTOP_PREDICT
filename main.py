import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load("laptop_price_model.pkl")

st.set_page_config(page_title="Prediksi Harga Laptop", layout="centered")
st.title("💻 Prediksi Harga Laptop")
st.markdown("Masukkan spesifikasi laptop untuk memprediksi harganya:")

# Sidebar dengan kategori umum
with st.sidebar:
    st.header("📋 KETERANGAN ")
    st.markdown(
        """
    - Gunakan slider dan dropdown untuk mengisi spesifikasi laptop.
    - Pastikan semua kolom terisi dengan benar.
    - Pilih merek laptop, tipe, dan sistem operasi yang sesuai.
    - Tekan tombol **Prediksi Harga** untuk melihat hasil prediksi.
    """
    )

# ==== INPUT FORM ====
with st.form("form_laptop"):
    col1, col2 = st.columns(2)

    with col1:
        company = st.selectbox(
            "Merek Laptop (Company)",
            [
                "Lenovo",  # 244
                "Dell",  # 229
                "HP",  # 215
                "Asus",  # 130
                "Acer",  # 82
                "MSI",  # 44
                "Toshiba",  # 41
                "Apple",  # 19
                "Samsung",  # 7
                "Razer",  # 6
                "Vero",  # 4
                "Mediacom",  # 4
                "Microsoft",  # 4
                "Google",  # 3
                "LG",  # 3
                "Chuwi",  # 3
                "Xiaomi",  # 2
                "Huawei",  # 1
                "Fujitsu",  # 1
            ],
        )
        product = st.text_input("Nama Produk (Product)", value="MacBook Pro")
        typename = st.selectbox(
            "Tipe Laptop (TypeName)",
            [
                "Notebook",
                "Gaming",
                "Ultrabook",
                "2 in 1 Convertible",
                "Netbook",
                "Workstation",
            ],
        )
        os = st.selectbox(
            "Sistem Operasi (OpSys)",
            [
                "Windows 10",
                "No OS",
                "Linux",
                "Windows 7",
                "Chrome OS",
                "macOS",
                "Mac OS X",
                "Windows 10 S",
                "Android",
            ],
        )
        resolution_type = st.selectbox(
            "Tipe Resolusi", ["Full HD", "Retina", "HD", "4K", "Touchscreen", "Other"]
        )

        ram = st.slider("RAM (GB)", 2, 64, 8)
        ssd = st.slider("SSD (GB)", 0, 2048, 256, step=128)
        hdd = st.slider("HDD (GB)", 0, 2000, 0, step=128)

    with col2:
        inches = st.slider("Ukuran Layar (Inches)", 10.0, 18.0, 13.3, step=0.1)
        weight = st.number_input("Berat (Kg)", value=1.3, step=0.1)
        total_mem = ssd + hdd

        cpu_brand = st.selectbox("Brand CPU", ["Intel", "AMD", "Others"])
        cpu_type = st.selectbox(
            "Tipe CPU", ["i3", "i5", "i7", "i9", "Ryzen 3", "Ryzen 5", "Ryzen 7"]
        )
        gpu_brand = st.selectbox("GPU Brand", ["Intel", "Nvidia", "AMD"])

        ips = st.checkbox("IPS Panel")
        touch = st.checkbox("Touchscreen")

        width = st.number_input("Lebar Layar (pixel)", value=1920)
        height = st.number_input("Tinggi Layar (pixel)", value=1080)
        aspect_ratio = round(width / height, 2)

    submitted = st.form_submit_button("🎯 Prediksi Harga")

# ==== PREDIKSI ====
if submitted:
    input_df = pd.DataFrame(
        [
            {
                "Company": company,
                "Product": product,
                "TypeName": typename,
                "Inches": inches,
                "Ram": ram,
                "OpSys": os,
                "Weight": weight,
                "SSD_GB": ssd,
                "HDD_GB": hdd,
                "Total_Memory_GB": total_mem,
                "GPU_Brand": gpu_brand,
                "CPU_Brand": cpu_brand,
                "CPU_Type": cpu_type,
                "Width": width,
                "Height": height,
                "IPS Panel": int(ips),
                "Touchscreen": int(touch),
                "Resolution_Type": resolution_type,
                "Aspect_Ratio": aspect_ratio,
            }
        ]
    )

    # Prediksi
    try:
        pred = model.predict(input_df)[0]
        st.success(f"💰 Perkiraan Harga Laptop: {pred:,.0f} €")
    except Exception as e:
        st.error(f"Gagal memprediksi: {e}")
