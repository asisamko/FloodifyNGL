import subprocess
import random
import time

# Clean up console
def clear_console():
    subprocess.run(['cls'], shell=True)
clear_console()

print("""
  _  _      _   _    _      _      ___ _              _         
 | \| |__ _| | | |  (_)_ _ | |__  | __| |___  ___  __| |___ _ _ 
 | .` / _` | | | |__| | ' \| / /  | _|| / _ \/ _ \/ _` / -_) '_|
 |_|\_\__, |_| |____|_|_||_|_\_\  |_| |_\___/\___/\__,_\___|_|  
      |___/                                                    
""")

# User inputs
username = input("Enter username: ")

# Validate msgcount input
while True:
    msgcount = input("Amount of messages: ")
    if not msgcount.isdigit():
        print("Only numbers are allowed. Please try again.")
    else:
        msgcount = int(msgcount)
        if msgcount <= 0:
            print("Please enter a positive number.")
        else:
            break

# Read messages from file
with open("messages.txt", "r", encoding="utf-8") as file:
    messages = file.readlines()

# Validate msgcount is within range
if msgcount > len(messages):
    print("Error: Insufficient number of messages in the file.")
    exit()

msgdelay = input("Delay in seconds: ")

curl_command = [
    'curl',
    "-s",
    '-X', 'POST',
    '-H', 'Content-Type: application/json',
    '-H', 'Accept: application/json',
    '-d', '{{"username": "{}", "question": "{{message}}", "deviceId": "example_deviceid"}}'.format(username),
    'https://ngl.link/api/submit'
]

counter = 1

try:
    for _ in range(msgcount):
        message = random.choice(messages).strip()
        curl_command[9] = '{{"username": "{}", "question": "{}", "deviceId": "example_deviceid"}}'.format(username, message)
        
        try:
            result = subprocess.run(curl_command, capture_output=True, text=True)
            output = result.stdout
            if result.returncode == 0:
                print(f"{output}")
                print(f"{counter}. Message has been successfully sent!")
            else:
                print(f"Error executing cURL command: {result.stderr}")
                print(f"{counter}. Something went wrong.")
            counter += 1
        except subprocess.CalledProcessError as e:
            print(f"Error executing cURL command: {e}")
except Exception as ex:
    print(f"An error occurred: {ex}")
