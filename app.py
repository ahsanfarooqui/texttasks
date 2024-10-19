import streamlit as st
import groq
from transformers import LLaMAForConditionalGeneration, LLAMATokenizer
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer
tokenizer = LLAMATokenizer.from_pretrained("llama-base")
model = LLaMAForConditionalGeneration.from_pretrained("llama-base")

# Initialize the model client using GROQ API client
groq_key = st.secrets["GROQ_API_KEY"]
client = groq.Client(key=groq_key)

# Function to generate text from the prompt
def generate_text(prompt, temperature=0.9, max_length=256):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs=inputs, max_length=max_length, temperature=temperature, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Main function
if __name__ == "__main__":
    st.title("LLaMA Text Generation App")

    # Choose the task for this text generation
    task = st.selectbox("Choose the task", ["Summarization", "Drafting a letter", "Creating meeting minutes"])

    # Define the prompts based on the task chosen
    if task == "Summarization":
        prompt = "Please summarize this article..."
    elif task == "Drafting a letter":
        prompt = "Please draft a letter to..."
    elif task == "Creating meeting minutes":
        prompt = "Please create meeting minutes for..."

    # Get the user input for the prompt
    user_input = st.text_input("Please provide the prompt")

    # Combine the prompt and user input
    prompt = prompt + user_input

    # Get the temperature value from the user
    temperature = st.slider("Temperature", 0.0, 1.0)

    # Get the maximum length of the generated text
    max_length = st.slider("Maximum Length", 100, 256)

    # Generate the text
    generated_text = generate_text(prompt, temperature, max_length)

    # Display the generated text
    st.write(f"Generated Text: {generated_text}")

    # Load the interaction history
    interaction_history = st.experimental_get_query_params()

    # Display the interaction history
    st.write("Interaction History:")
    for key, value in interaction_history.items():
        st.write(f"{key}: {value}")

    # Function to clear the memory
    def clear_memory():
        interaction_history = {}
        st.experimental_set_query_params(interaction_history)

    # Create a button to clear the memory
    clear_button = st.button("Clear Memory")
    if clear_button:
        st.experimental_set_query_params(interaction_history={})
