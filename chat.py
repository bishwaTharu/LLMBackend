import os
from dotenv import load_dotenv, find_dotenv
import requests
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header


load_dotenv(find_dotenv())
base_url = os.getenv("BASE_URL")


st.set_page_config(page_title="Chatbot")
st.title("Simple AI Chatbot 🤖")

if "generated" not in st.session_state:
    st.session_state["generated"] = ["I'm AI chatbot, How may I help you?"]

if "past" not in st.session_state:
    st.session_state["past"] = ["Hi!"]

input_container = st.container()
colored_header(label="", description="", color_name="blue-30")
response_container = st.container()


def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


## Applying the user input box
with input_container:
    user_input = get_text()


def chat_url():
    return base_url


def prompt_():
    txt_ = input()
    return txt_


def generate_response(prompt):
    payload = {"input_text": prompt}

    response_ = requests.post(chat_url(), json=payload)
    chatbot_response = response_.json().get("response")
    # response = chatbot.chat(prompt)
    return chatbot_response


with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state["generated"]:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i))
