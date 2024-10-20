import streamlit as st
import os
from groq import Groq  # Assuming this is the correct import for the Groq client

# Initialize Groq Client using the API key from environment variables
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
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
        
        # Parse the response to extract the content of the assistant's reply
        content = response.choices[0].message.content
        return content
    except Exception as e:
        st.error(f"Error querying Groq model: {e}")
        return None

# Sidebar for model parameter controls (LEFT SIDEBAR)
st.sidebar.title("Model Parameters")
temperature = st.sidebar.slider("Temperature", 0.0, 2.0, 1.0)
max_tokens = st.sidebar.slider("Max Tokens", 50, 1000, 150)
top_p = st.sidebar.slider("Top-p", 0.0, 1.0, 0.95)
frequency_penalty = st.sidebar.slider("Frequency Penalty", -2.0, 2.0, 0.0)
presence_penalty = st.sidebar.slider("Presence Penalty", -2.0, 2.0, 0.0)

# Initialize session state for chat history
if 'history' not in st.session_state:
    st.session_state.history = []

# Function to handle different tasks (summarization, drafting, meeting minutes, etc.)
def get_task_prompt(task, user_input):
    if task == "Summarize Text":
        return f"Summarize the following text:\n{user_input}"
    elif task == "Draft a Letter":
        return f"Draft a formal letter based on this input:\n{user_input}"
    elif task == "Meeting Minutes":
        return f"Create meeting minutes from the following discussion:\n{user_input}"
    elif task == "Rephrase Text":
        return f"Rephrase the following text:\n{user_input}"
    elif task == "Generate Ideas":
        return f"Generate creative ideas based on the following topic:\n{user_input}"
    elif task == "Create a Story":
        return f"Write a short story based on the following prompt:\n{user_input}"
    elif task == "Write a Blog Post":
        return f"Write a blog post about:\n{user_input}"
    else:
        return user_input

# Clear chat and memory button
if st.sidebar.button("Clear Chat"):
    st.session_state.history = []

# Main UI elements for text input and task selection
st.title("Draft Buddy")
task = st.selectbox("Select Task", [
    "Summarize Text",
    "Draft a Letter",
    "Meeting Minutes",
    "Rephrase Text",
    "Generate Ideas",
    "Create a Story",
    "Write a Blog Post"
])
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

# CSS for chat bubble styles
st.markdown("""
    <style>
    .user-bubble {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
        max-width: 80%;
    }
    .assistant-bubble {
        background-color: #F1F0F0;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        text-align: left;
        max-width: 80%;
        margin-left: auto;
    }
    .container {
        display: flex;
        flex-direction: column;
    }
    </style>
""", unsafe_allow_html=True)

# Collapsible history section on the right side of the main interface
with st.expander("📜 Show Chat History", expanded=False):
    st.write("Chat History:")
    for idx, entry in enumerate(st.session_state.history):
        st.markdown(f'<div class="container"><div class="user-bubble"><strong>User:</strong> {entry["prompt"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="container"><div class="assistant-bubble"><strong>Assistant:</strong> {entry["response"]}</div></div>', unsafe_allow_html=True)
        st.write("---")

# Display only the latest response at the bottom
if st.session_state.history:
    latest_response = st.session_state.history[-1]['response']
    st.subheader("Latest Response")
    st.write(latest_response)
