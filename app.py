import streamlit as st
import os
from groq import Groq  # Assuming this is the correct import for the Groq client

# Initialize Groq Client using the API key from environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API")
)

# Function to query the LLaMA model using Groq's chat completion
def query_llama(messages, temperature, max_tokens, top_p, frequency_penalty, presence_penalty):
    try:
        # Using client to generate chat completion with Groq API
        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Adjust to the correct model name if needed
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        st.write(response)
        # Parse the response to extract the content of the assistant's reply
        content = response['choices'][0]
        return content
    except Exception as e:
        st.error(f"Error querying Groq model: {e}")
        return None

# Sidebar for model parameter controls
st.sidebar.title("Model Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 1.0)
max_tokens = st.sidebar.slider("Max Tokens", 50, 500, 150)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.95)
frequency_penalty = st.sidebar.slider("Frequency Penalty", -2.0, 2.0, 0.0)
presence_penalty = st.sidebar.slider("Presence Penalty", -2.0, 2.0, 0.0)

# Initialize session state for chat history
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

        # Add the task prompt as a message in the conversation
        messages = [{"role": "user", "content": task_prompt}]
        
        response = query_llama(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )
        
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
