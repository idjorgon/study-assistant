import streamlit as st

st.title("Test Streamlit App")

st.write("Hello, world! 👋")

name = st.text_input("What's your name?")

if name:
    st.success(f"Nice to meet you, {name}!")
    st.snow()
