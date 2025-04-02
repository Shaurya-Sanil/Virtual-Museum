import tkinter as tk
from tkinter import scrolledtext
import subprocess
import openai
import pyttsx3

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Function to handle TTS


def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to open other Python files (rooms)


def open_room(file_name):
    try:
        subprocess.Popen(["python", file_name])
    except FileNotFoundError:
        chat_display.insert(tk.END, f"Tour Guide: Sorry, the {
                            file_name} room is not available right now.\n")
        speak_text(f"Sorry, the {file_name} room is not available right now.")

# Function to process user input


def process_user_input():
    user_input = input_box.get("1.0", tk.END).strip()
    if user_input:
        chat_display.insert(tk.END, f"You: {user_input}\n")
        input_box.delete("1.0", tk.END)

        # Generate response from ChatGPT
        response = generate_chat_response(user_input)
        chat_display.insert(tk.END, f"Tour Guide: {response}\n")
        speak_text(response)

        # Check for room navigation commands
        if "library" in user_input.lower():
            open_room("library_room.py")
        elif "research room" in user_input.lower():
            open_room("research_room.py")
        elif "cultural floor" in user_input.lower():
            open_room("cultural_floor.py")

# Function to generate ChatGPT response


def generate_chat_response(prompt):
    # Replace with your OpenAI API key
    openai.api_key = "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"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful Virutal museum tour guide.You can take the user to the library , research room or the cultural room floor. Dont give very lengthy answers to keep it interesting but answer the questions of the user and dont make use of any emojis"},
                {"role": "user", "content": prompt},
            ],
        )
        reply = response['choices'][0]['message']['content']

        return reply
    except Exception as e:
        return "Ok"


# Main Tkinter Window
root = tk.Tk()
root.title("Museum Lobby")
root.geometry("900x650")
root.configure(bg="#F7E9D7")

# Header
header = tk.Label(
    root, text="Welcome to the Museum Lobby", font=("Georgia", 28, "bold"), bg="#6C4A35", fg="white", pady=15
)
header.pack(fill=tk.X)

# Buttons for Navigation
button_frame = tk.Frame(root, bg="#F7E9D7")
button_frame.pack(pady=30)


def create_nav_button(text, room_file):
    button = tk.Button(
        button_frame,
        text=text,
        font=("Georgia", 16),
        bg="#6C4A35",
        fg="white",
        padx=20,
        pady=15,
        relief=tk.RAISED,
        command=lambda: open_room(room_file),
    )
    button.pack(side=tk.LEFT, padx=15)


create_nav_button("Library", "library_room.py")
create_nav_button("Research Room", "research_room.py")
create_nav_button("Cultural Floor", "cultural_floor.py")

# ChatGPT Chatbox
chat_frame = tk.Frame(root, bg="#F7E9D7")
chat_frame.pack(pady=10, fill=tk.BOTH, expand=True)

chat_display = scrolledtext.ScrolledText(
    chat_frame, wrap=tk.WORD, font=("Georgia", 14), height=15, bg="#FAF3E0")
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Starter message
starter_message = (
    "Tour Guide: Welcome to the Museum! I’m here to guide you. You can ask me questions about the museum or I can take you to the rooms you want .\n"
)
chat_display.insert(tk.END, starter_message)
speak_text("Welcome to the Museum! I’m here to guide you. You can ask me questions about the museum or I can take you to the rooms you want .")

input_frame = tk.Frame(root, bg="#F7E9D7")
input_frame.pack(fill=tk.X, padx=10, pady=10)

input_box = tk.Text(input_frame, height=3, font=("Georgia", 14), bg="#FAF3E0")
input_box.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

send_button = tk.Button(
    input_frame, text="Send", font=("Georgia", 14, "bold"), bg="#6C4A35", fg="white", command=process_user_input
)
send_button.pack(side=tk.RIGHT, padx=5)

# Run the Tkinter main loop
root.mainloop()
