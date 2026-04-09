import streamlit as st
from supabase import create_client
import pandas as pd

# --- ANALİTİK AYARLAR ---
# Buradaki tırnak içindeki kısımları kendi bilgilerinizle doldurun
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"
# -------------------------

try:
    supabase = create_client(URL, KEY)
except:
    st.error("Veritabanı bağlantısı kurulamadı. Lütfen anahtarları kontrol edin.")

# İzmir Genişletilmiş Veri Seti
izmir_data = {
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Atatürk", "Kahramandere", "Küçükkaya", "Payamlı"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak", "Güvendik", "Yenice", "Hacı İsa"],
    "Buca": ["Adatepe", "Safir", "Yiğitler", "Şirinyer", "Dumlupınar", "Yıldız", "Kuruçeşme", "Buca Koop"],
    "Çeşme": ["Alaçatı", "Ilıca", "Musalla", "Boyalık", "Dalyan", "Reisdere", "Germiyan", "Ovacık"],
    "Karşıyaka": ["Mavişehir", "Bostanlı", "Atakent", "Bahçelievler", "Tersane", "Alaybey", "Aksoy"],
    "Konak": ["Alsancak", "Göztepe", "Güzelyalı", "Hatay", "Karantina", "Küçükyalı", "Kahramanlar"],
    "Bornova": ["Kazımdirik", "Özkanlar", "Manavkuyu", "Mevlana", "Erzene", "Işıklar"],
    "Narlıdere": ["Yenikale", "Sahilevleri", "Huzur", "Limanreis", "Çatalkaya"],
    "Gaziemir": ["Atıfbey", "Yeşil mahallesi", "Irmak", "Sevgi", "Binbaşı Reşat Bey"],
    "Seferihisar": ["Sığacık", "Akarca", "Camikebir", "Hıdırlık"]
}

st.set_page_config(page_title="FnekCRM PRO", layout="wide")

# Dark Executive Tasarım Kodları
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 24px; }
    .stMetric { background-color: #1a1c23; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
    .stSidebar { background-color: #0b0e14; }
    h1, h2, h3 { color: #ffffff; font-family: 'Inter', sans-serif; }
    .stDataFrame { border: 1px solid #30363d; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⬛ FnekCRM | Analitik Gayrimenkul Yönetimi")

# --- SOL PANEL: VERİ GİRİŞİ ---
with st.sidebar:
    st.image("https://www.google.com/s2/favicons?domain=github.com&sz=64") # Geçici Logo
    st.header("🏢 Yeni Portföy Kaydı")
    with st.form("pro_form", clear_on_submit=True):
        baslik = st.text_input("İlan Başlığı (Örn: Deniz Manzaralı Villa)")
        ilce = st.selectbox("İlçe Seçiniz", list(izmir_data.keys()))
        mahalle = st.selectbox("Mahalle Seçiniz", izmir_data[ilce])
        m2 = st.number_input("Metrekare (Net m²)", min_value=1, step=1)
        fiyat = st.number_input("İstenen Toplam Fiyat (TL)", min_value=1000, step=10000)
        notlar = st.text_area("Analitik Notlar & Mülk Sahibi Durumu")
        
        submit = st.form_submit_button("Sisteme Güvenli Kaydet")
        
        if submit:
            if baslik:
                birim = fiyat / m2
                data = {
                    "mulk_adi": baslik, "bolge": ilce, "mahalle": mahalle, 
                    "m2": m2, "fiyat": fiyat, "birim_fiyat": birim, "notlar": notlar
                }
                try:
                    supabase.table("portfoy").insert(data).execute()
                    st.success("Veri bulut sunucularına işlendi.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Hata: {e}")
            else:
                st.warning("Lütfen bir ilan başlığı girin.")

# --- ANA EKRAN: ANALİTİK DASHBOARD ---
try:
    res = supabase.table("portfoy").select("*").order("eklenme_tarihi", desc=True).execute()
    df = pd.DataFrame(res.data)
except:
    df = pd.DataFrame()

if not df.empty:
    # 1. Üst Özet Metrikleri
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Toplam Hacim", f"{df['fiyat'].sum():,.0f} TL")
    c2.metric("Ortalama m² Fiyatı", f"{df['birim_fiyat'].mean():,.0f} TL")
    c3.metric("Toplam Portföy", len(df))
    c4.metric("En Değerli Bölge", df.loc[df['birim_fiyat'].idxmax()]['bolge'])

    st.divider()

    # 2. Sahibinden Tarzı İnceleme Paneli
    st.subheader("🔍 Portföy Detay İnceleme (Sahibinden Arayüzü)")
    secili_ilan = st.selectbox("İncelemek istediğiniz portföyü seçin:", df['mulk_adi'].tolist())
    
    ilan_detay = df[df['mulk_adi'] == secili_ilan].iloc[0]

    with st.container():
        col_sol, col_sag = st.columns([1.5, 2.5])
        
        with col_sol:
            st.markdown(f"### {ilan_detay['mulk_adi']}")
            st.markdown(f"**📍 Konum:** {ilan_detay['bolge']} / {ilan_detay['mahalle']}")
            st.markdown(f"**📐 Alan:** {int(ilan_detay['m2'])} m²")
            st.markdown(f"**💰 Toplam Fiyat:** {ilan_detay['fiyat']:,.0f} TL")
            st.markdown(f"**📊 Birim m² Fiyatı:** {ilan_detay['birim_fiyat']:,.0f} TL")
            st.caption(f"Kayıt Tarihi: {ilan_detay['eklenme_tarihi']}")

        with col_sag:
            st.info("💡 **Analitik Notlar & Strateji**")
            st.write(ilan_detay['notlar'] if ilan_detay['notlar'] else "Bu portföy için henüz not eklenmemiş.")
            
            # Bölge Kıyaslama Grafiği
            st.write(f"**{ilan_detay['bolge']} Bölgesi Fiyat Kıyaslaması**")
            bolge_df = df[df['bolge'] == ilan_detay['bolge']]
            st.bar_chart(bolge_df.set_index('mulk_adi')['birim_fiyat'])

    st.divider()
    
    # 3. Genel Liste
    with st.expander("📂 Tüm Portföy Listesini Gör"):
        st.dataframe(df, use_container_width=True)

else:
    st.info("Henüz veri girişi yapılmamış. Sol panelden ilk portföyünüzü kaydedebilirsiniz.")
