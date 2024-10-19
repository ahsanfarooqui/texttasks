import streamlit as st
import groq
import os

# Set up the Groq client
groq_client = groq.Client(api_key=os.environ['GROQ_API_KEY'])

# Set up the llama model
llama_model = groq_client.models. llama_model

# Create a Streamlit app
st.set_page_settings(
    layout="wide", 
    initial_sidebar_state="expanded", 
    default_sidebar_state="expanded"
)
st.title("Llama Model App")

# Create a sidebar with temperature and parameter controls
st.sidebar.title("Model Parameters")
temperature = st.sidebar.slider("Temperature", 0, 1, 0.5)
parameters = {}
parameters["temperature"] = temperature
parameters["prompt_len"] = st.sidebar.slider("Prompt Length", 10, 100, 50)
parameters["max_tokens"] = st.sidebar.slider("Max Tokens", 100, 1000, 500)

# Create a text input for prompts
prompt_input = st.text_area("Enter a prompt")

# Create an output area for the generated text
output_area = st.text_area("Generated Text", height=200)

# Create a chat log area to display all interactions
chat_log = st.text_area("Chat Log", height=200)

# Create a clear chat button
clear_chat_button = st.button("Clear Chat")

# Create a submit button to run the inference
submit_button = st.button("Generate Text")

# Define a function to run the inference and generate text
def generate_text(prompt):
    # Set the temperature and parameters in the llama model
    llama_model.set_temperature(temperature)
    llama_model.set_parameters(parameters)
    
    # Run the inference and get the generated text
    response = llama_model.generate(prompt, prompt_len=parameters["prompt_len"], max_tokens=parameters["max_tokens"])
    return response.text

# Define a function to clear the chat log
def clear_chat():
    chat_log.text("")

# Define a function to handle the submit button click
def submit_click():
    # Get the prompt from the input field
    prompt = prompt_input.text
    
    # Run the inference and generate text
    generated_text = generate_text(prompt)
    
    # Update the output area
    output_area.text(generated_text)
    
    # Add the interaction to the chat log
    chat_log.text(f"User: {prompt}\nLlama: {generated_text}\n---\n")
    
    # Update the chat log height
    st.session_state.chat_log_height = chat_log.height

# Define a function to handle the clear chat button click
def clear_chat_click():
    clear_chat()

# Add event listeners for the submit and clear chat buttons
if submit_button:
    submit_click()
if clear_chat_button:
    clear_chat()

# Add some example prompts and functions
st.header("Example Functions")
st.text("Text Summarization")
st.text("Draft a Letter or Email")
st.text("Create Meeting Minutes")

# Add some example prompts for each function
st.session_state.prompts = {
    "Text Summarization": "Summarize this article",
    "Draft a Letter or Email": "Draft a formal email",
    "Create Meeting Minutes": "Create meeting minutes"
}

# Create a dropdown menu for selecting the function
function_select = st.slider("Select a Function", list(st.session_state.prompts.keys()))

# Add some placeholder text for the output area
output_area.text("")

# Update the chat log height on each render
st.session_state.chat_log_height = chat_log.height
