import streamlit as st
import sqlite3
from datetime import datetime

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Base44 IA Video Factory", page_icon="🎬", layout="centered")

# 2. FONCTIONS DE LA BASE DE DONNÉES (SQLITE)
def init_db():
    """Initialise la base de données locale si elle n'existe pas."""
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

def sauvegarder_video(date_creation, theme, capital, script, statut):
    """Enregistre de manière sécurisée une vidéo dans l'historique."""
    conn = sqlite3.connect("video_history.db")
    cursor = conn.cursor()
    query = '''
        INSERT INTO videos (date_creation, theme, capital, script, statut)
        VALUES (?, ?, ?, ?, ?)
    '''
    cursor.execute(query, (date_creation, theme, str(capital), script, statut))
    conn.commit()
    conn.close()

def extraire_historique():
    """Récupère toutes les vidéos enregistrées."""
    conn = sqlite3.connect("video_history.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT date_creation, theme, capital, script, statut FROM videos ORDER BY id DESC")
        lignes = cursor.fetchall()
    except sqlite3.OperationalError:
        lignes = []
    conn.close()
    return lignes

# Initialisation au démarrage
init_db()

# 3. INTERFACE UTILISATEUR
st.title("🎬 Usine à Vidéos TikTok Automatisée")
st.write("Générez vos vidéos d'affiliation en un clic et suivez votre historique de production.")

# Formulaire de configuration
theme_choisi = st.selectbox(
    "Thème de la campagne :",
    ["Piège de la Martingale", "Stratégie Stochastique 14-5-3", "Session Flash 20h-23h"]
)
capital_saisi = st.number_input("Capital affiché (F CFA) :", value=260000)
mise_fixe = int(capital_saisi * 0.02)

# 4. GESTION DE L'ÉTAT (SESSION STATE)
if "script_genere" not in st.session_state:
    st.session_state.script_genere = ""
if "show_success" not in st.session_state:
    st.session_state.show_success = False

# 5. ACTION DE GÉNÉRATION
if st.button("🚀 Confectionner la Vidéo"):
    with st.spinner("Confection de la vidéo par l'IA et enregistrement dans l'historique..."):
        
        # Rédaction du script dynamique selon le thème choisi
        if "Martingale" in theme_choisi:
            script_final = f"Arrête de doubler tes mises sur Pocket Option ! C'est le piège. Avec {capital_saisi} F CFA, ta mise maximale est de {mise_fixe} F CFA. Rejoins mon Telegram en bio."
        else:
            script_final = f"Session OTC Pocket Option de 20h à 23h. Configuration Stochastique 14, 5, 3 et niveaux 85/15. Rejoins mon Telegram pour le Bot gratuit."

        # Préparation des autres variables
        statut_video = "Générée avec succès"
        date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Sauvegarde en Session State pour l'affichage ultérieur
        st.session_state.script_genere = script_final

        # Appel de la fonction de sauvegarde (Totalement isolée du scope global)
        sauvegarder_video(date_actuelle, theme_choisi, capital_saisi, script_final, statut_video)

        # Déclenchement de l'affichage de succès et rechargement
        st.session_state.show_success = True
        st.rerun()

# Affichage des messages de succès (En dehors du bouton)
if st.session_state.get("show_success", False):
    st.balloons()
    st.success("✅ Vidéo confectionnée et enregistrée dans votre historique !")
    st.info(f"**Texte envoyé à l'IA :** {st.session_state.script_genere}")
    st.session_state.show_success = False

# 6. SECTION HISTORIQUE VISIBLE SUR L'APPLICATION
st.markdown("---")
st.subheader("📊 Historique de vos Vidéos Générées")

lignes_historique = extraire_historique()

# Affichage des résultats avec les index de colonnes SQL corrigés
if lignes_historique:
    for row in lignes_historique:
        # row[0]: date, row[1]: theme, row[2]: capital, row[3]: script, row[4]: statut
        with st.expander(f"📅 {row[0]} | 🎬 {row[1]} ({row[2]} F CFA)"):
            st.write(f"**Statut :** {row[4]}")
            st.write(f"**Script déclamé :**")
            st.code(row[3], language="text")
else:
    st.caption("Aucune vidéo dans l'historique pour le moment. Lancez votre première confection !")
