import streamlit as st
from supabase import create_client
import pandas as pd

# --- BAĞLANTI ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"
supabase = create_client(URL, KEY)

# --- GİRİŞ ---
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    with st.form("login_form"):
        pw = st.text_input("Yönetici Şifresi", type="password")
        if st.form_submit_button("Sistemi Aç"):
            if pw == "3003Locate":
                st.session_state.auth = True
                st.rerun()
            else: st.error("Hatalı!")
    st.stop()

st.title("⬛ FnekCRM | Operasyonel Yönetim")

t1, t2, t3 = st.tabs(["📁 PORTFÖY YÖNETİMİ", "👤 CRM", "🔥 FSBO"])

with t1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Yeni Portföy Kaydı")
        with st.form("p_full_form"):
            p_baslik = st.text_input("Mülk Başlığı*")
            
            col_a, col_b = st.columns(2)
            with col_a:
                p_ilce = st.selectbox("İlçe", ["Güzelbahçe", "Urla", "Buca", "Narlıdere"])
                p_islem = st.selectbox("İşlem Tipi", ["Satılık", "Kiralık", "Devren"])
                p_fiyat = st.number_input("Fiyat (TL)", min_value=0, step=1000)
            with col_b:
                p_mahalle = st.text_input("Mahalle")
                p_tip = st.selectbox("Mülk Tipi", ["Konut", "Ticari", "Arsa", "Villa"])
                p_m2 = st.number_input("Net m2", min_value=1, step=1)
            
            p_drive = st.text_input("Google Drive Link")
            p_soz = st.text_input("Sözleşme/Dosya Link")
            
            if st.form_submit_button("PORTFÖYÜ SİSTEME İŞLE"):
                if p_baslik:
                    # ANALİTİK VERİ YAPILANDIRMASI
                    payload = {
                        "baslik": str(p_baslik),
                        "ilce": str(p_ilce),
                        "mahalle": str(p_mahalle),
                        "fiyat": int(p_fiyat),
                        "m2": int(p_m2),
                        "birim_fiyat": round(float(p_fiyat/p_m2), 2) if p_m2 > 0 else 0,
                        "islem_tipi": str(p_islem),
                        "mulk_tipi": str(p_tip),
                        "drive_link": str(p_drive) if p_drive else None,
                        "sozlesme_link": str(p_soz) if p_soz else None
                    }
                    
                    try:
                        supabase.table("portfoy_v2").insert(payload).execute()
                        st.success("Portföy başarıyla envantere eklendi.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Veri Tipleri Hatası: {str(e)}")
                else:
                    st.warning("Mülk başlığı girmek zorunludur.")

    with c2:
        st.subheader("Güncel Envanter Verileri")
        res = supabase.table("portfoy_v2").select("*").order("eklenme_tarihi", desc=True).execute()
        if res.data:
            df = pd.DataFrame(res.data)
            # Analitik görünüm için sütunları düzenle
            st.dataframe(df[['baslik', 'ilce', 'fiyat', 'islem_tipi', 'mulk_tipi']], use_container_width=True)
