import streamlit as st
from supabase import create_client
import pandas as pd

# --- ANALİTİK AYARLAR (Kendi anahtarlarınızı tırnak içine yazın) ---
import streamlit as st
from supabase import create_client
import pandas as pd

# --- ANALİTİK AYARLAR (Kendi anahtarlarınızı tırnak içine yazın) ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"
# -------------------------------------------------------------

supabase = create_client(URL, KEY)

# İzmir Veri Seti (Örnekleme - Tüm ilçeler eklenebilir)
izmir_data = {
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Atatürk", "Kahramandere"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak"],
    "Buca": ["Adatepe", "Safir", "Yiğitler", "Şirinyer", "Dumlupınar", "Yıldız"],
    "Çeşme": ["Alaçatı", "Ilıca", "Musalla", "Boyalık", "Dalyan"],
    "Karşıyaka": ["Mavişehir", "Bostanlı", "Atakent", "Bahçelievler", "Tersane"]
}

st.set_page_config(page_title="FnekCRM PRO", layout="wide")

# Dark Theme & Kurumsal Stil
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #ffffff; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #1f1f1f; color: white; border: 1px solid #333; }
    .stButton>button:hover { border-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("⬛ FnekCRM | Executive Dashboard")

# --- SOL PANEL: VERİ GİRİŞİ ---
with st.sidebar:
    st.header("🏢 Portföy Kayıt")
    with st.form("pro_form", clear_on_submit=True):
        baslik = st.text_input("İlan Başlığı")
        ilce = st.selectbox("İlçe", list(izmir_data.keys()))
        mahalle = st.selectbox("Mahalle", izmir_data[ilce])
        m2 = st.number_input("Metrekare (Net)", min_value=1)
        fiyat = st.number_input("İstenen Fiyat (TL)", min_value=1000)
        notlar = st.text_area("Özel Analitik Notlar")
        
        if st.form_submit_button("Sisteme İşle"):
            birim = fiyat / m2
            data = {
                "mulk_adi": baslik, "bolge": ilce, "mahalle": mahalle, 
                "m2": m2, "fiyat": fiyat, "birim_fiyat": birim, "notlar": notlar
            }
            supabase.table("portfoy").insert(data).execute()
            st.success("Bulut senkronizasyonu tamamlandı.")

# --- ANA EKRAN: ANALİTİK & İNCELEME ---
res = supabase.table("portfoy").select("*").execute()
df = pd.DataFrame(res.data)

if not df.empty:
    # Üst Özet Kartlar
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Hacim", f"{df['fiyat'].sum():,.0f} TL")
    c2.metric("Ort. m² Birim", f"{df['birim_fiyat'].mean():,.0f} TL")
    c3.metric("Aktif Portföy", len(df))

    st.divider()

    # İlanları Seçme ve İnceleme (Sahibinden Tarzı)
    st.subheader("🔍 Portföy Detay Analizi")
    secili_ilan_adi = st.selectbox("İncelemek istediğiniz ilanı seçin:", df['mulk_adi'].tolist())
    
    ilan_detay = df[df['mulk_adi'] == secili_ilan_adi].iloc[0]

    # Detay Kartı Tasarımı
    with st.container():
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown(f"### {ilan_detay['mulk_adi']}")
            st.info(f"📍 {ilan_detay['bolge']} / {ilan_detay['mahalle']}")
            st.write(f"**m²:** {ilan_detay['m2']}")
            st.write(f"**Birim Fiyat:** {ilan_detay['birim_fiyat']:,.0f} TL")
            st.error(f"**TOPLAM FİYAT: {ilan_detay['fiyat']:,.0f} TL**")
        
        with col_b:
            st.markdown("#### Danışman Notları & Strateji")
            st.write(ilan_detay['notlar'] if ilan_detay['notlar'] else "Not eklenmemiş.")
            # Basit bir kıyaslama grafiği
            st.bar_chart(df[df['bolge'] == ilan_detay['bolge']].set_index('mulk_adi')['birim_fiyat'])

    st.divider()
    st.write("### Tüm Veri Tablosu")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Sistemde analiz edilecek veri bulunamadı.")
# -------------------------------------------------------------

supabase = create_client(URL, KEY)

# İzmir Veri Seti (Örnekleme - Tüm ilçeler eklenebilir)
izmir_data = {
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Atatürk", "Kahramandere"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak"],
    "Buca": ["Adatepe", "Safir", "Yiğitler", "Şirinyer", "Dumlupınar", "Yıldız"],
    "Çeşme": ["Alaçatı", "Ilıca", "Musalla", "Boyalık", "Dalyan"],
    "Karşıyaka": ["Mavişehir", "Bostanlı", "Atakent", "Bahçelievler", "Tersane"]
}

st.set_page_config(page_title="FnekCRM PRO", layout="wide")

# Dark Theme & Kurumsal Stil
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #ffffff; font-weight: bold; }
    .stButton>button { width: 100%; background-color: #1f1f1f; color: white; border: 1px solid #333; }
    .stButton>button:hover { border-color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

st.title("⬛ FnekCRM | Executive Dashboard")

# --- SOL PANEL: VERİ GİRİŞİ ---
with st.sidebar:
    st.header("🏢 Portföy Kayıt")
    with st.form("pro_form", clear_on_submit=True):
        baslik = st.text_input("İlan Başlığı")
        ilce = st.selectbox("İlçe", list(izmir_data.keys()))
        mahalle = st.selectbox("Mahalle", izmir_data[ilce])
        m2 = st.number_input("Metrekare (Net)", min_value=1)
        fiyat = st.number_input("İstenen Fiyat (TL)", min_value=1000)
        notlar = st.text_area("Özel Analitik Notlar")
        
        if st.form_submit_button("Sisteme İşle"):
            birim = fiyat / m2
            data = {
                "mulk_adi": baslik, "bolge": ilce, "mahalle": mahalle, 
                "m2": m2, "fiyat": fiyat, "birim_fiyat": birim, "notlar": notlar
            }
            supabase.table("portfoy").insert(data).execute()
            st.success("Bulut senkronizasyonu tamamlandı.")

# --- ANA EKRAN: ANALİTİK & İNCELEME ---
res = supabase.table("portfoy").select("*").execute()
df = pd.DataFrame(res.data)

if not df.empty:
    # Üst Özet Kartlar
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Hacim", f"{df['fiyat'].sum():,.0f} TL")
    c2.metric("Ort. m² Birim", f"{df['birim_fiyat'].mean():,.0f} TL")
    c3.metric("Aktif Portföy", len(df))

    st.divider()

    # İlanları Seçme ve İnceleme (Sahibinden Tarzı)
    st.subheader("🔍 Portföy Detay Analizi")
    secili_ilan_adi = st.selectbox("İncelemek istediğiniz ilanı seçin:", df['mulk_adi'].tolist())
    
    ilan_detay = df[df['mulk_adi'] == secili_ilan_adi].iloc[0]

    # Detay Kartı Tasarımı
    with st.container():
        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.markdown(f"### {ilan_detay['mulk_adi']}")
            st.info(f"📍 {ilan_detay['bolge']} / {ilan_detay['mahalle']}")
            st.write(f"**m²:** {ilan_detay['m2']}")
            st.write(f"**Birim Fiyat:** {ilan_detay['birim_fiyat']:,.0f} TL")
            st.error(f"**TOPLAM FİYAT: {ilan_detay['fiyat']:,.0f} TL**")
        
        with col_b:
            st.markdown("#### Danışman Notları & Strateji")
            st.write(ilan_detay['notlar'] if ilan_detay['notlar'] else "Not eklenmemiş.")
            # Basit bir kıyaslama grafiği
            st.bar_chart(df[df['bolge'] == ilan_detay['bolge']].set_index('mulk_adi')['birim_fiyat'])

    st.divider()
    st.write("### Tüm Veri Tablosu")
    st.dataframe(df, use_container_width=True)

else:
    st.info("Sistemde analiz edilecek veri bulunamadı.")
