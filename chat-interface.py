import gradio as gr
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Load your OpenAI API key from environment variables or directly
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_ai(message):
    response = openai.ChatCompletion.create(
        model="your-finetuned-model-id",
        messages=[{"role": "system", "content": os.getenv('ASSISTANT_DESCRIPTION')},
                  {"role": "user", "content": message}]
    )
    return response.choices[0].message['content']

# Create Gradio interface
interface = gr.Interface(
    fn=chat_with_ai,
    inputs="text",
    outputs="text",
    title="Chat with Fine-tuned OpenAI Model"
)

# Launch the interface
interface.launch()
