import streamlit as st
from supabase import create_client
import pandas as pd
import plotly.express as px

# --- 1. GÜVENLİK (3003Locate) ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "3003Locate":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False
    if "password_correct" not in st.session_state:
        st.markdown("### 🔒 FnekCRM | Kurumsal Giriş")
        st.text_input("Şifre", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Şifre", type="password", on_change=password_entered, key="password")
        st.error("❌ Hatalı Şifre!")
        return False
    return True

if not check_password():
    st.stop()

# --- 2. BAĞLANTI ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"
supabase = create_client(URL, KEY)

# İzmir Veri Seti
izmir_data = {
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Atatürk", "Kahramandere"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak", "Güvendik"],
    "Buca": ["Adatepe", "Safir (Yıldız)", "Yiğitler", "Şirinyer", "Dumlupınar", "Buca Koop"],
    "Narlıdere": ["Yenikale", "Sahilevleri", "Huzur", "Limanreis", "Çatalkaya"]
}

st.set_page_config(page_title="FnekCRM Executive", layout="wide")
st.title("⬛ FnekCRM | Profesyonel Operasyon")

tab1, tab2, tab3 = st.tabs(["📁 PORTFÖY YÖNETİMİ", "👤 MÜŞTERİ (CRM)", "🔥 FSBO TAKİP"])

# --- TAB 1: PORTFÖY ---
with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Yeni Kayıt")
        ilce = st.selectbox("İlçe", list(izmir_data.keys()), key="p_ilce")
        mahalle = st.selectbox("Mahalle", izmir_data[ilce], key="p_mah")
        with st.form("p_form"):
            p_baslik = st.text_input("Mülk Başlığı*")
            p_fiyat = st.number_input("Fiyat (TL)", min_value=0)
            p_m2 = st.number_input("Net m2", min_value=1)
            p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren Satılık", "Devren Kiralık"])
            p_tip = st.selectbox("Tip", ["Konut", "Ticari", "Arsa"])
            p_drive = st.text_input("Drive Link (Opsiyonel)")
            p_soz = st.text_input("Sözleşme Link (Opsiyonel)")
            p_not = st.text_area("Analitik Notlar")
            if st.form_submit_button("Sisteme İşle"):
                if p_baslik:
                    supabase.table("portfoy_yeni").insert({
                        "baslik": p_baslik, "ilce": ilce, "mahalle": mahalle, "fiyat": p_fiyat,
                        "m2": p_m2, "birim_fiyat": p_fiyat/p_m2 if p_m2 > 0 else 0, 
                        "islem_tipi": p_islem, "mulk_tipi": p_tip, 
                        "resim_link": p_drive if p_drive else None, 
                        "sozlesme_link": p_soz if p_soz else None, "notlar": p_not
                    }).execute()
                    st.rerun()

    with c2:
        res_p = supabase.table("portfoy_yeni").select("*").execute()
        df_p = pd.DataFrame(res_p.data)
        if not df_p.empty:
            st.subheader("📊 Envanter Analizi")
            st.metric("Toplam Hacim", f"{df_p['fiyat'].sum():,.0f} TL")
            
            secili = st.selectbox("Mülk Detayı:", df_p['baslik'].tolist())
            d = df_p[df_p['baslik'] == secili].iloc[0]
            
            st.info(f"📍 {d['ilce']} / {d['mahalle']} | {d['islem_tipi']}")
            st.write(f"**Notlar:** {d['notlar']}")
            
            sc1, sc2 = st.columns(2)
            with sc1:
                if d['resim_link']: st.link_button("📂 Drive Resimleri", d['resim_link'])
            with sc2:
                if d['sozlesme_link']: st.link_button("📄 Sözleşme Detayı", d['sozlesme_link'])
        else:
            st.info("Henüz portföy girişi yapılmadı.")

# --- TAB 2: CRM ---
with tab2:
    c3, c4 = st.columns([1, 2])
    with c3:
        st.subheader("Müşteri Kaydı")
        with st.form("m_form"):
            m_ad = st.text_input("Ad Soyad")
            m_tel = st.text_input("Telefon")
            m_rol = st.selectbox("Rol", ["Alıcı", "Satıcı"])
            m_butce = st.text_input("Bütçe/Beklenti")
            m_ilgi = st.text_area("Notlar")
            if st.form_submit_button("Müşteri Ekle"):
                supabase.table("musteriler").insert({
                    "ad_soyad": m_ad, "telefon": m_tel, "rol": m_rol, 
                    "butce_beklenti": m_butce, "ilgi_alani": m_ilgi
                }).execute()
                st.rerun()
    with c4:
        st.subheader("Rehber")
        res_m = supabase.table("musteriler").select("*").execute()
        df_m = pd.DataFrame(res_m.data)
        if not df_m.empty:
            st.dataframe(df_m[['ad_soyad', 'telefon', 'rol', 'butce_beklenti']], use_container_width=True)
        else:
            st.info("Müşteri listesi boş.")

# --- TAB 3: FSBO ---
with tab3:
    c5, c6 = st.columns([1, 2])
    with c5:
        st.subheader("FSBO Takip")
        with st.form("f_form"):
            f_link = st.text_input("İlan Linki")
            f_ad = st.text_input("Mal Sahibi")
            f_tel = st.text_input("Telefon")
            f_ozet = st.text_input("Mülk Özeti")
            f_durum = st.selectbox("Durum", ["Potansiyel", "Randevu", "Portföy", "İptal"])
            if st.form_submit_button("FSBO Kaydet"):
                supabase.table("fsbo_takip").insert({
                    "ilan_link": f_link, "mal_sahibi_ad": f_ad, "mal_sahibi_tel": f_tel, 
                    "mulk_ozeti": f_ozet, "durum": f_durum
                }).execute()
                st.rerun()
    with c6:
        st.subheader("Saha Takip Listesi")
        res_f = supabase.table("fsbo_takip").select("*").execute()
        df_f = pd.DataFrame(res_f.data)
        if not df_f.empty:
            st.dataframe(df_f[['mal_sahibi_ad', 'mal_sahibi_tel', 'durum', 'mulk_ozeti']], use_container_width=True)
        else:
            st.info("FSBO takibi boş.")
