import streamlit as st
import re
from io import BytesIO
from gtts import gTTS

def display_math_response(response_text):
    """Viser tekst og LaTeX formler korrekt i Streamlit."""
    latex_expressions = re.findall(r"\$\$(.*?)\$\$", response_text)
    text_parts = re.split(r"\$\$(.*?)\$\$", response_text)
    
    for i, part in enumerate(text_parts):
        # Lige indeks = almindelig tekst, ulige = latex
        if i % 2 == 0:
            st.write(part)
        else:
            st.latex(part)

def text_to_speech(text):
    """
    Konverterer tekst til tale og returnerer en BytesIO-strøm
    (i stedet for at gemme en mp3-fil på disk).
    """
    tts = gTTS(text, lang="da")
    audio_data = BytesIO()
    tts.write_to_fp(audio_data)
    audio_data.seek(0)  # Sæt 'filhovedet' til start
    return audio_data
