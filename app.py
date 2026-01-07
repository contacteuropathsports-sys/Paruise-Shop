import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import urllib.parse
import random
import plotly.express as px
import plotly.graph_objects as go

# --- 1. CONFIGURATION & AMBIANCE ---
st.set_page_config(page_title="Paruise Shop - L'Expérience", page_icon="👑", layout="wide")

# INFO BOUTIQUE
SHOP_NAME = "Paruise Shop"
SHOP_PHONE = "22893991499"

# --- 2. STYLE "DARK LUXE" (SOMMEIL & OR) ---
st.markdown("""
<style>
    /* FOND PRINCIPAL : NOIR PROFOND */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    
    /* SIDEBAR : BORDEAUX SOMBRE */
    [data-testid="stSidebar"] {
        background-color: #4A0E19;
    }
    [data-testid="stSidebar"] * {
        color: #F9F9F9 !important;
    }

    /* TITRES : OR ET BLANC */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 600;
    }
    h1 span, h2 span, h3 span { color: #D4AF37 !important; }

    /* BOUTONS D'ACTION (Bordeaux & Or) */
    .stButton>button {
        background: linear-gradient(45deg, #800020, #5a0016);
        color: white; 
        border: 1px solid #D4AF37; 
        border-radius: 12px;
        height: 55px; 
        font-size: 18px; 
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        transition: transform 0.2s;
    }
    .stButton>button:hover { 
        transform: scale(1.02); 
        border-color: white;
    }

    /* LES ÉTAPES (Step 1, 2, 3) - MODE SOMBRE */
    .step-box {
        background-color: #1E1E1E; /* Gris foncé */
        padding: 20px; 
        border-radius: 15px;
        border-left: 6px solid #D4AF37; /* Or */
        box-shadow: 0 4px 10px rgba(0,0,0,0.3); 
        margin-bottom: 15px;
        color: white;
    }
    .step-title { 
        font-size: 20px; 
        font-weight: bold; 
        color: #D4AF37; /* Or */
        margin-bottom: 10px; 
    }

    /* ALERTES (Adaptées au sombre) */
    .success-msg { 
        background-color: #1B5E20; /* Vert foncé */
        color: #FFFFFF; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #4CAF50; 
        text-align: center; 
        font-size: 18px;
    }
    
    /* CHAMPS DE SAISIE (Fond Clair pour lisibilité maximale) */
    .stTextInput input, .stNumberInput input, .stSelectbox div, .stDateInput input, .stTextArea textarea {
        background-color: #F0F2F6 !important;
        color: #000000 !important;
        border-radius: 8px;
        border: 1px solid #555;
    }
    
    /* Texte dans les listes déroulantes */
    div[data-baseweb="select"] > div {
        background-color: #F0F2F6 !important;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONNEXION ---
@st.cache_resource
def get_database():
    try:
        scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]
        import os
        if not os.path.exists('credentials.json'): return None
        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)
        return client.open("Data manager Paruise Shop")
    except: return None

sh = get_database()
if not sh: st.stop()

def load_data(sheet):
    try:
        ws = sh.worksheet(sheet)
        d = ws.get_all_values()
        if len(d) < 2: return pd.DataFrame()
        return pd.DataFrame(d[1:], columns=d[0]).loc[:, [h for h in d[0] if h.strip() != ""]]
    except: return pd.DataFrame()

# --- 4. FONCTIONS MAGIQUES ---
def clean_num(val):
    try: return float(str(val).replace("FCFA","").replace(" ","").replace(",",".").strip())
    except: return 0.0

def whatsapp_link(phone, msg):
    encoded = urllib.parse.quote(msg)
    if pd.isna(phone) or str(phone).strip() == "": return f"https://wa.me/?text={encoded}"
    clean = str(phone).replace(" ", "").replace("+", "").replace(".", "").split(".")[0]
    return f"https://wa.me/{clean}?text={encoded}"

# --- 5. NAVIGATION (ORDRE VALIDÉ) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3163/3163212.png", width=100)
st.sidebar.markdown("### PARUISE SHOP")
st.sidebar.caption("L'Art de gérer son Empire")

menu = st.sidebar.radio("NAVIGUER", [
    "🛒 Nouvelle Vente (Caisse)",
    "📦 Stock & Pépites",
    "💌 Clients & Amour",
    "📢 Marketing Impactant",
    "💸 Dépenses (Sorties)",
    "📈 Évolution du Budget"
])

# =============================================================================
# 1. CAISSE (FLUX CONTINU & ÉMOTIONNEL)
# =============================================================================
if menu == "🛒 Nouvelle Vente (Caisse)":
    st.title("🛍️ Encaisser avec le Sourire")
    st.markdown("C'est ici que la magie opère. Transformons une visiteuse en cliente fidèle.")
    
    df_prod = load_data("PRODUITS")
    df_cli = load_data("CLIENTS")
    
    # --- ÉTAPE 1 : QUI ? ---
    st.markdown("""<div class="step-box"><div class="step-title">1️⃣ Qui est notre Reine du jour ?</div>""", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        if not df_cli.empty: cli_list = ["-- Nouvelle Cliente --"] + df_cli["Nom_Client"].tolist()
        else: cli_list = ["-- Nouvelle Cliente --"]
        client_nom = st.selectbox("Sélectionne la cliente", cli_list, label_visibility="collapsed")
    
    final_client, final_tel = "", ""
    if client_nom == "-- Nouvelle Cliente --":
        with st.expander("✨ Créer une nouvelle fiche (C'est rapide !)", expanded=True):
            n_nom = st.text_input("Son petit Nom")
            n_tel = st.text_input("Son WhatsApp")
            col_a, col_b = st.columns(2)
            n_quartier = col_a.text_input("Quartier")
            n_source = col_b.selectbox("Comment nous a-t-elle connus ?", ["Passage devant boutique", "TikTok", "Facebook", "Recommandation Amie"])
            if st.button("💾 Enregistrer la Reine"):
                sh.worksheet("CLIENTS").append_row([n_nom, n_tel, n_quartier, n_source, ""])
                st.success(f"Bienvenue à {n_nom} dans la famille Paruise !")
                st.rerun()
    else:
        final_client = client_nom
        if not df_cli.empty:
            infos = df_cli[df_cli["Nom_Client"]==final_client]
            if not infos.empty: final_tel = str(infos.iloc[0]["Telephone"])
    st.markdown('</div>', unsafe_allow_html=True)

    # --- ÉTAPE 2 : QUOI ? ---
    st.markdown("""<div class="step-box"><div class="step-title">2️⃣ Son Coup de Cœur</div>""", unsafe_allow_html=True)
    if df_prod.empty:
        st.error("Ton stock est vide ma belle. Va vite ajouter des articles !")
        st.stop()
        
    c3, c4 = st.columns(2)
    with c3:
        if "Nom_Article" in df_prod.columns:
            df_prod["Display"] = df_prod["Nom_Article"]
            choix = st.selectbox("Article choisi", df_prod["Display"])
            row = df_prod[df_prod["Display"]==choix].iloc[0]
            
            p_vente = clean_num(row.get("Prix_Vente", 0))
            p_achat = clean_num(row.get("Prix_Achat", 0))
            st.info(f"🏷️ Prix Étiquette : **{p_vente:,.0f} FCFA**")
        else: st.error("Erreur Stock"); st.stop()
        
    with c4:
        qte = st.number_input("Quantité", 1, 20, 1)
        prix_final = st.number_input("PRIX FINAL (Si tu as fait une remise)", value=int(p_vente), step=500)
    
    # --- ÉTAPE 3 : L'ARGENT ---
    st.markdown("""</div><div class="step-box"><div class="step-title">3️⃣ L'Encaissement</div>""", unsafe_allow_html=True)
    pay = st.selectbox("Moyen de paiement", ["Espèces 💵", "Flooz 📱", "TMoney 🟡", "Virement 🏦"])
    
    total = prix_final * qte
    benefice = (prix_final - p_achat) * qte
    
    # Couleur Or pour être visible sur le noir
    st.markdown(f"<h2 style='text-align:center; color:#D4AF37'>TOTAL À PAYER : {total:,.0f} FCFA</h2>", unsafe_allow_html=True)
    
    if st.button("✨ VALIDER LA VENTE ET FAIRE BRILLER ✨"):
        if final_client:
            date = datetime.now().strftime("%d/%m/%Y")
            sh.worksheet("VENTES").append_row([date, final_client, row["Nom_Article"], prix_final, qte, total, pay])
            
            st.balloons()
            st.markdown(f"<div class='success-msg'>👏 Bravo ! Encore une cliente satisfaite.<br>Tu as gagné <b>{benefice:,.0f} F</b> de bénéfice net sur cette vente !</div>", unsafe_allow_html=True)
            
            # --- LE REÇU ÉMOTIONNEL ---
            prenom = str(final_client).split(' ')[0]
            
            msg1 = f"""Coucou {prenom} ! C'est Paruise Shop 👑
Merci infiniment pour ta confiance.

🛍️ *Ton shopping :* {row['Nom_Article']}
💎 *Total :* {total:,.0f} FCFA

Tu vas être rayonnante avec ça ! Envoie-nous une photo quand tu le portes, on adore te voir briller. ✨"""

            msg2 = f"""Hello ma belle {prenom} ! 👋
C'est validé chez Paruise Shop !

👗 *Article :* {row['Nom_Article']}
💸 *Montant :* {total:,.0f} FCFA

Merci de soutenir mon business. Prends soin de toi et à très vite ! 😘"""
            
            final_msg = random.choice([msg1, msg2])
            link = whatsapp_link(final_tel, final_msg)
            
            st.markdown(f"<br><a href='{link}' target='_blank'><button style='width:100%; background-color:#25D366; border:none; height:50px; border-radius:10px; color:white; font-weight:bold; font-size:18px;'>📲 ENVOYER LE REÇU WHATSAPP</button></a>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ Oups ! Tu as oublié de choisir la cliente.")
    st.markdown('</div>', unsafe_allow_html=True)

# =============================================================================
# 2. STOCK
# =============================================================================
elif menu == "📦 Stock & Pépites":
    st.title("📦 Tes Trésors (Stock)")
    
    with st.expander("➕ REÇEVOIR UN NOUVEL ARRIVAGE", expanded=False):
        with st.form("add_stk"):
            c1, c2 = st.columns(2)
            n_nom = c1.text_input("Nom de la pépite")
            n_cat = c2.selectbox("Catégorie", ["Robe", "Ensemble", "Sac", "Chaussure", "Accessoire"])
            c3, c4, c5 = st.columns(3)
            pa = c3.number_input("Prix Achat", step=500)
            pv = c4.number_input("Prix Vente", step=500)
            qty = c5.number_input("Quantité", min_value=1)
            
            if st.form_submit_button("Enregistrer"):
                sh.worksheet("PRODUITS").append_row([n_nom, n_cat, pa, pv, "", qty])
                st.success("C'est en rayon !")
                st.rerun()

    df_p = load_data("PRODUITS")
    if not df_p.empty:
        df_p["Stock_Actuel"] = pd.to_numeric(df_p["Stock_Actuel"], errors='coerce').fillna(0)
        
        # Design Tableau
        st.dataframe(df_p, use_container_width=True)
        
        low = df_p[df_p["Stock_Actuel"] < 3]
        if not low.empty:
            st.warning(f"⚠️ Attention ma chérie, {len(low)} articles sont bientôt en rupture !")
            st.dataframe(low[["Nom_Article", "Stock_Actuel"]])

# =============================================================================
# 3. CLIENTS
# =============================================================================
elif menu == "💌 Clients & Amour":
    st.title("💌 Chouchoute tes Clientes")
    df_v = load_data("VENTES")
    df_c = load_data("CLIENTS")
    
    if not df_v.empty:
        col_t = "Total" if "Total" in df_v.columns else df_v.columns[5]
        df_v["Val"] = df_v[col_t].apply(clean_num)
        top = df_v.groupby(df_v.columns[1])["Val"].sum().sort_values(ascending=False).head(3)
        
        st.markdown("### 👑 Le Podium des Reines (Top 3)")
        for cli, val in top.items():
            st.info(f"🏆 {cli} : {val:,.0f} FCFA dépensés chez toi !")
            
        st.divider()
        st.markdown("### 💌 Envoyer de l'amour")
        dest = st.selectbox("Choisir une cliente", df_c["Nom_Client"].tolist() if not df_c.empty else [])
        if dest:
            tel = df_c[df_c["Nom_Client"]==dest].iloc[0]["Telephone"]
            prenom = str(dest).split(' ')[0]
            msg_type = st.radio("Occasion :", ["Merci Spécial", "Relance Douce", "Anniversaire"])
            
            if msg_type == "Merci Spécial": txt = f"Coucou {prenom} ! ❤️ Merci d'être une cliente si fidèle. Passe me voir pour un petit cadeau !"
            elif msg_type == "Relance Douce": txt = f"Toc toc {prenom} ! 👀 J'ai reçu des nouveautés qui t'iraient à merveille. Viens jeter un œil !"
            else: txt = f"Joyeux Anniversaire {prenom} ! 🎂🥳 Passe récupérer ton cadeau à la boutique (-20% aujourd'hui) !"
            
            lnk = whatsapp_link(tel, txt)
            st.markdown(f"<a href='{lnk}' target='_blank'><button style='background-color:#25D366; color:white; border:none; padding:10px; border-radius:5px;'>📲 Envoyer sur WhatsApp</button></a>", unsafe_allow_html=True)

# =============================================================================
# 4. MARKETING
# =============================================================================
elif menu == "📢 Marketing Impactant":
    st.title("📢 Fais du Bruit !")
    
    tab1, tab2 = st.tabs(["📘 Facebook", "🎵 TikTok"])
    prod = st.text_input("Produit vedette", "Cette Robe en Soie")
    
    with tab1:
        st.markdown("### Storytelling Facebook")
        fb_txt = f"""🤫 JE NE DEVRAIS PAS VOUS MONTRER ÇA...

Quand j'ai ouvert le carton et vu {prod}... je n'ai pas pu résister.
La coupe ? Parfaite. La matière ? Une caresse.

👑 Mes Reines, attention, je n'en ai que quelques pièces.
📍 Paruise Shop (Face Station Sanol)
👇 Cliquez vite ici : https://wa.me/{SHOP_PHONE}"""
        st.text_area("Copier :", fb_txt, height=250)

    with tab2:
        st.markdown("### Titres TikTok")
        st.info("🎵 Son : Afro tendance douce.")
        st.code("Arrête de scroller si tu veux être la plus classe.")
        st.code("#Lome #TogoFashion #ParuiseShop #Chic228 #OOTD")

# =============================================================================
# 5. DÉPENSES
# =============================================================================
elif menu == "💸 Dépenses (Sorties)":
    st.title("💸 Où va l'argent ?")
    with st.form("dep"):
        d_date = st.date_input("Date", datetime.now())
        d_cat = st.selectbox("Motif", ["Marchandise", "Loyer", "Factures", "Transport", "Perso", "Épargne"])
        d_montant = st.number_input("Montant", step=500)
        d_desc = st.text_input("Détail")
        if st.form_submit_button("Noter la dépense"):
            try: sh.worksheet("DEPENSES").append_row([d_date.strftime("%d/%m/%Y"), d_cat, d_montant, d_desc])
            except: st.error("Crée l'onglet DEPENSES !")
            st.success("C'est noté. On surveille le budget !")

# =============================================================================
# 6. BUDGET
# =============================================================================
elif menu == "📈 Évolution du Budget":
    st.title("📈 La Vie de ton Argent")
    df_v = load_data("VENTES")
    df_d = load_data("DEPENSES")
    
    data_points = []
    
    if not df_v.empty:
        col_t = "Total" if "Total" in df_v.columns else df_v.columns[5]
        for _, row in df_v.iterrows():
            try:
                d = datetime.strptime(row.iloc[0], "%d/%m/%Y")
                montant = clean_num(row[col_t])
                data_points.append({"Date": d, "Montant": montant})
            except: pass
            
    if not df_d.empty:
        col_m = "Montant" if "Montant" in df_d.columns else df_d.columns[2]
        for _, row in df_d.iterrows():
            try:
                d = datetime.strptime(row.iloc[0], "%d/%m/%Y")
                montant = clean_num(row[col_m])
                data_points.append({"Date": d, "Montant": -montant})
            except: pass
            
    if data_points:
        df_chart = pd.DataFrame(data_points).sort_values("Date")
        df_chart["Caisse"] = df_chart["Montant"].cumsum()
        
        fig = px.area(df_chart, x="Date", y="Caisse", title="Trésorerie (Cash Réel)", color_discrete_sequence=['#D4AF37'])
        # Graphique adapté au mode sombre
        fig.update_layout(
            plot_bgcolor="#1E1E1E", 
            paper_bgcolor="#0E1117", 
            font_color="white",
            xaxis_showgrid=False, 
            yaxis_gridcolor='#333'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"<h3 style='text-align:center'>Solde actuel : <span style='color:#D4AF37'>{df_chart.iloc[-1]['Caisse']:,.0f} FCFA</span></h3>", unsafe_allow_html=True)
    else:
        st.info("Pas encore assez de données.")
