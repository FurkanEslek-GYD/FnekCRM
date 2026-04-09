import streamlit as st
from supabase import create_client
import pandas as pd

# --- ANALİTİK AYARLAR ---
URL = https://kzeklqalcuvgilrhomvs.supabase.co 
KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0
# -----------------------

# Sistem Bağlantısı
supabase = create_client(URL, KEY)

# Profesyonel Arayüz Ayarları
st.set_page_config(page_title="FnekCRM", layout="wide")
st.markdown("<h1 style='text-align: center; color: black;'>⬛ FnekCRM | Analitik Gayrimenkul Yönetimi</h1>", unsafe_allow_html=True)

# Sol Panel: Veri Girişi
with st.sidebar:
    st.header("🏢 Yeni Portföy Ekle")
    with st.form("ekleme_formu", clear_on_submit=True):
        ad = st.text_input("Mülk Başlığı (Örn: Güzelbahçe Villası)")
        bolge = st.selectbox("Bölge", ["Güzelbahçe", "Urla", "Buca", "Karşıyaka", "Çeşme"])
        m2 = st.number_input("Metrekare (m²)", min_value=1.0)
        fiyat = st.number_input("Fiyat (TL)", min_value=1000.0)
        
        if st.form_submit_button("Sisteme Kaydet ve Analiz Et"):
            birim = fiyat / m2
            data = {"mulk_adi": ad, "bolge": bolge, "m2": m2, "fiyat": fiyat, "birim_fiyat": birim}
            supabase.table("portfoy").insert(data).execute()
            st.success("Veri buluta işlendi!")

# Ana Ekran: Analitik Raporlama
st.subheader("📊 Portföy Analiz Paneli")
res = supabase.table("portfoy").select("*").execute()
df = pd.DataFrame(res.data)

if not df.empty:
    # Üst Gösterge Kartları
    c1, c2, c3 = st.columns(3)
    avg_price = df['birim_fiyat'].mean()
    c1.metric("Ortalama m² Fiyatı", f"{avg_price:,.0f} TL")
    c2.metric("En Değerli Bölge", df.groupby('bolge')['birim_fiyat'].mean().idxmax())
    c3.metric("Toplam Kayıt", len(df))

    # Veri Tablosu
    st.write("### Mevcut İlanlar")
    st.dataframe(df.sort_values("eklenme_tarihi", ascending=False), use_container_width=True)
else:
    st.info("Henüz portföy girişi yapılmadı. Sol taraftan ilk veriyi girerek başlayabilirsiniz.")