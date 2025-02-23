import streamlit as st
import re
import os
from gtts import gTTS

def display_math_response(response_text):
    """Viser tekst og LaTeX formler korrekt i Streamlit."""
    latex_expressions = re.findall(r"\$\$(.*?)\$\$", response_text)
    text_parts = re.split(r"\$\$(.*?)\$\$", response_text)
    
    for i, part in enumerate(text_parts):
        if i % 2 == 0:
            st.write(part)
        else:
            st.latex(part)

def text_to_speech(text, filename="speech.mp3"):
    """Konverterer tekst til tale og gemmer som en mp3-fil."""
    tts = gTTS(text, lang="da")  # Dansk sprog
    tts.save(filename)
    return filename
