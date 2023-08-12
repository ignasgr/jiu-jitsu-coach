import requests
import streamlit as st


ENDPOINT = "http://openai/chat"

def main():

    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    for message in st.session_state["messages"]:
        st.chat_message(message["role"]).markdown(message["content"])

    if user_prompt := st.chat_input("Start typing here..."):

        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user").markdown(user_prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for chunk in requests.post(
                url=ENDPOINT,
                json={"history": st.session_state.messages},
                stream=True
            ):
                chunk_msg = chunk.decode("utf-8")
                full_response += chunk_msg
                message_placeholder.markdown(full_response + "▌")

            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
