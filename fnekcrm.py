import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. GÜVENLİK (3003Locate) ---
if "auth" not in st.session_state:
    st.session_state.auth = False

def login():
    st.title("⬛ FnekCRM Giriş")
    pw = st.text_input("Yönetici Şifresi", type="password")
    if st.button("Sistemi Aç"):
        if pw == "3003Locate":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı Şifre!")

if not st.session_state.auth:
    login()
    st.stop()

# --- 2. BAĞLANTI AYARLARI ---
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
st.title("⬛ FnekCRM | Operasyonel Yönetim")

tab1, tab2, tab3 = st.tabs(["📁 PORTFÖY YÖNETİMİ", "👤 MÜŞTERİ (CRM)", "🔥 FSBO TAKİP"])

# --- TAB 1: PORTFÖY ---
with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Yeni Kayıt")
        ilce_p = st.selectbox("İlçe", list(izmir_data.keys()), key="p_ilce")
        mahalle_p = st.selectbox("Mahalle", izmir_data[ilce_p], key="p_mah")
        with st.form("p_form_final"):
            p_baslik = st.text_input("Mülk Adı*")
            col_a, col_b = st.columns(2)
            with col_a:
                p_fiyat = st.number_input("Fiyat (TL)", min_value=0)
            with col_b:
                p_m2 = st.number_input("Net m2", min_value=1)
            
            p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren Satılık"])
            p_tip = st.selectbox("Tip", ["Konut", "Ticari", "Arsa"])
            p_drive = st.text_input("Drive Link (Opsiyonel)")
            p_soz = st.text_input("Sözleşme Link (Opsiyonel)")
            
            if st.form_submit_button("Sisteme İşle"):
                if p_baslik:
                    supabase.table("portfoy_yeni").insert({
                        "baslik": p_baslik, "ilce": ilce_p, "mahalle": mahalle_p,
                        "fiyat": p_fiyat, "m2": p_m2, "birim_fiyat": p_fiyat/p_m2,
                        "islem_tipi": p_islem, "mulk_tipi": p_tip,
                        "resim_link": p_drive if p_drive else None,
                        "sozlesme_link": p_soz if p_soz else None
                    }).execute()
                    st.success("Portföy Kaydedildi.")
                    st.rerun()
                else:
                    st.error("Mülk adı boş bırakılamaz.")
    
    with c2:
        st.subheader("Envanter")
        try:
            res_p = supabase.table("portfoy_yeni").select("*").order("eklenme_tarihi", desc=True).execute()
            df_p = pd.DataFrame(res_p.data)
            if not df_p.empty:
                st.dataframe(df_p[['baslik', 'ilce', 'fiyat', 'islem_tipi']], use_container_width=True)
            else:
                st.info("Portföy listesi henüz boş.")
        except:
            st.warning("Veriler yüklenirken bir hata oluştu.")

# --- TAB 2: CRM ---
with tab2:
    c3, c4 = st.columns([1, 2])
    with c3:
        st.subheader("CRM Girişi")
        with st.form("m_form"):
            m_ad = st.text_input("Müşteri Ad Soyad")
            m_tel = st.text_input("Telefon")
            m_rol = st.selectbox("Rol", ["Alıcı", "Satıcı"])
            m_butce = st.text_input("Bütçe/Beklenti")
            if st.form_submit_button("Müşteri Kaydet"):
                supabase.table("musteriler").insert({"ad_soyad": m_ad, "telefon": m_tel, "rol": m_rol, "butce_beklenti": m_butce}).execute()
                st.success("Müşteri eklendi.")
                st.rerun()
    with c4:
        st.subheader("Müşteri Rehberi")
        try:
            res_m = supabase.table("musteriler").select("*").execute()
            df_m = pd.DataFrame(res_m.data)
            if not df_m.data: st.info("Rehber boş.")
            else: st.dataframe(df_m[['ad_soyad', 'telefon', 'rol']], use_container_width=True)
        except: st.info("Müşteri verisi bulunamadı.")

# --- TAB 3: FSBO ---
with tab3:
    c5, c6 = st.columns([1, 2])
    with c5:
        st.subheader("Saha Takip")
        with st.form("f_form"):
            f_ad = st.text_input("Mal Sahibi")
            f_tel = st.text_input("İletişim")
            f_ozet = st.text_input("Mülk Özeti")
            f_durum = st.selectbox("Durum", ["Potansiyel", "Randevu", "Portföy"])
            if st.form_submit_button("FSBO Kaydet"):
                supabase.table("fsbo_takip").insert({"mal_sahibi_ad": f_ad, "mal_sahibi_tel": f_tel, "mulk_ozeti": f_ozet, "durum": f_durum}).execute()
                st.success("FSBO eklendi.")
                st.rerun()
    with c6:
        st.subheader("Takip Listesi")
        try:
            res_f = supabase.table("fsbo_takip").select("*").execute()
            df_f = pd.DataFrame(res_f.data)
            if not df_f.data: st.info("Takip listesi boş.")
            else: st.dataframe(df_f[['mal_sahibi_ad', 'mal_sahibi_tel', 'durum']], use_container_width=True)
        except: st.info("Saha verisi bulunamadı.")
