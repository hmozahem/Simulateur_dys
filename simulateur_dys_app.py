import streamlit as st
import random
import time

# Fonction pour brouiller les lettres à l'intérieur des mots
def scramble_word(word, keep_first_last=False):
    if len(word) > 3:
        middle = list(word[1:-1]) if keep_first_last else list(word)
        random.shuffle(middle)
        return word[0] + ''.join(middle) + word[-1] if keep_first_last else ''.join(middle)
    return word

# Fonction pour brouiller partiellement le texte (seulement certains mots)
def partial_scramble_text(text, scramble_chance=0.5, keep_first_last=False):
    return ' '.join([scramble_word(word, keep_first_last) if random.random() < scramble_chance else word for word in text.split()])

# Titre
st.markdown("<h3>Simulateur de Dyslexie (version bêta)</h3>", unsafe_allow_html=True)

# Disclaimer mis à jour avec introduction plus grande
st.markdown(
    "<div style='font-size: 20px; color: black;'>Il y a plusieurs options présentes qui représentent des variantes de la dyslexie, mais elles ne sont pas forcément cumulatives.</div>",
    unsafe_allow_html=True
)

# Ajout du texte supplémentaire après le disclaimer
st.markdown(
    "<div style='font-size: 14px; color: gray;'>Ceci est une version expérimentale, destinée à simuler certaines formes de dyslexie afin de fournir un aperçu non exhaustif. Il ne s'agit en aucun cas de la Dyslexie avec un grand D, mais plutôt d'une représentation de certaines de ses manifestations.</div>",
    unsafe_allow_html=True
)

# Texte discret pour "Développé par Hussein"
st.markdown(
    "<div style='font-size: 10px; color: gray; text-align: right;'>Développé par Hussein (100% Handinamique)</div>",
    unsafe_allow_html=True
)

# Ajout du CSS pour les cadres fixes et des infobulles
st.markdown(
    """
    <style>
    .text-box {
        border: 1px solid lightgray;
        padding: 10px;
        height: 200px;
    }
    </style>
    """, unsafe_allow_html=True
)

# Mise en place des colonnes pour le texte original et le texte transformé
col1, col2 = st.columns([1, 1])

# Cadre pour le texte original à gauche
with col1:
    st.subheader("Texte original")
    user_input = st.text_area("Entrez le texte ici", height=200, key="original_text", label_visibility="collapsed")

# Cadre pour le texte transformé à droite
with col2:
    st.subheader("Texte transformé")
    text_placeholder = st.empty()

# Réglages placés en bas
st.subheader("Réglages")

# Scramble Chance slider
scramble_chance = st.slider("Pourcentage de mots brouillés", 0.0, 1.0, 0.5)

# Option pour maintenir les premières et dernières lettres des mots stables
keep_first_last = st.checkbox("Garder les premières et dernières lettres stables", value=False)

# Vitesse de mise à jour
update_speed = st.slider("Vitesse de mise à jour (en millisecondes)", 500, 3000, 1000)

# Option pour activer ou désactiver le brouillage partiel (désactivé par défaut)
scramble_letters = st.checkbox("Activer le brouillage des lettres", value=False)

# Simulation du texte si activée
if user_input:
    if scramble_letters:
        for _ in range(100):  # Limite la boucle pour éviter une boucle infinie
            scrambled_text = partial_scramble_text(user_input, scramble_chance, keep_first_last)
            text_placeholder.markdown(f"<div class='text-box'>{scrambled_text}</div>", unsafe_allow_html=True)
            time.sleep(update_speed / 1000)
    else:
        text_placeholder.markdown(f"<div class='text-box'>{user_input}</div>", unsafe_allow_html=True)
