import streamlit as st
from src.generator import generate_explanation, generate_exercise, generate_solution, generate_hint
from src.utils import display_math_response, text_to_speech
import streamlit as st

# 1) Opsætning af siden
st.set_page_config(
    page_title="Asa Matematik",
    page_icon="📚",  # Du kan også bruge en .png-fil, hvis du vil
    layout="centered"  # layout="wide" hvis du vil have en bred side
)
page_bg_css = """
<style>
/* Hele appens baggrund */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #FFFFFF 0%, #E3F2FD 100%);
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)


def show_ui():
    """Viser brugergrænsefladen til AI Matematikopgavegeneratoren med én opgave ad gangen."""
    topics = [
        "Brøker", "Geometri", "Areal af trekanter", "Divisor og primtal",
        "Ligninger", "Ligninger og regneudtryk", "Mål og enheder",
        "Hele koordinatsystemet", "Cirkler", "Skitse og tegning",
        "Statistiske undersøgelser", "Spil og simulering", "Indbrud i borgen"
    ]

    st.title("📚🤖 AI Matematikopgavegenerator")
    st.write("### Velkommen til AsaMatematik 😀")

    
    st.write("💡 Vælg et matematikemne, og lad mig forklare og give dig opgaver!")
    

    # Vælg emne og sværhedsgrad
    selected_topic = st.selectbox("📌 Vælg et emne:", topics)
    difficulty = st.selectbox("📏 Vælg sværhedsgrad:", ["Let", "Mellem", "Svær"])

    # Session states for forklaring
    if "explanation" not in st.session_state:
        st.session_state.explanation = None

    # Knap: Forklar emnet
    if st.button("📖 Forklar emnet"):
        st.session_state.explanation = generate_explanation(selected_topic)

    # Hvis vi har en forklaring, vis den
    if st.session_state.explanation:
        st.subheader(f"📚 Forklaring af {selected_topic}")
        display_math_response(st.session_state.explanation)

        # Knap: Lyt til forklaringen
        if st.button("🔊 Lyt til forklaringen"):
            audio_data = text_to_speech(st.session_state.explanation)
            st.audio(audio_data, format="audio/mp3")

        # Knap: Få hjælp (hint)
        if st.button("🆘 Få hjælp til forklaringen"):
            hint = generate_hint(st.session_state.explanation)
            st.write(f"💡 **Alternativ forklaring:** {hint}")

    # Session states for opgave
    if "current_exercise" not in st.session_state:
        st.session_state.current_exercise = None
    if "exercise_solution" not in st.session_state:
        st.session_state.exercise_solution = None
    if "exercise_attempt" not in st.session_state:
        st.session_state.exercise_attempt = None

    # Knap: Giv mig en opgave
    if st.button("🎲 Giv mig en opgave"):
        st.session_state.current_exercise = generate_exercise(selected_topic, difficulty)
        st.session_state.exercise_solution = generate_solution(
            selected_topic,
            st.session_state.current_exercise
        )
        st.session_state.exercise_attempt = None

    # Hvis der er en aktuel opgave, vis den
    if st.session_state.current_exercise:
        st.subheader("📝 Opgave:")
        display_math_response(st.session_state.current_exercise)

        st.session_state.exercise_attempt = st.text_area("✍️ Skriv din løsning her:")

        # Knap: Tjek mit svar
        if st.button("✅ Tjek mit svar"):
            if not st.session_state.exercise_attempt or st.session_state.exercise_attempt.strip() == "":
                st.write("💡 Du skal skrive din løsning, før du kan tjekke den!")
            else:
                st.write("### ✅ Løsning:")
                display_math_response(st.session_state.exercise_solution)

                st.write("Vil du prøve en ny opgave?")
                col1, col2 = st.columns(2)

                with col1:
                    if st.button("👍 Jeg vil prøve igen"):
                        st.session_state.current_exercise = generate_exercise(selected_topic, difficulty)
                        st.session_state.exercise_solution = generate_solution(
                            selected_topic,
                            st.session_state.current_exercise
                        )
                        st.session_state.exercise_attempt = None

                with col2:
                    if st.button("❌ Nej, jeg er færdig"):
                        st.session_state.current_exercise = None
                        st.session_state.exercise_solution = None
                        st.session_state.exercise_attempt = None

if __name__ == "__main__":
    show_ui()
