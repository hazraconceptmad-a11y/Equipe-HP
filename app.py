import streamlit as st
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURATION NY PEJY ---
st.set_page_config(page_title="HAZRAPHARMA", layout="wide")

# --- DATA INITIALIZATION (Simulated Database) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=[
        "Numéro", "Anarana", "Sokajy", "Nombre", "Prix Achat", "Prix Vente", "Péremption", "Lieu"
    ])
if 'ventes' not in st.session_state:
    st.session_state.ventes = []

# --- 1. PAGE D'ACCÈS (AUTHENTIFICATION) ---
def login_page():
    st.markdown("<h1 style='text-align: center;'>HP+ HAZRAPHARMA</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>OBJET : VENTE 2026</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.info("Mpikambana: Tantely, Eliane, Perline, Mbolasahy, Elia, Mamy")
        num_tel = st.text_input("Ampidiro ny Numéro-nao (Page Numéros):")
        access_code = st.text_input("Code fidirana:", type="password")
        
        if st.button("Hiditra"):
            # Ny numéro irery ihany no afaka mampiasa azy (eto dia ohatra ny fanamarinana)
            if access_code == "hp+2626":
                st.session_state.authenticated = True
                st.success("Tafiditra ianao!")
                st.rerun()
            else:
                st.error("Code diso na numéro tsy nahazo lalana.")

# --- 2. LOGIQUE AI PHARMACIEN ---
def ai_pharmacien(article_name):
    return f"**Torohevitra AI ho an'ny {article_name}:**\n- Dosage: 1 maraina sy hariva\n- Posologie: Aorian'ny sakafo\n- Contre-indication: Tsy azon'ny vehivavy bevohoka ampiasaina."

# --- 3. MAIN APPLICATION ---
def main_app():
    # Header
    st.sidebar.title("HP+ HAZRAPHARMA")
    st.sidebar.write(f"Daty: {datetime.now().strftime('%d/%m/%Y')}")
    st.sidebar.write(f"Ora: {datetime.now().strftime('%H:%M:%S')}")
    
    menu = ["Lisitry ny Articles", "Stocks", "Vente", "Analyse de Vente", "Communication", "Contacts"]
    choice = st.sidebar.selectbox("Fidio ny Pejy", menu)

    # --- PAGE: LISITRY NY ARTICLES ---
    if choice == "Lisitry ny Articles":
        st.header("📦 Lisitry ny Articles")
        tab1, tab2 = st.tabs(["Vue Globale", "Vue par Catégorie"])
        
        with tab1:
            search = st.text_input("Hikaroka article...")
            # Simulation calculation & AI
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("Article: Paracétamol | Prix: 500 Ar")
                if st.button("Hividy (OK)"): st.toast("Voavidy!")
            with col_b:
                st.info(ai_pharmacien("Paracétamol"))

    # --- PAGE: STOCKS ---
    elif choice == "Stocks":
        st.header("📊 Fitantanana ny Stock")
        sub_menu = st.radio("Sokajy", ["Stocks de Base", "Stocks Finaux", "Historique"], horizontal=True)
        
        if sub_menu == "Stocks de Base":
            st.subheader("Entana Vaovao")
            # Form ampidirana entana
            with st.expander("Hanampy Entana"):
                name = st.text_input("Anaran'ny article")
                cat = st.selectbox("Sokajy", ["Médicaments", "Parapharmacie", "Tests"])
                qty = st.number_input("Isany", min_value=1)
                p_achat = st.number_input("Prix d'achat")
                p_vente = st.number_input("Prix de vente")
                if st.button("Enregistrer"):
                    new_data = {"Numéro": len(st.session_state.inventory)+1, "Anarana": name, "Sokajy": cat, 
                                "Nombre": qty, "Prix Achat": p_achat, "Prix Vente": p_vente}
                    st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_data])], ignore_index=True)
                    st.success("Voatahiry!")
            
            st.dataframe(st.session_state.inventory)

    # --- PAGE: VENTE ---
    elif choice == "Vente":
        st.header("💰 Varotra isan'andro")
        st.date_input("Fidio ny daty")
        v_type = st.radio("Fizarana", ["Pré-Vente", "Vente Définitive"])
        
        if v_type == "Pré-Vente":
            st.warning("Eto no manao calcul ny commande alohan'ny hanamarinana azy.")
            # Tableau pré-vente logic eto...

    # --- PAGE: COMMUNICATION ---
    elif choice == "Communication":
        st.header("💬 Fifandraisana")
        msg_type = st.selectbox("Karazana hafatra", ["Message d'Urgence", "Filazana", "SMS"])
        user_msg = st.text_area("Soraty ny hafatra...")
        if st.button("Alefaso"):
            st.success(f"Hafatra voararay! (Nalefan'i {choice})")

# --- FIAROVANA NY DATY (Valable hatramin'ny 31 Dec 2026) ---
expiry_date = datetime(2026, 12, 31)
if datetime.now() > expiry_date:
    st.error("Tapitra ny fotoana fampiasana ity site ity (31 Dec 2026).")
else:
    if not st.session_state.authenticated:
        login_page()
    else:
        main_app()
