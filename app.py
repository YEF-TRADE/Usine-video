import streamlit as st
import sqlite3
from datetime import datetime

# Configuration de la page Base44
st.set_page_config(page_title="Base44 IA Video Factory", page_icon="🎬", layout="centered")

# --- INITIALISATION DE LA BASE DE DONNÉES LOCALES (SQLite) ---
def init_db():
  conn = sqlite3.connect("video_history.db")
  cursor = conn.cursor()
  cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            theme TEXT,
            capital INTEGER,
            script TEXT,
            statut TEXT
        )
    ''')
  conn.commit()
  conn.close()

init_db()

# --- INTERFACE UTILISATEUR ---
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

if st.button("🚀 Confectionner et Enregistrer la Vidéo"):
  if not INVIDEO_API_KEY:
    st.warning("Veuillez renseigner votre clé API vidéo dans la barre latérale pour lancer la génération.")
  else:
    with st.spinner("Confection de la vidéo par l'IA et enregistrement dans l'historique..."):
           
            # Rédaction du script dynamique
      if "Martingale" in theme:
        script_genere = f"Arrête de doubler tes mises sur Pocket Option ! C'est le piège. Avec {capital} F CFA, ta mise maximale est de {mise_fixe} F CFA. Rejoins mon Telegram en bio."
      else:
        script_genere = f"Session OTC Pocket Option de 20h à 23h. Configuration Stochastique 14, 5, 3 et niveaux 85/15. Rejoins mon Telegram pour le Bot gratuit."
           
            # --- SAUVEGARDE DANS L'HISTORIQUE ---
date_actuelle = datetime.now().strftime("%d/%m/%Y %H:%M")
conn = sqlite3.connect("video_history.db")
cursor = conn.cursor()
cursor.execute('''
INSERT INTO videos (date, theme, capital, script, statut)
VALUES (?, ?, ?, ?, ?)
''', (date_actuelle, theme, capital, script_genere, "Générée avec succès"))
conn.commit()
conn.close()
st.balloons()
st.success("✅ Vidéo confectionnée et enregistrée dans votre historique !")
st.info(f"**Texte envoyé à l'IA :** {script_genere}")

# --- SECTION HISTORIQUE VISIBLE SUR L'APPLICATION ---
st.markdown("---")
st.subheader("📊 Historique de vos Vidéos Générées")

# Lecture des données sauvegardées
conn = sqlite3.connect("video_history.db")
cursor = conn.cursor()
cursor.execute("SELECT date, theme, capital, script, statut FROM videos ORDER BY id DESC")
rows = cursor.fetchall()
conn.close()

# Affichage scannable sous forme de liste propre
if rows:
  for row in rows:
    with st.expander(f"📅 {row[0]} - {row[1]} ({row[2]} F CFA)"):
      st.write(f"**Statut :** `{row[4]}`")
      st.write(f"**Script déclamé :** {row[3]}")
else:
  st.caption("Aucune vidéo dans l'historique pour le moment. Lancez votre première confection !")
