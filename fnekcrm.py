import streamlit as st
from supabase import create_client
import pandas as pd

# --- GÜVENLİK ---
if "auth" not in st.session_state:
    st.session_state.auth = False

def login():
    st.title("⬛ FnekCRM Giriş")
    pw = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if pw == "3003Locate":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Hatalı!")

if not st.session_state.auth:
    login()
    st.stop()

# --- BAĞLANTI ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="FnekCRM Pro", layout="wide")
st.title("⬛ FnekCRM | Kurumsal Operasyon")

t1, t2, t3 = st.tabs(["📁 PORTFÖY", "👤 CRM", "🔥 FSBO"])

# --- TAB 1: PORTFÖY ---
with t1:
    c1, c2 = st.columns([1, 2])
    with c1:
        with st.form("portfoy_form"):
            st.subheader("Yeni Kayıt")
            p_baslik = st.text_input("Mülk Başlığı*")
            p_ilce = st.selectbox("İlçe", ["Güzelbahçe", "Urla", "Buca", "Narlıdere"])
            p_fiyat = st.number_input("Fiyat", min_value=0)
            p_m2 = st.number_input("m2", min_value=1)
            p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren"])
            if st.form_submit_button("KAYDET"):
                if p_baslik:
                    # SQL'deki tablo sütunlarıyla %100 eşleşen veri yapısı
                    data_p = {
                        "baslik": p_baslik,
                        "ilce": p_ilce,
                        "fiyat": float(p_fiyat),
                        "m2": float(p_m2),
                        "birim_fiyat": float(p_fiyat/p_m2),
                        "islem_tipi": p_islem
                    }
                    supabase.table("portfoy_yeni").insert(data_p).execute()
                    st.success("Kaydedildi!")
                    st.rerun()

    with c2:
        res_p = supabase.table("portfoy_yeni").select("*").execute()
        if res_p.data:
            st.dataframe(pd.DataFrame(res_p.data)[['baslik', 'ilce', 'fiyat', 'islem_tipi']], use_container_width=True)

# --- TAB 2: CRM ---
with t2:
    c3, c4 = st.columns([1, 2])
    with c3:
        with st.form("crm_form"):
            st.subheader("Müşteri Ekle")
            m_ad = st.text_input("Ad Soyad")
            m_tel = st.text_input("Telefon")
            m_rol = st.selectbox("Rol", ["Alıcı", "Satıcı"])
            if st.form_submit_button("CRM KAYDET"):
                supabase.table("musteriler").insert({"ad_soyad": m_ad, "telefon": m_tel, "rol": m_rol}).execute()
                st.rerun()
    with c4:
        res_m = supabase.table("musteriler").select("*").execute()
        if res_m.data:
            st.dataframe(pd.DataFrame(res_m.data)[['ad_soyad', 'telefon', 'rol']], use_container_width=True)

# --- TAB 3: FSBO ---
with t3:
    c5, c6 = st.columns([1, 2])
    with c5:
        with st.form("fsbo_form"):
            st.subheader("Saha Takibi")
            f_ad = st.text_input("Mal Sahibi")
            f_tel = st.text_input("İletişim")
            f_durum = st.selectbox("Durum", ["Potansiyel", "Randevu", "Portföy"])
            if st.form_submit_button("FSBO KAYDET"):
                supabase.table("fsbo_takip").insert({"mal_sahibi_ad": f_ad, "mal_sahibi_tel": f_tel, "durum": f_durum}).execute()
                st.rerun()
    with c6:
        res_f = supabase.table("fsbo_takip").select("*").execute()
        if res_f.data:
            st.dataframe(pd.DataFrame(res_f.data)[['mal_sahibi_ad', 'mal_sahibi_tel', 'durum']], use_container_width=True)
