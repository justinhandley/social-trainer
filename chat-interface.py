import gradio as gr
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Load your OpenAI API key and fine-tuned model ID from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
model_id = os.getenv("FINETUNED_MODEL")

# Check if the model ID is loaded correctly
if not model_id:
    raise ValueError("Fine-tuned model ID not found. Make sure FINETUNED_MODEL is set in your .env file.")

def chat_with_ai(message):
    try:
        response = openai.ChatCompletion.create(
            model=model_id,  # Use the model ID loaded from environment variable
            messages=[
                {"role": "system", "content": "You are a helpful assistant for Silvermouse."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message['content']

    # Catch all exceptions and display a friendly error message
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Create Gradio interface
interface = gr.Interface(
    fn=chat_with_ai,
    inputs="text",
    outputs="text",
    title="Chat with Silvermouse AI Assistant"
)

# Launch the interface
interface.launch()
