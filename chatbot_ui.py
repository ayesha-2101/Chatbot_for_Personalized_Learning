import streamlit as st
import requests

st.set_option('client.showErrorDetails', False)
st.set_page_config(page_title="Educational Chatbot", page_icon="🤖")
st.title("Educational Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.container():
    user_input = st.text_input(
        "Type your message here...",
        placeholder="Type your message and press 'Send'",
        key="user_input",
    )
    send_button = st.button("Send")

if send_button and user_input:
    st.session_state.messages.append({"text": user_input, "is_user": True})

    rasa_server_url = "http://localhost:5005/webhooks/rest/webhook"
    response = requests.post(
        rasa_server_url, json={"sender": "user", "message": user_input}
    )

    if response.status_code == 200:
        bot_responses = response.json()
        combined_bot_response = " ".join(
            bot_response.get("text", "") for bot_response in bot_responses
        )
        st.session_state.messages.append(
            {"text": combined_bot_response, "is_user": False}
        )
    else:
        st.session_state.messages.append(
            {"text": "Error: Unable to connect to the Rasa server.", "is_user": False}
        )

    st.experimental_set_query_params()  

for message in st.session_state.messages:
    with st.container():
        if message["is_user"]:
            st.markdown(
                f"""
                <div style="background-color: #25D366; padding: 10px; border-radius: 10px; margin-bottom: 10px; max-width: 80%; text-align: left; margin-left: 10px;">
                    <p style="margin: 0; color: #000000;">You: {message['text']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div style="background-color: #FFFFFF; padding: 10px; border-radius: 10px; margin-bottom: 10px; max-width: 80%; text-align: left; margin-right: 10px;">
                    <p style="margin: 0; color: #000000;">Bot: {message['text']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
