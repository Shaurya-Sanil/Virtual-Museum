import tkinter as tk
from tkinter import Toplevel, scrolledtext
from PIL import Image, ImageTk  # Import Pillow for image handling
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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and knowledgeable museum tour guide for Indian History. Keep your answers concise. Ask if the user wants more details."},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
        )
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
    chat_display.insert(tk.END, f"You: {user_input}\n")
    user_input_entry.delete(0, tk.END)
    chat_display.yview(tk.END)

    short_response, full_response = get_chatgpt_response(user_input)
    chat_display.insert(tk.END, f"Tour Guide: {short_response}\n")
    chat_display.yview(tk.END)
    play_tts(short_response)

    if full_response and len(full_response) > len(short_response):
        ask_for_more_details(full_response)

# Function to ask if the user wants more clarification
def ask_for_more_details(full_response):
    chat_display.insert(
        tk.END, "Tour Guide: Would you like me to explain in more detail?\n")
    play_tts("Would you like me to explain in more detail?")
    chat_display.yview(tk.END)

    def clarify_response():
        chat_display.insert(
            tk.END, f"Tour Guide (Detailed): {full_response}\n")
        play_tts(full_response)
        clarify_button.destroy()

    clarify_button = tk.Button(root, text="Yes, explain more", font=("Georgia", 12), bg="#6C4A35", fg="#FFFFFF",
                               command=clarify_response)
    clarify_button.pack(pady=10)

# Function to show artifact details in a new window
def show_artifact_details(title, description, image_path):
    detail_window = Toplevel(root)
    detail_window.title(f"{title} - Artifact Details")
    detail_window.geometry("600x400")
    detail_window.configure(bg="#FFF8E8")

    title_label = tk.Label(detail_window, text=title, font=("Georgia", 18, "bold"), bg="#FFF8E8", fg="#4A3622")
    title_label.pack(pady=10)

    description_label = tk.Label(detail_window, text=description, font=("Georgia", 14), wraplength=500, bg="#FFF8E8", fg="#4A3622", justify="left")
    description_label.pack(pady=20)

    # Load and display image using Pillow
    try:
        image = Image.open(image_path)
        image = image.resize((250, 250))  # Resize image to fit within the window
        image_tk = ImageTk.PhotoImage(image)
        image_label = tk.Label(detail_window, image=image_tk)
        image_label.image = image_tk  # Keep a reference to avoid garbage collection
        image_label.pack(pady=10)
    except Exception as e:
        error_label = tk.Label(detail_window, text="Image not found!", font=("Georgia", 12, "italic"))
        error_label.pack(pady=10)

# Main application window
root = tk.Tk()
root.title("Indian History Room - Virtual Museum")
root.geometry("800x600")
root.configure(bg="#FFF8E8")

# Header
header_frame = tk.Frame(root, bg="#6C4A35", height=50)
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="Indian History Room - Virtual Museum", bg="#6C4A35", fg="#FFFFFF", font=("Georgia", 18))
header_label.pack(pady=10)

# Title and instructions
title_label = tk.Label(root, text="Explore the Rich Artifacts of Indian History", bg="#FFF8E8", fg="#4A3622", font=("Georgia", 24, "bold"))
title_label.pack(pady=10)

instructions_label = tk.Label(root, text="Click on an artifact to learn more about its history and significance.", bg="#FFF8E8", fg="#4A3622", font=("Georgia", 14))
instructions_label.pack(pady=10)

# Artifact container
artifact_frame = tk.Frame(root, bg="#FFF8E8")
artifact_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# List of artifacts with image paths
artifacts = [
    {"title": "Ashoka Pillar", "description": "The Ashoka Pillar is a series of columns dispersed throughout the Indian subcontinent, commissioned by Emperor Ashoka.", "image": "ashoka-pillar.jpg"},
    {"title": "Indus Valley Seals", "description": "Seals from the Indus Valley Civilization, used for trade and possibly religious purposes.", "image": "indus-seals.jpg"},
    {"title": "Chola Bronze Sculptures", "description": "Exquisite bronze sculptures created by the Chola dynasty, representing gods and goddesses.", "image": "chola-sculptures.jpg"},
    {"title": "Mughal Miniature Paintings", "description": "Detailed, colorful paintings created during the Mughal Empire, depicting court scenes and more.", "image": "mughal-paintings.jpg"},
]

for artifact in artifacts:
    artifact_container = tk.Frame(artifact_frame, bg="#6C4A35", pady=10, padx=10, relief=tk.RAISED, bd=2)
    artifact_container.pack(pady=10, fill=tk.X)

    artifact_title = tk.Label(artifact_container, text=artifact["title"], font=("Georgia", 14, "bold"), bg="#6C4A35", fg="#FFFFFF")
    artifact_title.pack(anchor="w")

    artifact_button = tk.Button(artifact_container, text="View Details", font=("Georgia", 12), bg="#FFF8E8", fg="#6C4A35",
                                command=lambda a=artifact: show_artifact_details(a["title"], a["description"], a["image"]))
    artifact_button.pack(anchor="e")

# Chatbox area
chatbox_frame = tk.Frame(root, bg="#FFF8E8", bd=2, relief=tk.GROOVE)
chatbox_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

chat_display = scrolledtext.ScrolledText(chatbox_frame, wrap=tk.WORD, font=("Georgia", 12), bg="#FFFFFF", fg="#4A3622", height=15)
chat_display.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
chat_display.insert(tk.END, "Tour Guide: Hi! I'm your guide for the Indian History Room. How can I assist you?\n")

# Input area for user messages
input_frame = tk.Frame(root, bg="#FFF8E8")
input_frame.pack(pady=10, fill=tk.X)

user_input_entry = tk.Entry(input_frame, font=("Georgia", 12), bg="#FFFFFF", fg="#4A3622")
user_input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

send_button = tk.Button(input_frame, text="Send", font=("Georgia", 12), bg="#6C4A35", fg="#FFFFFF", command=send_message)
send_button.pack(side=tk.RIGHT, padx=10)

# Run the application
root.mainloop()
