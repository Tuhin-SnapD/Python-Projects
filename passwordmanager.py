"""
This code is a simple password manager that allows a user to store and retrieve passwords in an encrypted format.

The program uses the Fernet class from the cryptography library to encrypt and decrypt passwords with a generated encryption key.

The program allows the user to choose between two options: "view" to view existing passwords or "add" to add a new password.

When the "view" option is selected, the program opens the passwords.txt file in read mode and loops through each line in the file. For each line, 
the program splits the line into the username and encrypted password, decrypts the password using the loaded encryption key, and prints the 
username and password.

When the "add" option is selected, the program prompts the user for an account name and password, encrypts the password using the loaded 
encryption key, and appends the account name and encrypted password to the passwords.txt file.

The program also includes functions to generate a new encryption key and load the encryption key from a file. The program checks whether the key 
file exists and generates a new key if it does not exist, or loads the key from the file if it does exist.

The program runs in an infinite loop until the user chooses to quit by entering 'q'.
"""

# Import the Fernet class from the cryptography library
from cryptography.fernet import Fernet

# Import the os module to work with the file system
import os


# Function to generate a new encryption key and save it to a file
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


# Function to load the encryption key from the file
def load_key():
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key


# Function to view the stored passwords
def view():
    try:
        # Open the passwords file in read mode
        with open('passwords.txt', 'r') as f:
            # Loop through each line in the file
            for line in f:
                # Remove any trailing whitespace characters from the line
                data = line.rstrip()
                # Split the line into the username and encrypted password
                user, passw = data.split("|")
                try:
                    # Decrypt the password using the loaded encryption key and print the username and password
                    print("User:", user, "| Password:",
                          fer.decrypt(passw.encode()).decode())
                except:
                    # If there is an error decrypting the password, print an error message
                    print("Error decrypting password:", passw)
    except FileNotFoundError:
        # If the passwords file is not found, print an error message
        print("Passwords file not found.")


# Function to add a new password
def add():
    # Prompt the user for the account name and password
    name = input('Account Name: ')
    pwd = input("Password: ")

    # Open the passwords file in append mode and write the account name and encrypted password
    with open('passwords.txt', 'a') as f:
        f.write(name + "|" + fer.encrypt(pwd.encode()).decode() + "\n")


# Generate or load encryption key
if not os.path.exists("key.key"):
    # If the key file does not exist, generate a new key and save it to the file
    write_key()

key = load_key()
fer = Fernet(key)

# Main loop to prompt the user for what action to perform
while True:
    mode = input(
        "Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
    if mode == "q":
        # If the user enters 'q', break out of the loop and exit the program
        break

    if mode == "view":
        # If the user enters 'view', call the view() function to display the stored passwords
        view()
    elif mode == "add":
        # If the user enters 'add', call the add() function to add a new password
        add()
    else:
        # If the user enters an invalid command, print an error message and continue to the next iteration of the loop
        print("Invalid mode.")
        continue