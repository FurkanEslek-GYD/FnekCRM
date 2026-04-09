import streamlit as st
from supabase import create_client
import pandas as pd

# --- ANALİTİK AYARLAR (Gömülü Anahtarlar) ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"

try:
    supabase = create_client(URL, KEY)
except:
    st.error("Veritabanı bağlantısı kurulamadı.")

# --- İZMİR 30 İLÇE VE KRİTİK MAHALLELER ---
izmir_full_data = {
    "Aliağa": ["Atatürk", "Yeni Mahalle", "Siteler", "Bahçelievler", "Kültür"],
    "Balçova": ["Korutürk", "Eğitim", "Onur", "Fevzi Çakmak", "Teleferik"],
    "Bayındır": ["Mithatpaşa", "Hacı Beşir", "Yeni Mahalle", "Cumhuriyet"],
    "Bayraklı": ["Mansuroğlu", "Manavkuyu", "Adalet", "Fuat Edip Baksi", "Osmangazi", "Tepekule"],
    "Bergama": ["İslamsaray", "Fatih", "Bahçelievler", "Maltepe"],
    "Beydağ": ["Atatürk", "Cumhuriyet", "Akıncılar"],
    "Bornova": ["Kazımdirik", "Özkanlar", "Manavkuyu", "Mevlana", "Erzene", "Işıklar", "Yeşilova", "Doğanlar"],
    "Buca": ["Adatepe", "Safir (Yıldız)", "Yiğitler", "Şirinyer", "Dumlupınar", "Buca Koop", "Kuruçeşme", "Efeler"],
    "Çeşme": ["Alaçatı", "Ilıca", "Musalla", "Boyalık", "Dalyan", "Reisdere", "Ovacık", "Fahrettin Paşa"],
    "Çiğli": ["Ataşehir", "Yeni Mahalle", "Balatçık", "Sasalı", "İzkent", "Egekent"],
    "Dikili": ["İsmetpaşa", "Salihler", "Çandarlı", "Bademli"],
    "Foça": ["Atatürk", "Fevzipaşa", "Yenifoça", "Kocamehmetler"],
    "Gaziemir": ["Atıfbey", "Yeşil Mahalle", "Irmak", "Sevgi", "Sarnıç", "Dokuz Eylül", "Hürriyet"],
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Atatürk", "Kahramandere", "Payamlı"],
    "Karabağlar": ["Bahçelievler", "Üçkuyular", "Poligon", "Basın Sitesi", "Esentepe", "Vatan"],
    "Karaburun": ["Merkez", "Mordoğan", "İskele", "Eskifoca"],
    "Karşıyaka": ["Mavişehir", "Bostanlı", "Atakent", "Bahçelievler", "Tersane", "Aksoy", "Donanmacı", "Nergiz", "Demirköprü"],
    "Kemalpaşa": ["Sekiz Eylül", "Soğukpınar", "Uluca", "Örnekköy"],
    "Kınık": ["Yeni Mahalle", "Fatih", "Osmaniye"],
    "Kiraz": ["İstiklal", "Cumhuriyet", "Yeni Mahalle"],
    "Konak": ["Alsancak", "Göztepe", "Güzelyalı", "Hatay", "Karantina", "Küçükyalı", "Kültür", "Mimar Sinan", "Güneşli"],
    "Menderes": ["Cüneytbey", "Barbaros", "Gümüldür", "Özdere", "Tekeli"],
    "Menemen": ["Ulukent", "Egekent 2", "Asarlık", "Kasımpaşa", "İstiklal"],
    "Narlıdere": ["Yenikale", "Sahilevleri", "Huzur", "Limanreis", "Çatalkaya", "Narlı", "Ilıca"],
    "Ödemiş": ["Akıncılar", "Hürriyet", "Anafartalar", "Atatürk"],
    "Seferihisar": ["Sığacık", "Akarca", "Camikebir", "Hıdırlık", "Ürkmez", "Turabiye"],
    "Selçuk": ["İsabey", "Atatürk", "Cumhuriyet"],
    "Tire": ["Fatih", "Atatürk", "Hürriyet", "Cumhuriyet"],
    "Torbalı": ["Tepeköy", "Ertuğrul", "Ayrancılar", "Torbalı Mahallesi", "Yedi Eylül"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak", "Güvendik", "Denizli", "Çamlıçay"]
}

st.set_page_config(page_title="FnekCRM PRO", layout="wide")

# Dark Executive Tasarım (Ağır Abi Modu)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    [data-testid="stMetricValue"] { color: #ffffff !important; font-size: 28px; font-weight: 800; }
    .stMetric { background-color: #1a1c23; padding: 25px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .stSidebar { background-color: #0b0e14; border-right: 1px solid #30363d; }
    h1, h2, h3 { color: #ffffff; font-family: 'Inter', sans-serif; letter-spacing: -0.5px; }
    .stButton>button { background-color: #ffffff; color: #000000; font-weight: bold; border-radius: 5px; border: none; transition: 0.3s; }
    .stButton>button:hover { background-color: #cccccc; }
    </style>
    """, unsafe_allow_html=True)

st.title("⬛ FnekCRM | Analitik Gayrimenkul Yönetimi")

# --- SOL PANEL: DİNAMİK VERİ GİRİŞİ ---
with st.sidebar:
    st.header("🏢 Portföy Kaydı")
    
    # Mahalle sorunu için dinamik kutular (Form dışına alındı)
    ilce_secimi = st.selectbox("İlçe", list(izmir_full_data.keys()), key="ilce_sb")
    mahalle_secimi = st.selectbox("Mahalle", izmir_full_data[ilce_secimi], key="mahalle_sb")

    with st.form("kayit_formu", clear_on_submit=True):
        baslik = st.text_input("İlan Başlığı (Örn: Güzelbahçe Müstakil)")
        m2 = st.number_input("Metrekare (Net)", min_value=1, step=1)
        fiyat = st.number_input("Toplam Fiyat (TL)", min_value=1000, step=50000)
        notlar = st.text_area("Analitik Notlar & Mülk Sahibi Durumu")
        
        if st.form_submit_button("Sisteme Güvenli Kaydet"):
            if baslik:
                birim = fiyat / m2
                data = {
                    "mulk_adi": baslik, "bolge": ilce_secimi, "mahalle": mahalle_secimi, 
                    "m2": m2, "fiyat": fiyat, "birim_fiyat": birim, "notlar": notlar
                }
                supabase.table("portfoy").insert(data).execute()
                st.success("Veri buluta işlendi.")
                st.rerun()
            else:
                st.warning("İlan başlığı boş bırakılamaz.")

# --- ANA EKRAN: ANALİTİK PANEL ---
try:
    res = supabase.table("portfoy").select("*").order("eklenme_tarihi", desc=True).execute()
    df = pd.DataFrame(res.data)
except:
    df = pd.DataFrame()

if not df.empty:
    # Üst Metrikler
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Portföy Hacmi", f"{df['fiyat'].sum():,.0f} TL")
    c2.metric("Ağırlıklı m² Ortalaması", f"{df['birim_fiyat'].mean():,.0f} TL")
    c3.metric("Aktif İlan Sayısı", len(df))

    st.divider()

    # İnceleme Paneli (Sahibinden Tarzı)
    st.subheader("🔍 Portföy Detay Analizi")
    secili_ilan = st.selectbox("İncelemek istediğiniz portföyü seçin:", df['mulk_adi'].tolist())
    d = df[df['mulk_adi'] == secili_ilan].iloc[0]

    col_sol, col_sag = st.columns([1, 2])
    with col_sol:
        st.markdown(f"### {d['mulk_adi']}")
        st.info(f"📍 {d['bolge']} / {d['mahalle']}")
        st.write(f"📏 **Net Alan:** {int(d['m2'])} m²")
        st.write(f"📊 **m² Birim:** {d['birim_fiyat']:,.0f} TL")
        st.error(f"💰 **TOPLAM: {d['fiyat']:,.0f} TL**")
    
    with col_sag:
        st.markdown("#### Danışman Notları & Strateji")
        st.write(d['notlar'] if d['notlar'] else "Not eklenmemiş.")
        # Bölge bazlı analiz grafiği
        st.write(f"📈 **{d['bolge']} Bölgesi Karşılaştırmalı Analiz**")
        bolge_df = df[df['bolge'] == d['bolge']]
        st.bar_chart(bolge_df.set_index('mulk_adi')['birim_fiyat'])

    st.divider()
    
    # Veri Tablosu
    with st.expander("📂 Tüm Veri Setini İncele"):
        st.dataframe(df, use_container_width=True)
else:
    st.info("Sistem şu an boş. Sol taraftan ilk analitik verinizi girebilirsiniz Furkan Bey.")
