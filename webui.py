import os
from dotenv import load_dotenv, find_dotenv
import requests
import streamlit as st


load_dotenv(find_dotenv())
base_url = os.getenv("BASE_URL")

st.set_page_config(page_title="Chatbot")
st.title("Simple AI Chatbot 🤖")

if "generated" not in st.session_state:
    st.session_state["generated"] = ["I'm an AI chatbot. How may I help you?"]

if "past" not in st.session_state:
    st.session_state["past"] = ["Hi!"]

response_container = st.container()


counter = 0  # Global counter variable

def get_text():
    global counter
    counter += 1
    input_text = st.text_input(
        "",
        "",
        key=f"input_{counter}",
        help="Type your message here...",
    )


    st.markdown(
        """
        <style>
        .stTextInput>div>div>input {
            padding: 10px 12px;
            border-radius: 20px;
            border: 1px solid #dddfe2;
            background-color: #f0f2f5;
            width: 100%;
            outline: none;
            font-size: 14px;
            transition: border-color 0.2s ease-in-out;
            color: #000000; /* Adjust the text color here */
        }

        .stTextInput>div>div>input:focus {
            border-color: #0084ff;
            box-shadow: none;
        }
        
        .stTextInput>div>div>input::placeholder {
            color: #808080;
            opacity: 1;
        }

        .stTextInput>div>div>input::-webkit-input-placeholder {
            color: #808080;
        }

        .stTextInput>div>div>input::-moz-placeholder {
            color: #808080;
        }

        .stTextInput>div>div>input:-ms-input-placeholder {
            color: #808080;
        }

        .stTextInput>div>div>input:-moz-placeholder {
            color: #808080;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    return input_text


def chat_url():
    return base_url


def generate_response(prompt):
    payload = {"input_text": prompt}
    response_ = requests.post(chat_url(), json=payload)
    chatbot_response = response_.json().get("response")
    return chatbot_response


def chat_message(text, is_user=False, key=None):
    if is_user:
        message_type = "user"
        avatar = "https://cdn.pixabay.com/photo/2023/05/20/21/17/ai-generated-8007371_1280.jpg"  # Replace with the URL of the user avatar
        bg_color = "#DCF8C6"
        text_color = "#000000"  # Black text color for user messages
    else:
        message_type = "bot"
        avatar = "https://cdn.pixabay.com/photo/2023/05/24/17/48/ai-generated-8015423_1280.jpg"  # Replace with the URL of the chatbot avatar
        bg_color = "#F1F0F0"
        text_color = "#000000"  # Black text color for bot messages

    st.markdown(
        f"""
        <div class="message-container {'user-message-container' if is_user else 'bot-message-container'}">
            <img src="{avatar}" alt="Avatar" class="message-avatar">
            <div class="message-text" style="background-color: {bg_color}; color: {text_color}">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    .message-container {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
        margin-bottom: 10px;
    }

    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 10px;
    }

    .user-message-container {
        justify-content: flex-end;
    }

    .bot-message-container {
        justify-content: flex-start;
    }

    .message-text {
        padding: 10px;
        border-radius: 8px;
        font-size: 14px;
    }

    .message-input-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        margin-top: 20px;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 8px;
    }

    .message-input {
        flex: 1;
        margin-right: 10px;
        border: none;
        outline: none;
        font-size: 14px;
    }

    .message-send-button {
        background-color: #0084ff;
        color: white;
        border: none;
        padding: 8px 12px;
        border-radius: 4px;
        cursor: pointer;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with response_container:
    user_input = get_text()

    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            chat_message(
                st.session_state["past"][i], is_user=True, key=str(i) + "_user"
            )
            chat_message(st.session_state["generated"][i], key=str(i))
            if i == len(st.session_state["generated"]) - 1:
                st.markdown("<hr>", unsafe_allow_html=True)

with response_container:
    user_input = get_text()

    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            chat_message(
                st.session_state["past"][i], is_user=True, key=str(i) + "_user"
            )
            chat_message(st.session_state["generated"][i], key=str(i))

        # Scroll to bottom of the chat
        js = "document.getElementById('output-container').scrollIntoView();"
        st.write(f"<script>{js}</script>", unsafe_allow_html=True)
