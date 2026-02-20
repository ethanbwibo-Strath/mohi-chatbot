import streamlit as st
import requests

# 1. Page Configuration
st.set_page_config(page_title="Rafiki IT Chatbot", page_icon="🤖")
st.title("🤖 Rafiki IT: MOHI Support")
st.markdown("---")

# 2. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Chat Input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to UI
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 5. Call the FastAPI Backend
    with st.chat_message("assistant"):
        with st.spinner("Rafiki is thinking..."):
            try:
                # Prepare the history to send to the backend
                # We send the existing messages so the bot has 'memory'
                chat_history = st.session_state.messages 

                response = requests.post(
                    "http://127.0.0.1:8000/chat", 
                    json={
                        "message": prompt,
                        "history": chat_history
                    }
                )
                
                if response.status_code == 200:
                    answer = response.json().get("response")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error("I'm having trouble connecting to the brain.")
            except Exception as e:
                st.error(f"Connection Error: {e}")