
import os

def update_dropbox_token():
    """
    Updates the Dropbox access token in the generate_Graber.py script.
    """
    new_token = input("Please enter your new Dropbox access token: ")

    if not new_token.startswith("sl."):
        print("Invalid Dropbox token format. It should start with 'sl.'.")
        return

    try:
        with open("tools/generate_Graber.py", "r", encoding="utf-8") as f:
            lines = f.readlines()

        token_line_index = -1
        for i, line in enumerate(lines):
            if "DROPBOX_ACCESS_TOKEN =" in line:
                token_line_index = i
                break

        if token_line_index == -1:
            print("Error: Could not find the DROPBOX_ACCESS_TOKEN line in generate_Graber.py.")
            return

        lines[token_line_index] = f'    DROPBOX_ACCESS_TOKEN = "{new_token}"\n'

        with open("tools/generate_Graber.py", "w", encoding="utf-8") as f:
            f.writelines(lines)

        print("Successfully updated the Dropbox access token in generate_Graber.py.")

    except IOError as e:
        print(f"Error updating the file: {e}")

if __name__ == "__main__":
    update_dropbox_token()
