import subprocess
import time
import random
import json

color_yellow = "\033[93m"
color_red = "\033[91m"
color_green = "\033[92m"
color_reset = "\033[0m"

subprocess.run(['cls'], shell=True)

print("""
  _  _      _   _    _      _      ___ _              _         
 | \| |__ _| | | |  (_)_ _ | |__  | __| |___  ___  __| |___ _ _ 
 | .` / _` | | | |__| | ' \| / /  | _|| / _ \/ _ \/ _` / -_) '_|
 |_|\_\__, |_| |____|_|_||_|_\_\  |_| |_\___/\___/\__,_\___|_|  
      |___/ Made by asisamko - limited for 2 seconds
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

message_option = input("Use custom messages? (y/n): ").lower()

messages = []

if message_option == 'y':
    # Custom messages
    print("Enter your custom messages (one per line). Press enter on an empty line to finish.")
    while True:
        message = input("> ")
        if not message:
            break
        messages.append(message)
else:
    # Default messages from wordlist
    with open("messages_sk2.txt", "r", encoding="utf-8") as file:
        messages = file.readlines()

if not messages:
    print("No messages found.")
    exit()

# Combine custom messages and default messages
all_messages = messages + [random.choice(messages).strip() for _ in range(msgcount - len(messages))]
random.shuffle(all_messages)

curl_command = [
    'curl',
    "-s",
    '-X', 'POST',
    '-H', 'Content-Type: application/json',
    '-H', 'Accept: application/json',
    '-d', '{{"username": "{}", "question": "{{message}}", "deviceId": "error"}}'.format(username, ''),
    'https://ngl.link/api/submit'
]

counter = 1

try:
    for message in all_messages[:msgcount]:
        # Encode the message using json.dumps
        encoded_message = json.dumps(message)
        # Remove the surrounding quotes added by json.dumps
        encoded_message = encoded_message[1:-1]
        
        curl_command[9] = '{{"username": "{}", "question": "{}", "deviceId": "example_deviceid"}}'.format(username, encoded_message)

        try:
            output = subprocess.check_output(curl_command, stderr=subprocess.STDOUT)
            print(output.decode('utf-8'))
            if "Message successfully sent" in output.decode('utf-8'):
                print(f"{counter}. Message sent successfully." + color_reset)
            else:
                print(f"{counter}. Something went wrong.")
            counter += 1

            time.sleep(2)
        except subprocess.CalledProcessError as e:
            print(f"Error executing cURL command: {e}")
except Exception as ex:
    print(f"An error occurred: {ex}")
