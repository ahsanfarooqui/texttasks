import streamlit as st
import os
from groq import Groq  # Assuming this is the correct import based on your setup

# Initialize Groq Client using the API key from environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API")
)

# Function to query the LLaMA model using Groq's chat completion
def query_llama(prompt, temperature, max_length, top_k, top_p):
    try:
        # Using client to generate chat completion with Groq API
        response = client.chat.completions.create(
            model="llama",  # Adjust based on the actual Groq model name
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_length,
            top_k=top_k,
            top_p=top_p
        )
        
        # Assuming the API returns text in a 'text' field
        return response['choices'][0]['text']  # Modify as per actual response structure
    except Exception as e:
        st.error(f"Error querying Groq model: {e}")
        return None

# Sidebar for model parameter controls
st.sidebar.title("Model Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_length = st.sidebar.slider("Max Length", 50, 500, 100)
top_k = st.sidebar.slider("Top-k", 1, 100, 50)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.95)

# Initialize session state for history and memory
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to handle different tasks (summarization, drafting, meeting minutes)
def get_task_prompt(task, user_input):
    if task == "Summarize Text":
        return f"Summarize the following text:\n{user_input}"
    elif task == "Draft a Letter":
        return f"Draft a formal letter based on this input:\n{user_input}"
    elif task == "Meeting Minutes":
        return f"Create meeting minutes from the following discussion:\n{user_input}"
    else:
        return user_input

# Clear chat and memory button
if st.sidebar.button("Clear Chat"):
    st.session_state.history = []

# Main UI elements for text input and task selection
st.title("Groq-powered LLaMA Text Utility App")
task = st.selectbox("Select Task", ["Summarize Text", "Draft a Letter", "Meeting Minutes"])
prompt = st.text_area("Enter your prompt")

# Button to submit the prompt to Groq's LLaMA model
if st.button("Submit"):
    if prompt:
        task_prompt = get_task_prompt(task, prompt)
        response = query_llama(task_prompt, temperature, max_length, top_k, top_p)
        if response:
            st.session_state.history.append({
                "task": task,
                "prompt": prompt,
                "response": response
            })

# Display chat history
st.header("Chat History")
for idx, entry in enumerate(st.session_state.history):
    st.write(f"**Task {idx + 1}:** {entry['task']}")
    st.write(f"**Prompt:** {entry['prompt']}")
    st.write(f"**Response:** {entry['response']}")
    st.write("---")

# Footer with Groq API mention
st.sidebar.write("Powered by Groq and LLaMA")
