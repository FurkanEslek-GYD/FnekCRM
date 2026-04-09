import streamlit as st
from supabase import create_client
import pandas as pd

# --- GÜVENLİK (3003Locate) ---
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

# --- BAĞLANTI ---
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
st.title("⬛ FnekCRM | Kurumsal Yönetim")

tab1, tab2, tab3 = st.tabs(["📁 PORTFÖYLER", "👤 CRM", "🔥 FSBO"])

# --- TAB 1: PORTFÖY ---
with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Yeni Portföy")
        ilce = st.selectbox("İlçe", list(izmir_data.keys()), key="p_ilce")
        mahalle = st.selectbox("Mahalle", izmir_data[ilce], key="p_mah")
        with st.form("p_form"):
            p_baslik = st.text_input("Mülk Adı*")
            p_fiyat = st.number_input("Fiyat (TL)", min_value=0)
            p_m2 = st.number_input("m2", min_value=1)
            p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren Satılık"])
            p_tip = st.selectbox("Tip", ["Konut", "Ticari", "Arsa"])
            p_drive = st.text_input("Drive Link")
            p_soz = st.text_input("Sözleşme Link")
            if st.form_submit_button("Kaydet"):
                if p_baslik:
                    supabase.table("portfoy_yeni").insert({
                        "baslik": p_baslik, "ilce": ilce, "mahalle": mahalle, "fiyat": p_fiyat,
                        "m2": p_m2, "birim_fiyat": p_fiyat/p_m2, "islem_tipi": p_islem, "mulk_tipi": p_tip,
                        "resim_link": p_drive if p_drive else None, "sozlesme_link": p_soz if p_soz else None
                    }).execute()
                    st.rerun()
    with c2:
        try:
            df_p = pd.DataFrame(supabase.table("portfoy_yeni").select("*").execute().data)
            if not df_p.empty:
                st.dataframe(df_p[['baslik', 'ilce', 'fiyat', 'islem_tipi']], use_container_width=True)
        except: st.info("Veri bekleniyor...")

# --- TAB 2: CRM ---
with tab2:
    c3, c4 = st.columns([1, 2])
    with c3:
        st.subheader("Müşteri Kaydı")
        with st.form("m_form"):
            m_ad = st.text_input("Ad Soyad")
            m_tel = st.text_input("Telefon")
            m_rol = st.selectbox("Rol", ["Alıcı", "Satıcı"])
            m_but = st.text_input("Bütçe")
            if st.form_submit_button("Müşteriyi Kaydet"):
                supabase.table("musteriler").insert({"ad_soyad": m_ad, "telefon": m_tel, "rol": m_rol, "butce_beklenti": m_but}).execute()
                st.rerun()
    with c4:
        try:
            df_m = pd.DataFrame(supabase.table("musteriler").select("*").execute().data)
            if not df_m.empty: st.dataframe(df_m[['ad_soyad', 'telefon', 'rol']], use_container_width=True)
        except: st.info("Rehber boş.")

# --- TAB 3: FSBO ---
with tab3:
    c5, c6 = st.columns([1, 2])
    with c5:
        st.subheader("FSBO Takip")
        with st.form("f_form"):
            f_link = st.text_input("İlan Linki")
            f_ad = st.text_input("Mal Sahibi")
            f_tel = st.text_input("Telefon")
            f_durum = st.selectbox("Durum", ["Potansiyel", "Randevu", "Portföy"])
            if st.form_submit_button("FSBO Kilitle"):
                supabase.table("fsbo_takip").insert({"ilan_link": f_link, "mal_sahibi_ad": f_ad, "mal_sahibi_tel": f_tel, "durum": f_durum}).execute()
                st.rerun()
    with c6:
        try:
            df_f = pd.DataFrame(supabase.table("fsbo_takip").select("*").execute().data)
            if not df_f.empty: st.dataframe(df_f[['mal_sahibi_ad', 'mal_sahibi_tel', 'durum']], use_container_width=True)
        except: st.info("FSBO listesi boş.")
