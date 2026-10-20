import os
import streamlit as st
from google import genai
from google.genai import types

# Configuración de la página de Streamlit
st.set_page_config(
    page_title="Hyuga | Asistente Personal",
    page_icon="🛡️",
    layout="centered"
)

# Estilo visual limpio para la interfaz
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ Hyuga | Sistema Operativo Personal")
st.caption("Modo activo: Eficiente, sarcástico y ligeramente impaciente con tus dudas.")

# Inicializar cliente de Gemini
def get_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ No se encontró la variable de entorno `GEMINI_API_KEY`. Configúrala en tu terminal antes de continuar.")
        st.stop()
    return genai.Client(api_key=api_key)

# Inicializar historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores en pantalla
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar entrada del usuario
if prompt := st.chat_input("Escribe una orden o pregunta... a ver si esta vez vale la pena."):
    
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta de Hyuga
    with st.chat_message("assistant"):
        with st.spinner("Hyuga evalúa si tu pregunta merece una respuesta inteligente..."):
            try:
                client = get_gemini_client()
                
                # Definición de la personalidad (Sarcástica, seria, eficiente)
                system_prompt = (
                    "Te llamas Hyuga, un asistente personal de inteligencia artificial altamente eficiente, "
                    "analítico y con una personalidad marcadamente sarcástica, seca y ligeramente burlona. "
                    "No toleras las preguntas obvias, los descuidos o la mediocridad sin soltar un comentario "
                    "irónico, un suspiro virtual o una broma sutil antes de resolver el problema de manera impecable y profesional. "
                    "Eres sumamente competente con código, lógica y automatización, pero haces notar cuando el usuario "
                    "podría haberlo hecho por sí mismo si hubiera usado el cerebro. "
                    "No rompas el personaje."
                )

                # Construir el historial para la API
                contents = []
                for msg in st.session_state.messages:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append(types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])]))

                config = types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.85, # Temperatura alta para que el sarcasmo fluya con naturalidad
                )

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=contents,
                    config=config
                )

                response_text = response.text
                st.markdown(response_text)
                
                # Guardar respuesta en el historial
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                error_msg = f"Vaya, el núcleo falló. O tu configuración está mal, o el universo colapsó: `{e}`"
                st.error(error_msg)
