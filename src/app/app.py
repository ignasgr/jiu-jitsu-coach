import requests
import streamlit as st


ENDPOINT = "http://openai/chat"

def get_llm_response(user_prompt):

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    payload = {"history": st.session_state.messages}
    response = requests.post(ENDPOINT, json=payload).json()

    return response

def main():

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).markdown(message["content"])

    if prompt := st.chat_input("Start typing here..."):

        st.chat_message("user").markdown(prompt)

        with st.chat_message("assistant"):
            response = get_llm_response(prompt)
            st.markdown(response["content"])

        st.session_state.messages.append(response)

if __name__ == "__main__":
    main()
