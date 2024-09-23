import json
import re
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
# Set up your OpenAI API key
client = OpenAI(api_key=api_key)
# Load the DEBUG environment variable, defaulting to False if not set
DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'

def debug_log(message):
    """Helper function to print logs only if DEBUG is enabled."""
    if DEBUG:
        print(message)

def clean_text(text):
    """
    Cleans up text by removing problematic encoded characters and correcting escaped sequences.
    """
    # Decode the text into a readable format
    text = text.encode('latin1').decode('utf-8')

    # Remove problematic encoding artifacts (like \u00c2)
#     text = re.sub(r'\\u00[89A-Za-z][0-9A-Fa-f]', '', text)

    # Remove any remaining escaped sequences like \" or excess spaces
#     text = text.replace('\\"', '"')

    return text

def generate_prompt_with_openai(post_body):
    """
    Sends the post body to OpenAI to generate a custom prompt for the entry using the new chat-based API.
    """
    try:
        # Use OpenAI's new ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4",  # Or gpt-3.5-turbo depending on your access
            messages=[
                {"role": "system", "content": "You are an assistant who helps create training prompts for an ai that will help us make a social media post creation bot. All prompts should be from the perspective of a social media manager, including things like 'Create a post about' or 'Here is something that is happening, make a post about it' "},
                {"role": "user", "content": f"Generate a prompt question (plain text only, one or two sentences, no quotes) based on this post: '{post_body}' "}
            ],
            max_tokens=50
        )

        # Accessing the correct part of the response
        prompt = response.choices[0].message.content.strip()



        # Print the prompt to ensure it's being generated
        debug_log(f"Generated Prompt: {prompt}")

        return prompt

    except Exception as e:
        debug_log(f"Error generating prompt: {e}")
        return None

def clean_input_with_openai(post_body):
    """
    Sends the post body to OpenAI to generate a custom prompt for the entry using the new chat-based API.
    """
    try:
        # Use OpenAI's new ChatCompletion API
        response = client.chat.completions.create(
            model="gpt-4",  # Or gpt-3.5-turbo depending on your access
            messages=[
                {"role": "system", "content": os.getenv('CLEANUP_INSTRUCTIONS')},
                {"role": "user", "content": f"Clean up this post and return it properly formatted text for use in the content field of a jsonl file for training openai: '{post_body}' "}
            ]
        )

        # Accessing the correct part of the response
        prompt = response.choices[0].message.content.strip()

        # Remove any surrounding quotes that are already in the prompt
        if prompt.startswith('"') and prompt.endswith('"'):
            prompt = prompt[1:-1]

        # Remove all double quotes in the prompt
            prompt = prompt.replace('"', '')

        # Print the prompt to ensure it's being generated
        debug_log(f"Generated Prompt: {prompt}")

        return prompt

    except Exception as e:
        debug_log(f"Error generating prompt: {e}")
        return None

def process_json(input_file, output_file):
    # Load the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Open the output JSONL file
    with open(output_file, 'w') as output:
        for post in data:
            post_title = post.get('title', '')

            # Skip posts that are just sharing links
            if 'shared a link' in post_title.lower():
                debug_log(f"Skipping post with title: {post_title}")  # Debugging: Check what is being skipped
                continue

            # Extract post body or description
            post_body = post.get('data', [{}])[0].get('post', '')

            if post_body:
                # Clean the post body text
                post_body = clean_text(post_body)

                # Print post body to ensure it's not empty
                debug_log(f"Processing Post Body: {post_body}")

                # Generate the prompt using OpenAI API
                prompt = generate_prompt_with_openai(post_body)
                completion = post_body

                if prompt and completion:
                    # Construct the chat-based format with system, user, and assistant roles
                    output_entry = {
                        "messages": [
                            {"role": "system", "content": os.getenv('ASSISTANT_DESCRIPTION')},
                            {"role": "user", "content": prompt},
                            {"role": "assistant", "content": completion}
                        ]
                    }
                    # Write to the output file in JSONL format
                    output.write(json.dumps(output_entry) + '\n')
                    print(f"Writing to file: {output_entry}")  # Debugging: Confirm writing to file
                else:
                    debug_log(f"Prompt generation failed for post: {post_body}")
            else:
                debug_log("Post body is empty or not found.")

# Call the function to process the JSON file
process_json(os.getenv('INPUT_FILE'), os.getenv('OUTPUT_FILE'))
