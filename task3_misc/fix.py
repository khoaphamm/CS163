import json
import re


def fix_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        # Replace the missing commas between adjacent JSON objects
        fixed_content = re.sub(r'\}\s*\{', '},{', file_content.strip())

        # Ensure the entire content is wrapped in square brackets
        if not fixed_content.startswith('['):
            fixed_content = '[' + fixed_content
        if not fixed_content.endswith(']'):
            fixed_content += ']'

        try:
            fixed_data = json.loads(fixed_content)
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(fixed_data, file, indent=4, ensure_ascii=False)
            print("JSON file fixed and saved.")
        except json.JSONDecodeError as json_err:
            print(f"JSON parsing error: {json_err}")
            # Print a snippet around the error position to help diagnose the issue
            error_pos = json_err.pos
            print("Error context:", fixed_content[max(0, error_pos - 50):error_pos + 50])
    except Exception as e:
        print(f"An error occurred: {e}")


fix_json('bus-history.json')