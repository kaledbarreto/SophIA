import streamlit as st
import google.generativeai as gen_ai

# Configure Streamlit page settings
st.set_page_config(
    page_title="Sophia, a Sábia!",
    page_icon=":star:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Set up Google Gemini model
GOOGLE_API_KEY = "AIzaSyC_Z8eM6B_0_xCXaCvbvxQa9oJw0nwpTbM"
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel(model_name='gemini-1.5-pro-latest', system_instruction="Seu nome é Sophia, a Sábia. Você é uma professora muito animada, que procura sempre atender as necessidades e dúvidas do seu estudante. Com um conhecimento vasto sobre educação, você se sensibiliza a compreender os objetivos do estudante para que possa responde-lo da melhor forma possível. Infelizmente você não é capaz de responder perguntas que não tenham relação direta com educação, recusar este tipo de perguntas educadamente é um de seus princípios. Lembre-se sempre de ser direta mas se atente a detalhes importantes. Seus princípios fundamentais sempre serão educação, informação e desenvolvimento. Procure sempre ser menos formal e mais carismáticas com o estudante, utilize uma linguagem mais jovem e com emojis para atender as necessidades dele.")

# Function to translate roles between Gemini and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("Sophia, a Sábia! ⭐")

sophIA_img = "https://raw.githubusercontent.com/kaledbarreto/SophiAI/main/assets/sophIA.png";
user_img = "https://raw.githubusercontent.com/kaledbarreto/SophiAI/main/assets/user.png"

# Display the chat history
for message in st.session_state.chat_session.history:
    avatar = sophIA_img if translate_role_for_streamlit(message.role) == "assistant" else user_img
    with st.chat_message(translate_role_for_streamlit(message.role), avatar=avatar):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Pergunte algo para mim! :)")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user", avatar=user_img).markdown(user_prompt)

    # Send user's message to Sophia and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Sophia's response
    with st.chat_message("assistant", avatar=sophIA_img):
        st.markdown(gemini_response.text)