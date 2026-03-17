# run.py
import sys
import os
import subprocess

def main():
    """
    Launcher script for the cut-doc utility.
    Passes arguments directly to the CLI.
    """
    # Ensure the script is run with a name argument
    if len(sys.argv) < 2:
        print("Usage: python run.py \"<Name to Search>\" [--pdf-folder <path>] [--output-folder <path>] [--no-pdf]")
        sys.exit(1)

    # Construct the command to run the cut_doc.cli module
    # The first argument to python is '-m' to run a module as a script
    command = [sys.executable, "-m", "cut_doc.cli"] + sys.argv[1:]

    print(f"Running command: {' '.join(command)}")

    # Execute the command
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'python' executable not found. Make sure Python is in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    main()
