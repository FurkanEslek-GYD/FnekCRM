import streamlit as st
from supabase import create_client
import pandas as pd

# --- ANALİTİK AYARLAR ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"

try:
    supabase = create_client(URL, KEY)
except:
    st.error("Veritabanı bağlantısı kurulamadı.")

# İzmir Veri Seti
izmir_full_data = {
    "Aliağa": ["Atatürk", "Yeni Mahalle", "Siteler", "Bahçelievler"],
    "Balçova": ["Korutürk", "Eğitim", "Onur", "Fevzi Çakmak"],
    "Bayraklı": ["Mansuroğlu", "Manavkuyu", "Adalet", "Fuat Edip Baksi"],
    "Bornova": ["Kazımdirik", "Özkanlar", "Manavkuyu", "Mevlana", "Erzene"],
    "Buca": ["Adatepe", "Safir (Yıldız)", "Yiğitler", "Şirinyer", "Dumlupınar"],
    "Çeşme": ["Alaçatı", "Ilıca", "Musalla", "Boyalık", "Dalyan", "Reisdere"],
    "Çiğli": ["Ataşehir", "Yeni Mahalle", "Balatçık", "Sasalı"],
    "Gaziemir": ["Atıfbey", "Yeşil Mahalle", "Irmak", "Sarnıç"],
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Kahramandere"],
    "Karşıyaka": ["Mavişehir", "Bostanlı", "Atakent", "Bahçelievler", "Aksoy"],
    "Konak": ["Alsancak", "Göztepe", "Güzelyalı", "Hatay", "Kültür"],
    "Narlıdere": ["Yenikale", "Sahilevleri", "Huzur", "Limanreis"],
    "Seferihisar": ["Sığacık", "Akarca", "Camikebir", "Hıdırlık"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak", "Güvendik"]
} # Diğer ilçeler de eklenebilir

st.set_page_config(page_title="FnekCRM PRO", layout="wide")

# Dark Executive Tasarım
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px; font-weight: 800; }
    .stMetric { background-color: #1a1c23; padding: 20px; border-radius: 12px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #ffffff; font-family: 'Inter', sans-serif; }
    .stButton>button { background-color: #ffffff; color: #000000; font-weight: bold; width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⬛ FnekCRM | Executive Dashboard")

# --- SOL PANEL: GELİŞMİŞ VERİ GİRİŞİ ---
with st.sidebar:
    st.header("🏢 Detaylı Portföy Kaydı")
    
    ilce = st.selectbox("İlçe", list(izmir_full_data.keys()), key="ilce_sb")
    mahalle = st.selectbox("Mahalle", izmir_full_data[ilce], key="mahalle_sb")

    with st.form("pro_kayit_formu", clear_on_submit=True):
        baslik = st.text_input("İlan Başlığı")
        
        col_1, col_2 = st.columns(2)
        with col_1:
            islem = st.selectbox("İşlem Tipi", ["Satılık", "Kiralık", "Devren Satılık", "Devren Kiralık"])
        with col_2:
            mulk = st.selectbox("Mülk Tipi", ["Konut", "Ticari", "Arsa", "Turistik"])
            
        m2 = st.number_input("Metrekare (Net)", min_value=1)
        fiyat = st.number_input("Toplam Fiyat (TL)", min_value=1000, step=10000)
        notlar = st.text_area("Analitik Notlar & Portföy Stratejisi")
        
        if st.form_submit_button("Sisteme İşle ve Analiz Et"):
            if baslik:
                birim = fiyat / m2
                data = {
                    "mulk_adi": baslik, "bolge": ilce, "mahalle": mahalle, 
                    "m2": m2, "fiyat": fiyat, "birim_fiyat": birim, 
                    "notlar": notlar, "islem_tipi": islem, "mulk_tipi": mulk
                }
                supabase.table("portfoy").insert(data).execute()
                st.success("Veri buluta başarıyla işlendi.")
                st.rerun()

# --- ANA EKRAN: ANALİTİK PANEL ---
try:
    res = supabase.table("portfoy").select("*").order("eklenme_tarihi", desc=True).execute()
    df = pd.DataFrame(res.data)
except:
    df = pd.DataFrame()

if not df.empty:
    # Filtreleme Seçenekleri
    st.write("### 📊 Analitik Özet")
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Hacim", f"{df['fiyat'].sum():,.0f} TL")
    c2.metric("Portföy Sayısı", len(df))
    c3.metric("Bölge Lideri", df['bolge'].mode()[0])

    st.divider()

    # Sahibinden Tarzı Detaylı İnceleme
    st.subheader("🔍 Portföy Detay Analizi")
    secili = st.selectbox("İncelemek istediğiniz portföyü seçin:", df['mulk_adi'].tolist())
    d = df[df['mulk_adi'] == secili].iloc[0]

    with st.container():
        col_sol, col_sag = st.columns([1, 2])
        with col_sol:
            st.markdown(f"### {d['mulk_adi']}")
            st.markdown(f"**{d['islem_tipi']} | {d['mulk_tipi']}**")
            st.info(f"📍 {d['bolge']} / {d['mahalle']}")
            st.write(f"📏 **Alan:** {int(d['m2'])} m²")
            st.write(f"📊 **Birim:** {d['birim_fiyat']:,.0f} TL")
            st.error(f"💰 **FİYAT: {d['fiyat']:,.0f} TL**")
        
        with col_sag:
            st.markdown("#### Danışman Notları")
            st.write(d['notlar'] if d['notlar'] else "Not eklenmemiş.")
            # Kıyaslama Grafiği
            st.bar_chart(df[df['islem_tipi'] == d['islem_tipi']].set_index('mulk_adi')['birim_fiyat'])

    st.divider()
    with st.expander("📂 Tüm Portföy Verisi"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("Henüz veri bulunmuyor. Sol panelden giriş yapabilirsiniz.")
