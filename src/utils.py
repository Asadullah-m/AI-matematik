import streamlit as st
import re

def display_math_response(response_text):
    """Viser tekst og LaTeX formler korrekt i Streamlit med naturlige linjeskift og afsnit."""
    # NY: Genkender kun $...$ for inline-formler (da vi bad OpenAI undgå $$...$$)
    latex_expressions = re.findall(r"\$(.*?)\$", response_text)
    text_parts = re.split(r"\$(.*?)\$", response_text)
    
    # NY: Bevar linjeskift og afsnit, og vis tekst og LaTeX separat for bedre struktur
    for i, part in enumerate(text_parts):
        if part.strip():  # Ignorer tomme dele
            if i % 2 == 0:
                # Almindelig tekst – bevar linjeskift og mellemrum, men fjern unødvendige ekstra linjeskift
                cleaned_text = "\n".join(line for line in part.splitlines() if line.strip())
                # NY: Brug st.markdown for at bevare formatering, men med bedre kontrol
                st.markdown(cleaned_text)
            else:
                # LaTeX-formel – rendrér den korrekt
                try:
                    st.latex(part)
                except Exception as e:
                    # Hvis der er en fejl i LaTeX, vis bare teksten som almindelig tekst
                    st.write(f"Fejl i formel: {part}")