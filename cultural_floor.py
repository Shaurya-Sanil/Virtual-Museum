import tkinter as tk
from tkinter import scrolledtext
import openai
import pyttsx3

# Set your OpenAI API key
openai.api_key = "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"  # Replace with your actual API key

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Speed of speech
engine.setProperty("volume", 1)  # Volume (0.0 to 1.0)

# Function to handle ChatGPT responses


def get_chatgpt_response(user_input):
    try:
        # Send the user input to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and knowledgeable museum tour guide. Keep your answers concise. Ask the user if they want more details after every short response."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
        )
        # Extract the assistant's response
        full_response = response['choices'][0]['message']['content']
        short_response = full_response.split(". ")[0] + "."
        # Return short response and full response for clarification
        return short_response, full_response
    except Exception as e:
        return "I'm sorry, I'm unable to respond at the moment. Please try again later.", ""

# Function to play TTS


def play_tts(message):
    engine.say(message)
    engine.runAndWait()

# Function to send a user message to the chatbox and get a response


def send_message():
    user_input = user_input_entry.get().strip()
    if not user_input:
        return
    # Display user input in chat
    chat_display.insert(tk.END, f"You: {user_input}\n")
    user_input_entry.delete(0, tk.END)
    chat_display.yview(tk.END)

    # Get ChatGPT's response
    short_response, full_response = get_chatgpt_response(user_input)
    chat_display.insert(tk.END, f"Tour Guide: {short_response}\n")
    chat_display.yview(tk.END)

    # Play the short response via TTS
    play_tts(short_response)

    # Ask if the user wants more clarification
    if full_response and len(full_response) > len(short_response):
        ask_for_more_details(full_response)

# Function to ask if the user wants more clarification


def ask_for_more_details(full_response):
    chat_display.insert(
        tk.END, "Tour Guide: Would you like me to explain in more detail?\n")
    play_tts("Would you like me to explain in more detail?")
    chat_display.yview(tk.END)

    # If the user wants more clarification
    def clarify_response():
        chat_display.insert(
            tk.END, f"Tour Guide (Detailed): {full_response}\n")
        play_tts(full_response)
        clarify_button.destroy()

    # Add a button for clarification
    clarify_button = tk.Button(root, text="Yes, explain more", font=("Georgia", 12), bg="#6C4A35", fg="#FFFFFF",
                               command=clarify_response)
    clarify_button.pack(pady=10)

# Function to simulate navigation


def navigate_to(floor_name):
    message = f"Navigating to {floor_name}. Please follow me."
    chat_display.insert(tk.END, f"Tour Guide: {message}\n")
    play_tts(message)
    chat_display.yview(tk.END)


# Initialize the main application window
root = tk.Tk()
root.title("Cultural Floor - Virtual Museum")
root.geometry("800x600")
root.configure(bg="#FFF8E8")  # Museum-themed background

# Header
header_frame = tk.Frame(root, bg="#6C4A35", height=50)
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="Cultural Floor - Virtual Museum",
                        bg="#6C4A35", fg="#FFFFFF", font=("Georgia", 18))
header_label.pack(pady=10)

# Title and instructions
title_label = tk.Label(root, text="Welcome to the Cultural Floor",
                       bg="#FFF8E8", fg="#4A3622", font=("Georgia", 24, "bold"))
title_label.pack(pady=10)

instructions_label = tk.Label(root, text="Explore the diverse cultural themes of our museum. Choose a themed floor or ask your tour guide below:",
                              bg="#FFF8E8", fg="#4A3622", font=("Georgia", 14))
instructions_label.pack(pady=10)

# Buttons for themed floors
button_frame = tk.Frame(root, bg="#FFF8E8")
button_frame.pack(pady=20)

themes = ["Indian History", "Ancient Artifacts",
          "Traditional Music", "Folk Dances", "Mughal Empire"]
for theme in themes:
    theme_button = tk.Button(button_frame, text=theme, font=("Georgia", 12), bg="#6C4A35", fg="#FFFFFF",
                             command=lambda t=theme: navigate_to(t))
    theme_button.pack(side=tk.LEFT, padx=10)

# Chatbox area
chatbox_frame = tk.Frame(root, bg="#FFF8E8", bd=2, relief=tk.GROOVE)
chatbox_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

chat_display = scrolledtext.ScrolledText(chatbox_frame, wrap=tk.WORD, font=(
    "Georgia", 12), bg="#FFFFFF", fg="#4A3622", height=15)
chat_display.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
chat_display.insert(tk.END, "Tour Guide: Welcome to the cultural floor. Here you'll find exhibits showcasing art, music, literature, traditions, and much more from different cultures around the world. Feel free to explore and let me know if you have any questions!\n")

# Input area for user messages
input_frame = tk.Frame(root, bg="#FFF8E8")
input_frame.pack(pady=10, fill=tk.X)

user_input_entry = tk.Entry(input_frame, font=(
    "Georgia", 12), bg="#FFFFFF", fg="#4A3622")
user_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

send_button = tk.Button(input_frame, text="Send", font=(
    "Georgia", 12), bg="#6C4A35", fg="#FFFFFF", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10)

# Run the application
root.mainloop()
