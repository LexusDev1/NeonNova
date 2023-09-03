import os
from typing import Literal, Tuple

if __name__ == "__main__":
    try:
        while True:
            command: str = input("DSB:> ")
            
            allowed_commands: Tuple[Literal["run", "g"]] = ("run", "g")

            if command in allowed_commands:
                if command == "run":
                    os.system("python Index.py")
                elif command == "g":
                    os.system("git add .")
                    os.system("git commit -m 'Updated code'")
                    os.system("git push origin main")
            else:
                os.system(command)
    except KeyboardInterrupt:
        print("\nProgram terminated by the user.")
