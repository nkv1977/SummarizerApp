import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
# Get API key safely
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API key not found. Please add it in Streamlit Secrets.")
    st.stop()  # Stop the app gracefully

# Initialize client
client = OpenAI(api_key=api_key)
# Streamlit UI
st.write("API Key found?", bool(api_key))
st.title("📝 AI Text Summarizer..Version 6th Sep 19:33")
st.write("Paste your text below and let AI summarize it for you.")

# User input
text = st.text_area("Enter text here:", height=200)

uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
if uploaded_file is not None:
    text = uploaded_file.read().decode("utf-8")

# Summary length option
option = st.radio("Choose summary length:", ["Short", "Medium", "Long"])
if option == "Short":
                prompt = f"Summarize briefly: {text}"
elif option == "Medium":
                prompt = f"Summarize in a paragraph: {text}"
else:
                prompt = f"Summarize in detail: {text}"

# Summarize button
if st.button("Summarize"):
    if text.strip() == "":
        st.warning("⚠️ Please enter some text first.")
    else:
        # Map user choice to instructions
        length_instruction = {
            "Short": "Summarize in 1 sentences.",
            "Medium": "Summarize in 1 short paragraph.",
            "Long": "Summarize in detail (3-5 sentences)."
        }

        # Call OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": f"{length_instruction[option]} Here is the text: {text}"}
            ]
        )

        # Show summary
        summary = response.choices[0].message.content
        st.subheader("📌 Summary")
        st.write(summary)





