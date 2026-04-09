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

# İzmir Veri Seti (Özet Liste)
izmir_data = {
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Atatürk", "Kahramandere"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak", "Güvendik"],
    "Buca": ["Adatepe", "Safir (Yıldız)", "Yiğitler", "Şirinyer", "Dumlupınar", "Buca Koop"],
    "Çeşme": ["Alaçatı", "Ilıca", "Musalla", "Boyalık", "Dalyan", "Reisdere"],
    "Karşıyaka": ["Mavişehir", "Bostanlı", "Atakent", "Bahçelievler", "Aksoy"],
    "Konak": ["Alsancak", "Göztepe", "Güzelyalı", "Hatay", "Kültür"],
    "Narlıdere": ["Yenikale", "Sahilevleri", "Huzur", "Limanreis", "Çatalkaya"]
}

st.set_page_config(page_title="FnekCRM Executive", layout="wide")

# UI Tasarımı
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #1a1c23; border-radius: 5px; color: white; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #ffffff; color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⬛ FnekCRM | Operasyonel Yönetim Merkezi")

tab1, tab2, tab3 = st.tabs(["📁 PORTFÖY KASASI", "👤 MÜŞTERİ (CRM)", "🔥 FSBO SAHA TAKİBİ"])

# --- 1. PORTFÖY KASASI ---
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Yeni Portföy Girişi")
        ilce_p = st.selectbox("İlçe", list(izmir_data.keys()), key="p_ilce")
        mahalle_p = st.selectbox("Mahalle", izmir_data[ilce_p], key="p_mah")
        
        with st.form("portfoy_form_v3"):
            p_baslik = st.text_input("Mülk Başlığı")
            c_a, c_b = st.columns(2)
            with c_a:
                p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren Satılık", "Devren Kiralık"])
            with c_b:
                p_tip = st.selectbox("Tip", ["Konut", "Ticari", "Arsa", "Turistik"])
            
            p_fiyat = st.number_input("Fiyat (TL)", min_value=0)
            p_m2 = st.number_input("m² (Net)", min_value=1)
            p_resim = st.text_input("Resim/Klasör Linki")
            p_soz = st.text_input("Sözleşme Linki")
            
            if st.form_submit_button("Sisteme Kilitle"):
                birim = p_fiyat / p_m2
                supabase.table("portfoy_yeni").insert({
                    "baslik": p_baslik, "ilce": ilce_p, "mahalle": mahalle_p,
                    "fiyat": p_fiyat, "m2": p_m2, "birim_fiyat": birim,
                    "islem_tipi": p_islem, "mulk_tipi": p_tip,
                    "resim_link": p_resim, "sozlesme_link": p_soz
                }).execute()
                st.success("Portföy başarıyla kaydedildi.")
                st.rerun()

    with col2:
        st.subheader("Portföy Envanteri")
        try:
            df_p = pd.DataFrame(supabase.table("portfoy_yeni").select("*").execute().data)
            st.dataframe(df_p, use_container_width=True)
        except: st.info("Henüz portföy yok.")

# --- 2. MÜŞTERİ (CRM) ---
with tab2:
    col3, col4 = st.columns([1, 2])
    with col3:
        st.subheader("Müşteri Kayıt")
        with st.form("crm_form"):
            m_ad = st.text_input("Ad Soyad")
            m_tel = st.text_input("Telefon")
            m_rol = st.selectbox("Rol", ["Alıcı", "Satıcı"])
            m_butce = st.text_input("Bütçe / Beklenti")
            m_not = st.text_area("İlgi Alanı & Notlar")
            if st.form_submit_button("Müşteriyi Arşive Ekle"):
                supabase.table("musteriler").insert({"ad_soyad": m_ad, "telefon": m_tel, "rol": m_rol, "butce_beklenti": m_butce, "ilgi_alani": m_not}).execute()
                st.rerun()
    with col4:
        st.subheader("Müşteri Listesi")
        try:
            df_m = pd.DataFrame(supabase.table("musteriler").select("*").execute().data)
            st.dataframe(df_m, use_container_width=True)
        except: st.info("Müşteri kaydı bulunmuyor.")

# --- 3. FSBO SAHA TAKİBİ ---
with tab3:
    col5, col6 = st.columns([1, 2])
    with col5:
        st.subheader("Sıcak FSBO Girişi")
        with st.form("fsbo_form_v3"):
            f_link = st.text_input("İlan Linki")
            f_ozet = st.text_input("Mülk Detayı (Örn: 2+1 Eşyalı)")
            f_ad = st.text_input("Mal Sahibi")
            f_tel = st.text_input("Mal Sahibi Tel")
            f_durum = st.selectbox("Durum", ["Potansiyel", "Randevu Alındı", "Portföy Oldu", "İptal"])
            f_not = st.text_area("Görüşme Geçmişi")
            if st.form_submit_button("Takibi Başlat"):
                supabase.table("fsbo_takip").insert({
                    "ilan_link": f_link, "mulk_ozeti": f_ozet,
                    "mal_sahibi_ad": f_ad, "mal_sahibi_tel": f_tel,
                    "durum": f_durum, "gorusme_notlari": f_not
                }).execute()
                st.rerun()
    with col6:
        st.subheader("Takip Çizelgesi")
        try:
            df_f = pd.DataFrame(supabase.table("fsbo_takip").select("*").execute().data)
            st.dataframe(df_f, use_container_width=True)
        except: st.info("Takipte ilan yok.")
