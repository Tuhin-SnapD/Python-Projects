""" 
This code is a Python script that uses the subprocess module to call the wsay command-line tool and speak the input phrase provided by the user.

It first welcomes the user to the program, then enters into an infinite loop that prompts the user to enter a phrase to be spoken. If the user 
inputs "q", the program uses subprocess.run() to call wsay and speak "bye, nice talking to you" before exiting the loop and terminating the 
program. If the user inputs any other phrase, the program constructs a command string using the f-string syntax with the input phrase as an 
argument to wsay, and then calls the subprocess.run() function to execute the command and speak the input phrase.

wsay is a command-line tool on Windows (https://github.com/p-groarke/wsay/releases) that is used to speak out loud the input text using the 
system's built-in text-to-speech functionality. When wsay is called with a string argument, it converts the string to speech and speaks it out 
loud through the system's audio output.

In the code provided, the subprocess module is used to call wsay with the user's input phrase and speak it out loud. The shell=True argument in 
the subprocess.run() function is used to execute the wsay command in a shell environment so that the wsay program is recognized as a command.
"""

# Import necessary modules
import subprocess

if __name__ == '__main__':
    print("RoboTalker")

    while True:
        # Get user input
        phrase = input("Type the phrase you want me to say: ")

        # Check if user wants to quit
        if phrase == "q":
            subprocess.run(['wsay', 'bye, nice talking to you'])
            break

        # Speak the user's input
        command = f'wsay "{phrase}"'
        subprocess.run(command, shell=True)
