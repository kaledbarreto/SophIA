import google.generativeai as genAi
from dotenv import load_dotenv
from utils.configs import *
import streamlit as st
import os

# Load Google Gemni
def loadGemini() -> None: 
    load_dotenv()
    genAi.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Setup Google Gemni Model
def setupModel() -> genAi.GenerativeModel:
    return genAi.GenerativeModel(
        model_name=modelName,
        system_instruction=systemInstructions
    )

# Translate roles between Gemini and Streamlit
def translateRoleForStreamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Load Streamlit Configs and Styles
def loadStreamlit() -> None:
    st.set_page_config(
        page_title="Sophia, a Sábia!",
        page_icon=":star:",
        layout="centered",
    )

    # Display the chatbot's title on the page
    st.markdown("<h1 style='text-align: center;'>Sophia, a Sábia! ⭐</h1>", unsafe_allow_html=True)

    # Create card layout with columns
    col1, col2 = st.columns([1, 2])

    # Display image in the left column
    with col1:
        st.image(sophiaImg, width=200)

    # Display text in the right column
    with col2:
        st.markdown(f"<p style='margin-top: 1.5em; font-size: 1.5em'>{headerText}</p>", unsafe_allow_html=True)

    # Display the divider
    st.divider()

def main() -> None:
    loadGemini()
    model = setupModel()

    # Initialize chat session in Streamlit if not already present
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[{'role':'model', 'parts': [model.generate_content(startChatText).text]}])

    loadStreamlit()

    # Display the chat history
    for message in st.session_state.chat_session.history:
        avatar = sophiaImg if translateRoleForStreamlit(message.role) == "assistant" else userImg
        with st.chat_message(translateRoleForStreamlit(message.role), avatar=avatar):
            st.markdown(message.parts[0].text)

    # Input field for user's message
    userPrompt = st.chat_input(inputPlaceholderText)
    if userPrompt:
        # Add user's message to chat and display it
        st.chat_message("user", avatar=userImg).markdown(userPrompt)

        # Send user's message to Gemini and get the response
        geminiResponse = st.session_state.chat_session.send_message(userPrompt)

        # Display Gemini's response
        with st.chat_message("assistant", avatar=sophiaImg):
            st.markdown(geminiResponse.text)

# Running the project!
if __name__ == "__main__":
    main()