import streamlit as st
import sqlite3
from datetime import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Base44 IA Video Factory", page_icon="🎬", layout="centered")

# 2. INITIALISATION DE LA BASE DE DONNÉES LOCALES (SQLite)
def init_db():
    conn = sqlite3.connect("video_history.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_creation TEXT,
            theme TEXT,
            capital TEXT,
            script TEXT,
            statut TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Appel de la fonction de création de table
init_db()

# 3. INTERFACE UTILISATEUR
st.title("🎬 Usine à Vidéos TikTok Automatisée")
st.write("Générez vos vidéos d'affiliation en un clic et suivez votre historique de production.")

# Formulaire de configuration
theme = st.selectbox(
    "Thème de la campagne :",
    ["Piège de la Martingale", "Stratégie Stochastique 14-5-3", "Session Flash 20h-23h"]
)
capital = st.number_input("Capital affiché (F CFA) :", value=260000)
mise_fixe = int(capital * 0.02)

# 4. GESTION DE L'ÉTAT ET ACTION DE GÉNÉRATION
if "script_genere" not in st.session_state:
    st.session_state.script_genere = ""
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# TOUT CE BLOC DOIT RESTER INDENTÉ DANS LE IF DU BOUTON
if st.button("🚀 Confectionner la Vidéo"):
    with st.spinner("Confection de la vidéo par l'IA et enregistrement dans l'historique..."):
        # 1. Création des variables locales
        if "Martingale" in theme:
            script_final = f"Arrête de doubler tes mises sur Pocket Option ! C'est le piège. Avec {capital} F CFA, ta mise maximale est de {mise_fixe} F CFA. Rejoins mon Telegram en bio."
        else:
            script_final = f"Session OTC Pocket Option de 20h à 23h. Configuration Stochastique 14, 5, 3 et niveaux 85/15. Rejoins mon Telegram pour le Bot gratuit."

        st.session_state.script_genere = script_final
        statut_video = "Générée avec succès"
        date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")

        # 2. Connexion et écriture immédiate (strictement indenté dans le bouton)
        conn = sqlite3.connect("video_history.db")
        cursor = conn.cursor()
        query = '''
            INSERT INTO videos (date_creation, theme, capital, script, statut)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (date_actuelle, theme, str(capital), script_final, statut_video))
        conn.commit()
        conn.close()

        # 3. Activation du message de succès et rechargement
        st.session_state.show_success = True
        st.rerun()

# Affichage des messages en sortie d'action (hors du bouton)
if st.session_state.get("show_success", False):
    st.balloons()
    st.success("✅ Vidéo confectionnée et enregistrée dans votre historique !")
    st.info(f"**Texte envoyé à l'IA :** {st.session_state.script_genere}")
    st.session_state.show_success = False

# 5. SECTION HISTORIQUE VISIBLE SUR L'APPLICATION
st.markdown("---")
st.subheader("📊 Historique de vos Vidéos Générées")

# Lecture des données sauvegardées
conn_lecture = sqlite3.connect("video_history.db")
cursor_lecture = conn_lecture.cursor()
try:
    cursor_lecture.execute("SELECT date_creation, theme, capital, script, statut FROM videos ORDER BY id DESC")
    lignes = cursor_lecture.fetchall()
except sqlite3.OperationalError:
    lignes = []
conn_lecture.close()

# Affichage des résultats corrigé avec les bons index du tuple SQL
if lignes:
    for row in lignes:
        with st.expander(f"📅 {row[0]} | 🎬 {row[1]} ({row[2]} F CFA)"):
            st.write(f"**Statut :** {row[4]}")
            st.write(f"**Script déclamé :**")
            st.code(row[3], language="text")
else:
    st.caption("Aucune vidéo dans l'historique pour le moment. Lancez votre première confection !")
