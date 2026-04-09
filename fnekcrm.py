# --- TAB 1: PORTFÖY (GÜNCELLENMİŞ v2) ---
with t1:
    c1, c2 = st.columns([1, 2])
    with c1:
        with st.form("p_form_v2"):
            st.subheader("Yeni Kayıt")
            p_baslik = st.text_input("Mülk Başlığı*")
            p_fiyat = st.number_input("Fiyat", min_value=0)
            p_m2 = st.number_input("m2", min_value=1)
            p_islem = st.selectbox("İşlem", ["Satılık", "Kiralık", "Devren"])
            p_ilce = st.selectbox("İlçe", ["Güzelbahçe", "Urla", "Buca", "Narlıdere"])
            
            if st.form_submit_button("KAYDET"):
                if p_baslik:
                    # Sadece SQL'de oluşturduğumuz kesin sütunları gönderiyoruz
                    data_p = {
                        "baslik": p_baslik,
                        "fiyat": float(p_fiyat),
                        "m2": float(p_m2),
                        "birim_fiyat": float(p_fiyat/p_m2),
                        "islem_tipi": p_islem,
                        "ilce": p_ilce
                    }
                    # Tablo ismini v2 olarak güncelledik
                    supabase.table("portfoy_v2").insert(data_p).execute()
                    st.success("Kaydedildi!")
                    st.rerun()

    with c2:
        try:
            res_p = supabase.table("portfoy_v2").select("*").execute()
            if res_p.data:
                st.dataframe(pd.DataFrame(res_p.data)[['baslik', 'fiyat', 'islem_tipi', 'ilce']], use_container_width=True)
        except:
            st.info("Veri bekleniyor...")
