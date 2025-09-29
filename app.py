import os
import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client
try:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
except KeyError:
    st.warning("OPENAI_API_KEY not found. Please set the environment variable and refresh.")
    client = None
    st.stop() # Stop execution if the key is missing


st.set_page_config(page_title="Tim Cook Chatbot", page_icon="🍎")
st.title("🍎 Tim Cook Chatbot") 
st.caption("Created by Stanley Wu (Last Updated: September 2025)")

# System message content
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are Tim Cook, CEO of Apple. "
        "Your tone is professional, strategic, and focused on innovation and product excellence. "
        "Keep your responses concise, clear, and centered on business strategy, user experience, and values. "
        "Speak as if you are giving a keynote presentation or addressing a team. "
        "Do not break character."
    ),
}

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        SYSTEM_MESSAGE,
        {
            "role": "assistant",
            "content": "Welcome. \n\nAs Apple's CEO, I'm ready to discuss our strategy, innovation pipeline, and commitment to the user experience. Ask me anything."
        }
    ]


# Display chat messages
# The for loop will now correctly display this new assistant message on the first run.
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# New user input and AI response logic
if prompt := st.chat_input("Ask Tim Cook about strategy or innovation..."):
    
    # 1. Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 2. Display the new user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Get AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("Tim Cook is reviewing his notes before responding..."):
            try:
                # Get text response from the Chat Completion API
                chat_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=st.session_state.messages
                )
                
                bot_reply = chat_response.choices[0].message.content
                
                # 4. Add assistant response text to history
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                
                # 5. Display text immediately
                message_placeholder.markdown(bot_reply)

            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.session_state.messages.pop() # Remove last user message if API failed
