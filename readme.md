# Social Media Post Generator Using OpenAI

This project allows you to generate and fine-tune a model to create engaging social media posts using OpenAI's API. The script converts a dataset into the correct format, generates prompts and completions, and even fine-tunes a model based on your needs.

## Prerequisites

Before getting started, ensure you have the following:
- **Python 3.7+** installed on your machine.
- An OpenAI account and an API key.

### Step 1: Check if Python is Installed

You can check if Python is installed by running the following command in your terminal or command prompt:

```bash
python --version
```
This should display the Python version, such as Python 3.x.x. If Python is not installed, download and install it from the official website: [Download Python](https://www.python.org/downloads/).

### Step 2: Install Required Python Packages

Once you have Python installed, you will need to install the required packages. First, ensure you have pip, the Python package manager, installed by running:

```bash
pip --version
```
If pip is installed, you should see a version number. Next, install the required dependencies by running:
    
    ```bash
pip install -r requirements.txt
```

If you don’t have the requirements.txt file, install the following packages manually:

```bash
pip install openai python-dotenv
```

### Step 3: Generate an OpenAI API Key

To use OpenAI’s API, you need an API key. Follow these steps to generate one:

1. Go to the [OpenAI API keys page](https://platform.openai.com/account/api-keys).
2. Click **Create new secret key**.
3. Copy the generated API key and paste it into the `.env` file you set up earlier as the value for `OPENAI_API_KEY`.

### Step 4: Get Your Facebook Post Data

For more information, check out the [detailed guide](./retrieve-fb-data.md).

After we ran that process, the file we started with was called profile_posts_1.json - import that into your project directory, and if it has a different name, update that in ```.env```

### Step 4: Set Up the `.env` File

The script requires an API key from OpenAI, which is stored in a `.env` file. This file holds environment variables that are kept separate from the code for security purposes.

1. **Rename the `.env.example` file:**

   In your project directory, rename the `.env.example` file to `.env`. You can do this from the command line or manually:

   - **Command line:**
        
       ```bash
       mv .env.example .env
       ```
   - **Manually:**
     - Locate the `.env.example` file in your project folder.
     - Rename it to `.env`.

2. **Add your OpenAI API key:**

   Open the `.env` file and add your OpenAI API key:
    
    ```bash
    OPENAI_API_KEY=your-api-key-here
    ```

3. **Tune any values to your needs:**
   
   For example, in our social posts some are in spanish, so we added 'translate from spanish to english' to our post cleaning instructions.  Also, make sure you put your company or purpose in the assistant variable. 

### Step 5: Run the Script

Once the environment variables and dependencies are set up, you can run the script to generate social media posts.

```bash
python social-trainer.py
```
If you didn't change the env variable, this should output 'social-training-data.jsonl'

### Step 6: Training a Model

If you’re fine-tuning a model using the dataset:

1. Ensure your training data is in JSONL format and follows OpenAI’s format for chat models.
- Each line in your training file should look like this:
        
    ```json
       {
        "messages": [
            {"role": "system", "content": "You are an assistant that helps create engaging social media posts."},
            {"role": "user", "content": "Create a post about something."},
            {"role": "assistant", "content": "This is an awesome post about something"}
        ]
        }
    ```
2. To upload your training file and fine-tune your model, use the OpenAI API:
    - Follow OpenAI’s [fine-tuning guide](https://platform.openai.com/docs/guides/fine-tuning) for detailed instructions on how to fine-tune the model.

### Step 7: Loading Your Fine-Tuned Model

Once your model is fine-tuned, you can load it by referencing its model ID. To generate prompts and completions using your fine-tuned model, make sure to update the model ID in the `generate_prompt_with_openai` function:
    
```python
    response = client.chat.completions.create(
        model="your-fine-tuned-model-id",  # Use your fine-tuned model ID here
        messages=[
            {"role": "system", "content": "You are an assistant that helps create engaging social media posts."},
            {"role": "user", "content": post_body}
        ],
    max_tokens=1024
    )
```
### Debugging (Optional)

If you want to enable logging for debugging purposes, you can modify the `.env` file by setting the `DEBUG` variable to `true`:
    
```bash
DEBUG=true
```

This will activate log messages in the script.

```
    ├── .env
    ├── .env.example
    ├── script.py
    ├── requirements.txt
    ├── social-training-data.jsonl
    └── README.md
```

### Troubleshooting

1. **Invalid API Key Error:**
    - Ensure you correctly added the API key to the `.env` file. Check for any extra spaces or incorrect values.

2. **Model Upload Error:**
    - Make sure your training dataset is in the correct JSONL format and follows OpenAI’s data formatting guidelines.

3. **Token Limit Errors:**
    - Check the length of your prompt and completion to ensure they don’t exceed the model’s token limit (for GPT-4, the total limit is 8192 tokens).

### Additional Resources

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Python-dotenv Documentation](https://saurabh-kumar.com/python-dotenv/)
- [JSONL File Format](https://jsonlines.org/)

By following the instructions in this README, you should be able to easily set up the project, fine-tune your model, and generate engaging social media posts. Happy coding!
