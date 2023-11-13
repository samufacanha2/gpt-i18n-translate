# GPT-I18n-Translate

This Python script uses OpenAI's GPT-3 model to translate the contents of JSON files from English to other languages.

## Installation

First, clone the repository to your local machine:

```bash
git clone git@github.com:samufacanha2/gpt-i18n-translate.git
```

Navigate to the project directory:

```bash
cd gpt-i18n-translate
```

Install the required Python dependencies:

```bash
pip install openai python-dotenv
```

## Setting Up Environment Variables

Create a `.env` file in the root directory of the project and add your OpenAI API key:

```bash
OPENAI_API_KEY=<your_openai_api_key>
```

Replace `<your_openai_api_key>` with your actual OpenAI API key.

## Running the Code

To run the code, use the following command:

```bash
python translate.py
```

## How it Works

The script reads JSON files from a specified directory (default is ./en), translates the contents to the target languages (default is Spanish), and saves the translated contents in new JSON files in a directory named after the target language.

If the translation fails for any file, the script will prompt you to retry the translation.

## Customization

You can customize the source directory and target languages by modifying the directory and target_languages variables at the bottom of the script.

```python
# The directory containing your JSON files
directory = "./en"

# The languages you want to translate to
target_languages = ["es"]  # Spanish
```

## Note

This script only translates the values of the JSON files, not the keys. Also, it does not translate anything inside double curly braces.
