import os
import sys
from typing import Literal, Tuple
from pathlib import Path
import subprocess

def execute_command(command):
    try:
        process = subprocess.Popen(
            ["zsh", "-c", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error: {stderr}")
        else:
            print(stdout)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    current_folder = os.path.basename(os.getcwd())
    sys.ps1 = f"DSB:{current_folder}> "

    try:
        while True:
            command: str = input(sys.ps1)

            allowed_commands: Tuple[Literal["run", "g", "pwd", "cd"]] = ("run", "g", "pwd", "cd")

            if command in allowed_commands:
                if command == "run":
                    os.system("python Index.py")
                elif command == "g":
                    os.system("git add .")
                    os.system("git commit -m 'Updated code'")
                    os.system("git push origin master")
                elif command == "pwd":
                    current_directory = os.getcwd()
                    print(f"Current folder: {current_directory}")
                elif command.startswith("cd "):
                    directory = command[3:]
                    try:
                        new_dir = Path(directory).resolve()
                        os.chdir(new_dir)
                    except FileNotFoundError:
                        print(f"Directory '{directory}' not found.")
            else:
                execute_command(command)
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
