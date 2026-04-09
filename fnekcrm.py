import streamlit as st
from supabase import create_client
import pandas as pd

# --- 1. GÜVENLİK VE ŞİFRELEME (3003Locate) ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "3003Locate":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown("### 🔒 FnekCRM | Kurumsal Giriş")
        st.text_input("Yönetici Şifresi", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown("### 🔒 FnekCRM | Kurumsal Giriş")
        st.text_input("Yönetici Şifresi", type="password", on_change=password_entered, key="password")
        st.error("❌ Hatalı Şifre!")
        return False
    else:
        return True

if not check_password():
    st.stop()

# --- 2. BAĞLANTI AYARLARI ---
URL = "https://kzeklqalcuvgilrhomvs.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imt6ZWtscWFsY3V2Z2lscmhvbXZzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU3MzE2NzQsImV4cCI6MjA5MTMwNzY3NH0.D0M1DtB1Qhx2fz175y96GTx9nHzfr8TR5dOveHnI8r0"

try:
    supabase = create_client(URL, KEY)
except:
    st.error("Veritabanı bağlantısı kurulamadı.")

# İzmir Veri Seti
izmir_data = {
    "Güzelbahçe": ["Yalı", "Çelebi", "Yelki", "Siteler", "Maltepe", "Atatürk", "Kahramandere"],
    "Urla": ["İskele", "Zeytinalanı", "Şirinkent", "Yenikale", "Altıntaş", "Kalabak", "Güvendik"],
    "Buca": ["Adatepe", "Safir (Yıldız)", "Yiğitler", "Şirinyer", "Dumlupınar", "Buca Koop"],
    "Karşıyaka": ["Mavişehir", "Bostanlı", "Atakent", "Bahçelievler", "Aksoy"],
    "Konak": ["Alsancak", "Göztepe", "Güzelyalı", "Hatay", "Kültür"],
    "Narlıdere": ["Yenikale", "Sahilevleri", "Huzur", "Limanreis", "Çatalkaya"]
}

st.set_page_config(page_title="FnekCRM Executive", layout="wide")

# UI Style
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #1a1c23; border-radius: 5px; color: white; margin-right: 5px; }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("⬛ FnekCRM | Operasyonel Verimlilik")

tab1, tab2, tab3 = st.tabs(["📁 PORTFÖYLER", "👤 CRM (MÜŞTERİ)", "🔥 FSBO TAKİP"])

# --- TAB 1: PORTFÖY YÖNETİMİ ---
with tab1:
    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Portföy Kayıt")
        ilce_p = st.selectbox("İlçe", list(izmir_data.keys()))
        mahalle_p = st.selectbox("Mahalle", izmir_data[ilce_p])
        with st.form("p_form_v5"):
            p_baslik = st.text_input("Mülk Adı (Zorunlu)*")
            col_x, col_y = st.columns(2)
            with col_x:
                p_islem = st.selectbox("İşlem Tipi", ["Satılık", "Kiralık", "Devren Satılık", "Devren Kiralık"])
            with col_y:
                p_tip = st.selectbox("Mülk Tipi", ["Konut", "Ticari", "Arsa", "Turistik"])
            
            p_fiyat = st.number_input("Toplam Fiyat (TL)", min_value=0)
            p_m2 = st.number_input("Net Alan (m²)", min_value=1)
            
            st.markdown("---")
            st.caption("Aşağıdaki alanları daha sonra da ekleyebilirsiniz:")
            p_drive = st.text_input("Drive Resim Linki (Opsiyonel)", placeholder="http://...")
            p_sozlesme = st.text_input("Sözleşme Linki (Opsiyonel)", placeholder="http://...")
            
            if st.form_submit_button("Portföyü Kilitle"):
                if p_baslik:
                    birim_f = p_fiyat / p_m2
                    supabase.table("portfoy_yeni").insert({
                        "baslik": p_baslik, "ilce": ilce_p, "mahalle": mahalle_p,
                        "fiyat": p_fiyat, "m2": p_m2, "birim_fiyat": birim_f,
                        "islem_tipi": p_islem, "mulk_tipi": p_tip, 
                        "resim_link": p_drive if p_drive else None, 
                        "sozlesme_link": p_sozlesme if p_sozlesme else None
                    }).execute()
                    st.success("Kaydedildi.")
                    st.rerun()
                else:
                    st.error("Lütfen mülk adını giriniz.")

    with c2:
        st.subheader("Envanter")
        data_p = supabase.table("portfoy_yeni").select("*").order("eklenme_tarihi", desc=True).execute()
        df_p = pd.DataFrame(data_p.data)
        if not df_p.empty:
            st.dataframe(df_p[['baslik', 'ilce', 'fiyat', 'islem_tipi']], use_container_width=True)
            secili = st.selectbox("Detay Analizi:", df_p['baslik'].tolist())
            d = df_p[df_p['baslik'] == secili].iloc[0]
            
            sc1, sc2 = st.columns(2)
            with sc1:
                if d['resim_link']: 
                    st.link_button("📂 Resimleri Aç", d['resim_link'])
                else: 
                    st.button("🖼️ Resim Henüz Yok", disabled=True)
            with sc2:
                if d['sozlesme_link']: 
                    st.link_button("📄 Sözleşmeyi Gör", d['sozlesme_link'])
                else: 
                    st.button("📑 Sözleşme Henüz Yok", disabled=True)
        else:
            st.info("Liste boş.")
