import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. GÜVENLİK VE GİRİŞ ---
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

# --- 2. VERİTABANI BAĞLANTISI ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"
supabase = create_client(URL, KEY)

st.set_page_config(page_title="FnekCRM Pro", layout="wide")
st.title("⬛ FnekCRM | Kurumsal Operasyon")

# --- 3. SEKMELERİN TANIMLANMASI ---
t1, t2, t3 = st.tabs(["📁 PORTFÖY (v2)", "👤 MÜŞTERİ (CRM)", "🔥 FSBO TAKİP"])

# --- TAB 1: PORTFÖY (v2) ---
with t1:
    c1, c2 = st.columns([1, 2])
    with c1:
        with st.form("p_form_v2_final"):
            st.subheader("Yeni Portföy Kaydı")
            p_baslik = st.text_input("Mülk Başlığı*")
            p_fiyat = st.number_input("Fiyat (TL)", min_value=0)
            p_m2 = st.number_input("m2", min_value=1)
            p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren"])
            p_ilce = st.selectbox("İlçe", ["Güzelbahçe", "Urla", "Buca", "Narlıdere"])
            
            if st.form_submit_button("KAYDET"):
                if p_baslik:
                    data_p = {
                        "baslik": p_baslik,
                        "fiyat": float(p_fiyat),
                        "m2": float(p_m2),
                        "birim_fiyat": float(p_fiyat/p_m2) if p_m2 > 0 else 0,
                        "islem_tipi": p_islem,
                        "ilce": p_ilce
                    }
                    supabase.table("portfoy_v2").insert(data_p).execute()
                    st.success("Portföy başarıyla eklendi!")
                    st.rerun()

    with c2:
        st.subheader("Aktif Envanter")
        try:
            res_p = supabase.table("portfoy_v2").select("*").execute()
            if res_p.data:
                df_p = pd.DataFrame(res_p.data)
                st.dataframe(df_p[['baslik', 'fiyat', 'islem_tipi', 'ilce']], use_container_width=True)
            else:
                st.info("Portföy listesi boş.")
        except:
            st.warning("Veri tabanı bağlantısı bekleniyor...")

# --- TAB 2: MÜŞTERİ (CRM) ---
with t2:
    c3, c4 = st.columns([1, 2])
    with c3:
        with st.form("crm_form_final"):
            st.subheader("Müşteri Kaydı")
            m_ad = st.text_input("Ad Soyad")
            m_tel = st.text_input("Telefon")
            m_rol = st.selectbox("Rol", ["Alıcı", "Satıcı"])
            if st.form_submit_button("CRM EKLE"):
                supabase.table("musteriler").insert({"ad_soyad": m_ad, "telefon": m_tel, "rol": m_rol}).execute()
                st.success("Müşteri kaydedildi.")
                st.rerun()
    with c4:
        st.subheader("Müşteri Portföyü")
        try:
            res_m = supabase.table("musteriler").select("*").execute()
            if res_m.data:
                st.dataframe(pd.DataFrame(res_m.data)[['ad_soyad', 'telefon', 'rol']], use_container_width=True)
        except:
            st.info("Henüz müşteri kaydı yok.")

# --- TAB 3: FSBO TAKİP ---
with t3:
    c5, c6 = st.columns([1, 2])
    with c5:
        with st.form("fsbo_form_final"):
            st.subheader("FSBO Takip")
            f_ad = st.text_input("Mal Sahibi")
            f_tel = st.text_input("İletişim No")
            f_durum = st.selectbox("Durum", ["Potansiyel", "Randevu", "Portföy"])
            if st.form_submit_button("FSBO EKLE"):
                supabase.table("fsbo_takip").insert({"mal_sahibi_ad": f_ad, "mal_sahibi_tel": f_tel, "durum": f_durum}).execute()
                st.success("Takip listesine eklendi.")
                st.rerun()
    with c6:
        st.subheader("Saha Takip Listesi")
        try:
            res_f = supabase.table("fsbo_takip").select("*").execute()
            if res_f.data:
                st.dataframe(pd.DataFrame(res_f.data)[['mal_sahibi_ad', 'mal_sahibi_tel', 'durum']], use_container_width=True)
        except:
            st.info("FSBO takibi boş.")
