import streamlit as st
from groq import GroqClient
import os

key = os.getenv("GROQ_API")  # Get the Groq API key from environment variables

# Set up the Groq client
groq_client = GroqClient(
    api_key=key,
    model_name="llama",
    model_version="main",
    logging=True,
    temperature=0.5,  # default temperature
    max_length=2048,  # default max length
    top_p=0.9,  # default top-p
    frequency_penalty=0.5,  # default frequency penalty
    presence_penalty=0.5,  # default presence penalty
)

# Set up the Streamlit app
st.set_page_title("Llama Model App")
st.markdown("# Llama Model App")

# Create a text input for prompts
prompt_text = st.text_area("Enter a prompt:", height=200)

# Create a dropdown menu for tasks
tasks = ["Text Summarization", "Draft Letter/Email", "Create Meeting Minutes"]
task = st.selectbox("Choose a task:", tasks)

# Create a button to generate text
generate_button = st.button("Generate Text")

# Create a button to clear memory
clear_button = st.button("Clear Memory")

# Create a checkbox for controlling temperature
temperature_control = st.checkbox("Adjust Temperature?", value=True)
temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=groq_client.temperature)

# Create a slider for controlling top-p
top_p_slider = st.slider("Top-P", min_value=0.0, max_value=1.0, value=groq_client.top_p)

# Create a slider for controlling frequency penalty
frequency_penalty_slider = st.slider("Frequency Penalty", min_value=0.0, max_value=1.0, value=groq_client.frequency_penalty)

# Create a slider for controlling presence penalty
presence_penalty_slider = st.slider("Presence Penalty", min_value=0.0, max_value=1.0, value=groq_client.presence_penalty)

# Define a function to generate text
def generate_text(prompt, temperature = 0.9, top_p_slider = 1.0, frequency_penalty_slider =1.0, presence_penalty_slider=1.0):
    response = groq_client.compute(prompt, max_length=2048, temperature=temperature, top_p=top_p_slider, frequency_penalty=frequency_penalty_slider, presence_penalty=presence_penalty_slider)
    return response

# Define a function to clear memory
def clear_memory():
    groq_client.clear_memory()

# Render the app
if generate_button:
    if task == "Text Summarization":
        st.markdown("### Text Summarization")
        st.write(generate_text(prompt_text),temperature, top_p_slider , frequency_penalty_slider, presence_penalty_slider)
    elif task == "Draft Letter/Email":
        st.markdown("### Draft Letter/Email")
        st.write(generate_text(prompt_text),temperature, top_p_slider , frequency_penalty_slider, presence_penalty_slider)
    elif task == "Create Meeting Minutes":
        st.markdown("### Create Meeting Minutes")
        st.write(generate_text(prompt_text),temperature, top_p_slider , frequency_penalty_slider, presence_penalty_slider)

if clear_button:
    clear_memory()
