import os

runfilePath: str = os.path.join(os.getcwd(), "build/Debug/MyProject.exe")

if __name__ == "__main__":

    if os.path.isfile(runfilePath):
        os.startfile(runfilePath)
    else:
        print("Execution file doesn't exist. Aborting...")
