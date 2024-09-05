import streamlit as st
import random
import time

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
def simulate_dyslexia(text, scramble, scramble_chance=0.5, keep_first_last=False):
    if scramble:
        return partial_scramble_text(text, scramble_chance, keep_first_last)
    return text

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

# Scramble settings
scramble_chance = st.slider("Pourcentage de mots brouillés", 0.0, 1.0, 0.5)
keep_first_last = st.checkbox("Garder les premières et dernières lettres stables", value=False)
dynamic_scramble = st.checkbox("Activer le brouillage dynamique", value=False)

# Scramble the text (statically on every input)
if user_input:
    scrambled_text = simulate_dyslexia(user_input, scramble=True, scramble_chance=scramble_chance, keep_first_last=keep_first_last)

    # Wrap each letter in a span to apply transition effects
    animated_text = ''.join([f"<span>{char}</span>" for char in scrambled_text])

    if dynamic_scramble:
        # Add class for dynamic animation
        text_placeholder.markdown(f"<div class='text-box'><div class='scrambled-text'>{animated_text}</div></div>", unsafe_allow_html=True)
    else:
        # Static scrambled text without animation
        text_placeholder.markdown(f"<div class='text-box'>{animated_text}</div>", unsafe_allow_html=True)
