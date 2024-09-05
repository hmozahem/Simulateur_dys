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
        middle = list(word[1:-1])
        random.shuffle(middle)
        return word[0] + ''.join(middle) + word[-1]  # Keep first and last letter in place
    elif len(word) > 1:
        letters = list(word)
        random.shuffle(letters)
        return ''.join(letters)
    return word

# Function to scramble text
def partial_scramble_text(text, scramble_chance=0.5, keep_first_last=False):
    return ' '.join([scramble_word(word, keep_first_last) if random.random() < scramble_chance else word for word in text.split()])

# Function for static scrambling
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

# Add custom CSS for smooth transition
st.markdown("""
    <style>
    .text-box {
        border: 1px solid lightgray;
        padding: 10px;
        height: 200px;
        overflow: hidden;
    }
    .scrambled-text span {
        display: inline-block;
        transition: transform 0.3s ease, opacity 0.3s ease;
    }
    .scrambled-text span:hover {
        transform: translateY(-5px);
        opacity: 0.8;
    }
    </style>
""", unsafe_allow_html=True)

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

# Option de suppression des espaces
remove_spaces = st.checkbox("Activer la suppression des espaces", value=False)

# Scramble settings
scramble_chance = st.slider("Pourcentage de mots brouillés", 0.0, 1.0, 0.5)
keep_first_last = st.checkbox("Garder les premières et dernières lettres stables", value=False)
dynamic_scramble = st.checkbox("Activer le brouillage dynamique", value=False)

# Options de style
col3, col4, col5 = st.columns(3)
with col3:
    bold = st.checkbox("Gras", value=False)
with col4:
    italic = st.checkbox("Italique", value=False)
with col5:
    underline = st.checkbox("Souligné", value=False)

# Option de sélection de police
font_choice = st.selectbox("Choisir la police", ["Arial", "Baskerville"])

# Options pour simuler différentes formes de dyslexie
col6, col7, col8, col9 = st.columns(4)
with col6:
    invert_letters_option = st.checkbox("Inverser lettres (b ↔ d, p ↔ q)", value=False)
with col7:
    omit_letters_option = st.checkbox("Omission aléatoire des lettres", value=False)
with col8:
    vary_case_option = st.checkbox("Variation des tailles de caractères", value=False)
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

# Static scrambling by default
if user_input:
    scrambled_text = simulate_dyslexia(user_input, remove_spaces, invert_letters_option, omit_letters_option, vary_case_option, mirror_option, True, scramble_chance, keep_first_last)

    # Wrap each letter in a span to apply transition effects
    animated_text = ''.join([f"<span>{char}</span>" for char in scrambled_text])

    if dynamic_scramble:
        # Add class for dynamic animation
        text_placeholder.markdown(f"<div class='text-box'><div class='scrambled-text'>{animated_text}</div></div>", unsafe_allow_html=True)
    else:
        # Static scrambled text without animation
        text_placeholder.markdown(f"<div class='text-box'>{animated_text}</div>", unsafe_allow_html=True)
