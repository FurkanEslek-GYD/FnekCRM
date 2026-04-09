import streamlit as st
from supabase import create_client
import pandas as pd

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
        with st.form("p_form_v7"):
            p_baslik = st.text_input("Mülk Başlığı*")
            p_fiyat = st.number_input("Fiyat (TL)", min_value=0)
            p_m2 = st.number_input("Net m2", min_value=1)
            p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren Satılık", "Devren Kiralık"])
            p_tip = st.selectbox("Tip", ["Konut", "Ticari", "Arsa"])
            p_drive = st.text_input("Drive Link (Opsiyonel)")
            p_soz = st.text_input("Sözleşme Link (Opsiyonel)")
            if st.form_submit_button("Sisteme İşle"):
                if p_baslik:
                    supabase.table("portfoy_yeni").insert({
                        "baslik": p_baslik, "ilce": ilce, "mahalle": mahalle, "fiyat": p_fiyat,
                        "m2": p_m2, "birim_fiyat": p_fiyat/p_m2 if p_m2 > 0 else 0, 
                        "islem_tipi": p_islem, "mulk_tipi": p_tip, 
                        "resim_link": p_drive if p_drive else None, 
                        "sozlesme_link": p_soz if p_soz else None
                    }).execute()
                    st.rerun()

    with c2:
        res_p = supabase.table("portfoy_yeni").select("*").execute()
        df_p = pd.DataFrame(res_p.data)
        if not df_p.empty:
            st.subheader("📊 Envanter")
            st.metric("Toplam Hacim", f"{df_p['fiyat'].sum():,.0f} TL")
            
            # Veri Tablosu
            st.dataframe(df_p[['baslik', 'ilce', 'mahalle', 'fiyat', 'islem_tipi']], use_container_width=True)
            
            # Detaylı İnceleme
            secili = st.selectbox("Detaylı Analiz:", df_p['baslik'].tolist())
            d = df_p[df_p['baslik'] == secili].iloc[0]
            
            st.markdown(f"### {d['baslik']}")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write(f"**Birim Fiyat:** {d['birim_fiyat']:,.0f} TL/m2")
                if d['resim_link']: st.link_button("📂 Drive Resimleri", d['resim_link'])
            with col_b:
                st.write(f"**Durum:** {d['islem_tipi']} / {d['mulk_tipi']}")
                if d['sozlesme_link']: st.link_button("📄 Sözleşmeyi Gör", d['sozlesme_link'])
        else:
            st.info("Henüz veri girişi yok.")

# --- TAB 2 & 3 (Stabil CRM ve FSBO) ---
with tab2:
    st.subheader("Müşteri Kaydı")
    # CRM kodları buraya (v3.6 ile aynı stabil yapı)
with tab3:
    st.subheader("FSBO Takip")
    # FSBO kodları buraya (v3.6 ile aynı stabil yapı)
