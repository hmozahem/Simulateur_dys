import streamlit as st
import random
import time

# Fonction pour inverser certaines lettres spécifiques
def invert_letters(text):
    letter_map = {'b': 'd', 'd': 'b', 'p': 'q', 'q': 'p'}
    return ''.join([letter_map.get(c, c) for c in text])

# Fonction pour omettre aléatoirement des lettres
def omit_random_letters(text, omit_prob=0.1):
    return ''.join([c if random.random() > omit_prob else '' for c in text])

# Fonction pour varier la taille des caractères
def vary_case(text):
    return ''.join([c.upper() if random.random() > 0.5 else c.lower() for c in text])

# Fonction pour inverser tout le texte (effet miroir)
def mirror_text(text):
    return text[::-1]

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

# Fonction principale pour simuler la dyslexie
def simulate_dyslexia(text, remove_spaces, invert, omit, vary, mirror, scramble, scramble_chance=0.5, keep_first_last=False):
    def scramble_word(word):
        if len(word) > 1:
            letters = list(word)
            random.shuffle(letters)
            return ''.join(letters)
        return word

    if invert:
        text = invert_letters(text)

    if omit:
        text = omit_random_letters(text)

    if vary:
        text = vary_case(text)

    # Appliquer l'effet miroir si activé
    if mirror:
        text = mirror_text(text)

    # Appliquer le brouillage partiel si activé
    if scramble:
        text = partial_scramble_text(text, scramble_chance, keep_first_last)

    scrambled_words = [scramble_word(word) for word in text.split()]

    # Ajuster le taux de suppression des espaces (réduit à 25 %) seulement si l'option "premières/dernières lettres stables" est désactivée
    if remove_spaces and not keep_first_last:
        return ''.join([word + (' ' if random.random() < 0.75 else '') for word in scrambled_words])
    else:
        return ' '.join(scrambled_words)

# Titre
st.markdown("<h3>Simulateur de Dyslexie (version bêta)</h3>", unsafe_allow_html=True)

# Disclaimer mis à jour
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

# Option de suppression des espaces
remove_spaces = st.checkbox("Activer la suppression des espaces", value=False)

# Scramble Chance slider
scramble_chance = st.slider("Pourcentage de mots brouillés", 0.0, 1.0, 0.5)

# Option pour maintenir les premières et dernières lettres des mots stables
keep_first_last = st.checkbox("Garder les premières et dernières lettres stables", value=False)

# Vitesse de mise à jour
update_speed = st.slider("Vitesse de mise à jour (en millisecondes)", 500, 3000, 1000)

# Option pour activer ou désactiver le brouillage partiel (désactivé par défaut)
scramble_letters = st.checkbox("Activer le brouillage des lettres", value=False)

# Options de style avec descriptions dans les infobulles
col3, col4, col5 = st.columns(3)
with col3:
    bold = st.checkbox("Gras (rend le texte en gras)", value=False)
with col4:
    italic = st.checkbox("Italique (rend le texte en italique)")
with col5:
    underline = st.checkbox("Souligné (souligner le texte)")

# Option de sélection de police
font_choice = st.selectbox("Choisir la police (affecte le style de police du texte transformé)", ["Arial", "Baskerville"])

# Options pour simuler différentes formes de dyslexie avec descriptions
col6, col7, col8, col9 = st.columns(4)
with col6:
    invert_letters_option = st.checkbox("Inverser lettres (b ↔ d, p ↔ q)", value=False)
with col7:
    omit_letters_option = st.checkbox("Omission aléatoire des lettres (supprime certaines lettres aléatoirement)", value=False)
with col8:
    vary_case_option = st.checkbox("Variation des tailles de caractères (majuscule/minuscule aléatoire)", value=False)
with col9:
    mirror_option = st.checkbox("Effet miroir (inverser tout le texte)", value=False)

# Appliquer la police et les styles sélectionnés via HTML et CSS
font_styles = {
    "Arial": "font-family: Arial, sans-serif;",
    "Baskerville": "font-family: Baskerville, serif;"
}

# Appliquer les styles (gras, italique, souligné)
style = ""
if bold:
    style += "font-weight: bold;"
if italic:
    style += "font-style: italic;"
if underline:
    style += "text-decoration: underline;"

# Simulation automatique des lettres qui bougent si activée
if user_input:
    for _ in range(100 if scramble_letters else 1):  # Boucle seulement si l'option est activée
        transformed_text = simulate_dyslexia(user_input, remove_spaces, invert_letters_option, omit_letters_option, vary_case_option, mirror_option, scramble_letters, scramble_chance, keep_first_last)
        styled_text = f"<div class='text-box' style='{font_styles[font_choice]} {style};'>{transformed_text}</div>"
        text_placeholder.markdown(styled_text, unsafe_allow_html=True)

        # Délai pour l'effet de mouvement
        time.sleep(update_speed / 1000)

