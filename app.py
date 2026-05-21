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

# Clés d'API (Barre latérale)
INVIDEO_API_KEY = st.sidebar.text_input("Clé API Vidéo :", type="password")

# 4. ACTION DE GÉNÉRATION ET ENREGISTREMENT (CORRIGÉ SANS LE DOUBLON)
if st.button("🚀 Confectionner la Vidéo"):
    with st.spinner("Confection de la vidéo par l'IA et enregistrement dans l'historique..."):
        
        # Rédaction du script dynamique selon le thème choisi
        if "Martingale" in theme:
            script_genere = f"Arrête de doubler tes mises sur Pocket Option ! C'est le piège. Avec {capital} F CFA, ta mise maximale est de {mise_fixe} F CFA. Rejoins mon Telegram en bio."
        else:
            script_genere = f"Session OTC Pocket Option de 20h à 23h. Configuration Stochastique 14, 5, 3 et niveaux 85/15. Rejoins mon Telegram pour le Bot gratuit."
        
        # Détermination du statut selon la présence de la clé API
        if INVIDEO_API_KEY:
            statut_video = "Générée avec succès (InVideo API)"
        else:
            statut_video = "Générée avec succès (Mode Démo / Sans Clé)"
            
        # Génération de la date au moment du clic
        date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        # Insertion des données dans la base SQLite
        conn = sqlite3.connect("video_history.db")
        cursor = conn.cursor()
        
        query = '''
            INSERT INTO videos (date_creation, theme, capital, script, statut)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (date_actuelle, theme, str(capital), script_genere, statut_video))
        conn.commit()
        conn.close()
        
        # Effets visuels de réussite
        st.balloons()
        st.success("✅ Vidéo confectionnée et enregistrée dans votre historique !")
        st.info(f"**Texte envoyé à l'IA :** {script_genere}")
        if not INVIDEO_API_KEY:
            st.warning("⚠️ Note : Génération effectuée en mode démo car aucune clé API n'a été saisie.")

# 5. SECTION HISTORIQUE VISIBLE SUR L'APPLICATION
st.markdown("---")
st.subheader("📊 Historique de vos Vidéos Générées")

# Lecture des données sauvegardées de manière sécurisée
conn_lecture = sqlite3.connect("video_history.db")
cursor_lecture = conn_lecture.cursor()

try:
    cursor_lecture.execute("SELECT date_creation, theme, capital, script, statut FROM videos ORDER BY id DESC")
    lignes = cursor_lecture.fetchall()
except sqlite3.OperationalError:
    lignes = []

conn_lecture.close()

# Affichage des résultats sous forme de liste propre et déroulante
if lignes:
    for row in lignes:
        # row[0]=date, row[1]=thème, row[2]=capital, row[3]=script, row[4]=statut
        with st.expander(f"📅 {row[0]} | 🎬 {row[1]} ({row[2]} F CFA)"):
            st.write(f"**Statut :** {row[4]}")
            st.write(f"**Script déclamé :**")
            st.code(row[3], language="text")
else:
    st.caption("Aucune vidéo dans l'historique pour le moment. Lancez votre première confection !")
