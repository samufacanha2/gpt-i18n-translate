import os
import json

from openai import OpenAI, OpenAIError
from dotenv import load_dotenv

from utils import yes_values, no_values, bcolors

load_dotenv()

os.system("cls" if os.name == "nt" else "clear")

print(f'\nAPI Key: {os.environ["OPENAI_API_KEY"]} \n')

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


def translate_text(text, model="gpt-3.5-turbo", target_language="es"):
    """
    Function to translate text using OpenAI's translation capabilities.
    """
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": f"Translate the values of following dictionary(en) text to {target_language}: {text} \n don't translate the dictionary keys. do not translate what is inside the double curly braces {{ like this }}. Don't write anything else than the translation.",
                },
            ],
        )
        if completion.choices[0].message.content is None:
            return None

        translation = completion.choices[0].message.content.strip()
        translation = translation[translation.find("{") : translation.rfind("}") + 1]
        return translation
    except OpenAIError as e:
        print(f"Error in translating text: {e}")
        return None


def translate_and_save_files(directory, target_languages, failed_files=None):
    """
    Function to translate the contents of JSON files in a directory to the target languages.
    """

    all_contents = {}

    if failed_files is None:
        failed_files = []

        # Recursively read and store the contents of each JSON file
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith(".json"):
                    file_path = os.path.join(root, filename)
                    if os.stat(file_path).st_size == 0:
                        continue

                    with open(file_path, "r", encoding="utf-8") as file:
                        # Construct a unique identifier for the file
                        relative_path = os.path.relpath(file_path, directory)
                        all_contents[relative_path] = json.load(file)
    else:
        # Load only the contents of the failed files
        for file_path, _ in failed_files:
            file_path = os.path.join(directory, file_path.replace("_", os.sep))
            with open(file_path, "r", encoding="utf-8") as file:
                all_contents[file_path] = json.load(file)

    new_failed_files = []

    for lang in target_languages:
        lang_directory = os.path.join(f"./{lang}")
        if not os.path.exists(lang_directory):
            os.makedirs(lang_directory)

        for file_path, content in all_contents.items():
            original_file_path = file_path
            current_directory = lang_directory
            while "/" in file_path[2:]:
                current_directory = os.path.join(
                    current_directory, file_path[: file_path.find("/")]
                )
                if not os.path.exists(current_directory):
                    os.makedirs(current_directory)
                file_path = file_path[file_path.find("/") + 1 :]

            translated_content = translate_text(
                json.dumps(content), target_language=lang
            )

            if translated_content is None or translated_content == "":
                new_failed_files.append((file_path, lang))
                continue

            translated_file_path = os.path.join(lang_directory, original_file_path)
            with open(translated_file_path, "w", encoding="utf-8") as file:
                try:
                    json.dump(
                        json.loads(translated_content),
                        file,
                        ensure_ascii=False,
                        indent=2,
                    )
                except:
                    new_failed_files.append((file_path, lang))
                    continue

            print(
                f"File {bcolors.OKCYAN} {translated_file_path} {bcolors.ENDC} translated to {bcolors.OKGREEN} {lang} {bcolors.ENDC} successfully."
            )

    if new_failed_files:
        retry_failed_translations(directory, new_failed_files)


def retry_failed_translations(directory, failed_files):
    """
    Function to retry translating the failed files.
    """
    print(
        f" {bcolors.FAIL} \n\n\tFailed to translate the following files:  {bcolors.ENDC}"
    )
    for filename, lang in failed_files:
        print(f" {bcolors.FAIL} \t\t{filename} to {lang} {bcolors.ENDC}")

    print("\n\tDo you want to retry translating the failed files? (y/n)\n")

    while True:
        retry = input("\t> ").lower()
        if retry in yes_values:
            translate_and_save_files(
                directory, [lang for _, lang in failed_files], failed_files
            )
            break
        elif retry in no_values:
            print("Exiting...")
            break
        else:
            print(
                f"\n {bcolors.WARNING} Invalid input, please type 'y' or 'n'. {bcolors.ENDC} \n"
            )


# The directory containing your JSON files
directory = "./en"

# The languages you want to translate to
target_languages = ["es"]  # Example for Spanish

translate_and_save_files(directory, target_languages)
