import os
import csv
import re
import bcrypt

debug = True
listUsers = []
reference_db=""

# Check if 'users.csv' exists, and create it if it doesn't
if not os.path.isfile('users.csv'):
    with open('users.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Username', 'Password', 'Database'])
    if debug:
        print("Created 'users.csv' as it didn't exist.")

def validatePassword(password, username):
    """Password validation"""
    if password == username:
        print("Error: Password cannot be the same as the username.")
        return False
    if len(password) < 8:
        print("Password must be at least 8 characters long.")
        return False
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one capital letter.")
        return False
    if not re.search(r"[0-9]", password):
        print("Password must contain at least one number.")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password must contain at least one symbol.")
        return False
    return True

def check_username_exists(username, filename):
    """Check if username already exists in the CSV"""
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                return True
    return False

def signUp(username, password, confirm_password):
    if debug: 
        print("--Sign Up--")
        print(f"Entered data Username: {username}.")

    if not validatePassword(password, username):
        return False

    if password != confirm_password:
        print("Passwords do not match.")
        return False

    if check_username_exists(username, 'users.csv'):
        print("Username already exists. Please choose another username.")
        return False

    print("Account created successfully.")

    """Encrypt the password"""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_data = {'Username': username, 'Password': hashed_password.decode('utf-8')}
    listUsers.append(user_data)
    
    """Write to CSV file"""
    with open('users.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, user_data['Password']])
    
    if debug:
        print(f"User {username} added to database.")
    
    return True

def login(username, password):
    """Login function to authenticate users"""
    with open('users.csv', mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username:
                stored_password = row['Password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                    print("Login successful!")
                    return True
                else:
                    print("Incorrect password. Please try again.")
                    return False
        print("Username not found. Please sign up first.")
        return False

def homeScreen():
    if debug: 
        print("--Home Screen--")
    """Once the credentials are confirmed, this will make the program accessible."""

if __name__ == "__main__":
    if debug: 
        print("Progress Started")
    
    while True:
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice (1/2/3): ")

        if choice == '1':
            strUsername = input("Enter Username: ")
            strPassword = input("Enter Password: ")
            strConfirmPassword = input("Confirm Password: ")    
            if signUp(strUsername, strPassword, strConfirmPassword):
                print("Please log in with your new credentials.")
        elif choice == '2':
            strUsername = input("Enter Username: ")
            strPassword = input("Enter Password: ")
            if login(strUsername, strPassword):
                break
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
