import os 

if __name__ == "__main__":
    try:
        while True:
            command = input("DSB:> ")
            if command == "run":
                os.system("python Index.py")
            else:
                os.system(command)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
