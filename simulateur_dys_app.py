import streamlit as st
import random
import time

# Function to invert specific letters
def invert_letters(text):
    letter_map = {'b': 'd', 'd': 'b', 'p': 'q', 'q': 'p'}
    return ''.join([letter_map.get(c, c) for c in text])

# Function to randomly omit letters
def omit_random_letters(text, omit_prob=0.1):
    return ''.join([c if random.random() > omit_prob else '' for c in text])

# Function to vary letter case
def vary_case(text):
    return ''.join([c.upper() if random.random() > 0.5 else c.lower() for c in text])

# Function to reverse the text (mirror effect)
def mirror_text(text):
    return text[::-1]

# Function to scramble the middle letters of a word (preserving first and last if needed)
def scramble_word(word, keep_first_last=False):
    if len(word) > 3 and keep_first_last:
        middle = list(word[1:-1])  # Select the middle letters
        random.shuffle(middle)
        return word[0] + ''.join(middle) + word[-1]  # Keep first and last letter in place
    elif len(word) > 1:
        letters = list(word)
        random.shuffle(letters)
        return ''.join(letters)
    return word

# Function to scramble some words in the text based on scramble_chance
def partial_scramble_text(text, scramble_chance=0.5, keep_first_last=False):
    return ' '.join([scramble_word(word, keep_first_last) if random.random() < scramble_chance else word for word in text.split()])

# Main function to simulate dyslexia
def simulate_dyslexia(text, remove_spaces, invert, omit, vary, mirror, scramble, scramble_chance=0.5, keep_first_last=False):
    # Apply letter inversion
    if invert:
        text = invert_letters(text)

    # Apply letter omission
    if omit:
        text = omit_random_letters(text)

    # Apply case variation
    if vary:
        text = vary_case(text)

    # Apply the mirror effect
    if mirror:
        text = mirror_text(text)

    # Apply partial scrambling if enabled
    if scramble:
        text = partial_scramble_text(text, scramble_chance, keep_first_last)

    words = text.split()

    # Handle space removal after scrambling
    if remove_spaces:
        return ''.join([word + (' ' if random.random() < 0.75 else '') for word in words])
    else:
        return ' '.join(words)

# Streamlit UI
st.markdown("<h3>Simulateur de Dyslexie (version bêta)</h3>", unsafe_allow_html=True)

# Disclaimer
st.markdown(
    "<div style='font-size: 14px; color: gray;'>Ceci est une version expérimentale destinée à simuler certaines formes de dyslexie afin de fournir un aperçu non exhaustif. Il ne s'agit en aucun cas de la Dyslexie avec un grand D, mais plutôt d'une représentation de certaines de ses manifestations.</div>",
    unsafe_allow_html=True
)

# Small credit text
st.markdown(
    "<div style='font-size: 10px; color: gray; text-align: right;'>Développé par Hussein (100% Handinamique)</div>",
    unsafe_allow_html=True
)

# Add some styling for the text boxes
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

# Two columns for original and transformed text
col1, col2 = st.columns([1, 1])

# Text input on the left
with col1:
    st.subheader("Texte original")
    user_input = st.text_area("Entrez le texte ici", height=200, key="original_text", label_visibility="collapsed")

# Text output on the right
with col2:
    st.subheader("Texte transformé")
    text_placeholder = st.empty()

# Control settings
st.subheader("Réglages")

# Space removal option
remove_spaces = st.checkbox("Activer la suppression des espaces", value=False)

# Scramble chance slider
scramble_chance = st.slider("Pourcentage de mots brouillés", 0.0, 1.0, 0.5)

# Option to keep the first and last letters stable
keep_first_last = st.checkbox("Garder les premières et dernières lettres stables", value=False)

# Speed of update
update_speed = st.slider("Vitesse de mise à jour (en millisecondes)", 500, 3000, 1000)

# Enable/disable letter scrambling
scramble_letters = st.checkbox("Activer le brouillage des lettres", value=False)

# Additional dyslexia effects
col3, col4, col5 = st.columns(3)
with col3:
    bold = st.checkbox("Gras (rend le texte en gras)", value=False)
with col4:
    italic = st.checkbox("Italique (rend le texte en italique)")
with col5:
    underline = st.checkbox("Souligné (souligner le texte)")

# Font style option
font_choice = st.selectbox("Choisir la police (affecte le style de police du texte transformé)", ["Arial", "Baskerville"])

# Dyslexia effects options
col6, col7, col8, col9 = st.columns(4)
with col6:
    invert_letters_option = st.checkbox("Inverser lettres (b ↔ d, p ↔ q)", value=False)
with col7:
    omit_letters_option = st.checkbox("Omission aléatoire des lettres (supprime certaines lettres aléatoirement)", value=False)
with col8:
    vary_case_option = st.checkbox("Variation des tailles de caractères (majuscule/minuscule aléatoire)", value=False)
with col9:
    mirror_option = st.checkbox("Effet miroir (inverser tout le texte)", value=False)

# Apply selected font styles
font_styles = {
    "Arial": "font-family: Arial, sans-serif;",
    "Baskerville": "font-family: Baskerville, serif;"
}

# Apply bold, italic, underline styles
style = ""
if bold:
    style += "font-weight: bold;"
if italic:
    style += "font-style: italic;"
if underline:
    style += "text-decoration: underline;"

# Run the dyslexia simulation and display the transformed text
if user_input:
    for _ in range(100 if scramble_letters else 1):  # Run the loop only if scrambling is enabled
        transformed_text = simulate_dyslexia(user_input, remove_spaces, invert_letters_option, omit_letters_option, vary_case_option, mirror_option, scramble_letters, scramble_chance, keep_first_last)
        styled_text = f"<div class='text-box' style='{font_styles[font_choice]} {style};'>{transformed_text}</div>"
        text_placeholder.markdown(styled_text, unsafe_allow_html=True)
        time.sleep(update_speed / 1000)
