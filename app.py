import streamlit as st
import os
import groq  # Assuming groq library supports LLaMA model usage

# Fetch API key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API")

# Initialize Groq Client
@st.cache_resource
def initialize_groq_client():
    if GROQ_API_KEY:
        client = groq.Client(api_key=GROQ_API_KEY)
        return client
    else:
        st.error("Groq API key not found. Please set 'GROQ_API_KEY' as an environment variable.")
        st.stop()

client = initialize_groq_client()

# Define a function to query the LLaMA model using Groq's API
def query_llama(prompt, temperature, max_length, top_k, top_p):
    try:
        # Example of how the query might work - update based on actual Groq API
        response = client.model.generate(
            model="llama", 
            prompt=prompt,
            temperature=temperature,
            max_length=max_length,
            top_k=top_k,
            top_p=top_p
        )
        return response.get("generated_text", "")
    except Exception as e:
        st.error(f"Error querying Groq model: {e}")
        return None

# Sidebar settings for the model parameters
st.sidebar.title("Model Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_length = st.sidebar.slider("Max Length", 50, 500, 100)
top_k = st.sidebar.slider("Top-k", 1, 100, 50)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.95)

# Initialize session state for history and memory
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to handle task-specific prompts
def get_task_prompt(task, user_input):
    if task == "Summarize Text":
        return f"Summarize the following text:\n{user_input}"
    elif task == "Draft a Letter":
        return f"Draft a formal letter based on this input:\n{user_input}"
    elif task == "Meeting Minutes":
        return f"Create meeting minutes from the following discussion:\n{user_input}"
    else:
        return user_input

# Clear chat and memory
if st.sidebar.button("Clear Chat"):
    st.session_state.history = []

# UI for main input and task selection
st.title("Groq-powered LLaMA Text Utility App")
task = st.selectbox("Select Task", ["Summarize Text", "Draft a Letter", "Meeting Minutes"])
prompt = st.text_area("Enter your prompt")

# Button to submit the prompt
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

# Footer displaying Groq information
st.sidebar.write("Powered by Groq and LLaMA")
