import os
import sys
import subprocess
from typing import Literal, Tuple
from pathlib import Path
from colorama import Fore, Style, init

try:
    from colorama import Fore, Style, init
except ImportError:
    print("Required packages are not installed. Some features may not work correctly.")

init(autoreset=True)

class CommandExecutor:
    @staticmethod
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
                print(f"{Fore.RED}Error: {stderr}")
            else:
                print(f"{Fore.GREEN}{stdout}")

        except Exception as e:
            print(f"{Fore.RED}An error occurred: {str(e)}")

def main():
    current_folder = os.path.basename(os.getcwd())
    sys.ps1 = f"{Fore.CYAN}DSB:{current_folder}>{Style.RESET_ALL} "

    try:
        while True:
            command: str = input(sys.ps1)

            if command.lower() == "exit":
                print(f"{Fore.YELLOW}Exiting the program.")
                break

            allowed_commands: Tuple[Literal["run", "git", "pwd", "cd", "exit"]] = ("run", "git", "pwd", "cd", "exit")

            if command in allowed_commands:
                if command == "run":
                    os.system("python Index.py")
                elif command == "git":
                    os.system("git add .")
                    os.system("git commit -m 'Updated code'")
                    os.system("git push origin master")
                elif command == "pwd":
                    current_directory = os.getcwd()
                    print(f"Current folder: {Fore.CYAN}{current_directory}{Style.RESET_ALL}")
                elif command.startswith("cd "):
                    directory = command[3:]
                    try:
                        new_dir = Path(directory).resolve()
                        os.chdir(new_dir)
                    except FileNotFoundError:
                        print(f"{Fore.RED}Directory not found.")
            else:
                CommandExecutor.execute_command(command)

    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}\nProgram terminated by the user.")

if __name__ == "__main__":
    main()
