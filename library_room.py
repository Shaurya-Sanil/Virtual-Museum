import tkinter as tk
from tkinter import scrolledtext
import openai
import pyttsx3

# Set your OpenAI API key
openai.api_key = "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"  # Replace with your actual API key

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty("rate", 200)  # Speed of speech
engine.setProperty("volume", 1)  # Volume (0.0 to 1.0)

# Function to handle ChatGPT responses


def get_chatgpt_response(user_input):
    try:
        # Send the user input to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a friendly and knowledgeable librarian in a virtual musuem library room. Keep your answers concise. Ask the user if they want more details after every short response."},
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
    chat_display.insert(tk.END, f"Librarian: {short_response}\n")
    chat_display.yview(tk.END)

    # Play the short response via TTS
    play_tts(short_response)

    # Ask if the user wants more clarification
    if full_response and len(full_response) > len(short_response):
        ask_for_more_details(full_response)

# Function to ask if the user wants more clarification


def ask_for_more_details(full_response):
    chat_display.insert(
        tk.END, "Librarian: Would you like me to explain in more detail?\n")
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
    chat_display.insert(tk.END, f"Librarian {message}\n")
    play_tts(message)
    chat_display.yview(tk.END)

# Function to display book details


def show_book_details(book_name):
    book_details = book_info.get(book_name, "Details not available.")
    chat_display.insert(tk.END, f"Librarian: {book_details}\n")
    play_tts(book_details)


# Book Information (Examples of Indian Books with short descriptions)
book_info = {
    "The Bhagavad Gita": "A 700-verse Hindu scripture that is part of the Indian epic Mahabharata. It consists of a conversation between Prince Arjuna and the god Krishna, who serves as his charioteer.",
    "Ramayana": "An ancient Indian epic that narrates the life of Prince Rama, his wife Sita, and his loyal companion Hanuman, and explores themes of duty, dharma, and righteousness.",
    "Mahabharata": "An ancient Indian epic that is one of the longest pieces of literature in the world, recounting the story of the Kurukshetra War and the fates of the Kaurava and Pandava brothers.",
    "Upanishads": "A collection of philosophical texts that explore the concepts of Brahman (universal consciousness) and Atman (individual soul), forming the basis for much of Indian spiritual thought.",
    "A Passage to India": "A novel by E. M. Forster set in British-controlled India, it deals with the complex social dynamics between the British, Indians, and Muslims during the colonial period.",
    "The Discovery of India": "Written by Jawaharlal Nehru, this book explores India's history, culture, and philosophy, and was penned during his imprisonment by the British.",
    "The God of Small Things": "A novel by Arundhati Roy that explores the tragic story of fraternal twins in a small town in Kerala, set against the backdrop of India's social and political struggles.",
    "Midnight's Children": "A novel by Salman Rushdie, blending history with magical realism, that follows the life of a boy born at the exact moment of India's independence.",
    "Train to Pakistan": "A novel by Khushwant Singh, depicting the partition of India in 1947, and its effects on the lives of people living on both sides of the new border."
}

# Initialize the main application window
root = tk.Tk()
root.title("Library - Virtual Museum")
root.geometry("800x600")
root.configure(bg="#FFF8E8")  # Library-themed background

# Header
header_frame = tk.Frame(root, bg="#6C4A35", height=50)
header_frame.pack(fill=tk.X)
header_label = tk.Label(header_frame, text="Library - Virtual Museum",
                        bg="#6C4A35", fg="#FFFFFF", font=("Georgia", 18))
header_label.pack(pady=10)

# Title and instructions
title_label = tk.Label(root, text="Welcome to the Library",
                       bg="#FFF8E8", fg="#4A3622", font=("Georgia", 24, "bold"))
title_label.pack(pady=10)

instructions_label = tk.Label(root, text="Explore the great works of Indian literature. Choose a book to learn more:",
                              bg="#FFF8E8", fg="#4A3622", font=("Georgia", 14))
instructions_label.pack(pady=10)

# Buttons for books
button_frame = tk.Frame(root, bg="#FFF8E8")
button_frame.pack(pady=20)

book_buttons = list(book_info.keys())
for book in book_buttons:
    book_button = tk.Button(button_frame, text=book, font=("Georgia", 12), bg="#6C4A35", fg="#FFFFFF",
                            command=lambda b=book: show_book_details(b))
    book_button.pack(side=tk.LEFT, padx=10)

# Chatbox area
chatbox_frame = tk.Frame(root, bg="#FFF8E8", bd=2, relief=tk.GROOVE)
chatbox_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

chat_display = scrolledtext.ScrolledText(chatbox_frame, wrap=tk.WORD, font=(
    "Georgia", 12), bg="#FFFFFF", fg="#4A3622", height=15)
chat_display.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
chat_display.insert(tk.END, "Librarian: Welcome to the Library! This is where knowledge and history come together. I’m your virtual librarian, and I’ll be here to help you explore the vast collection of books, manuscripts, and ancient texts.\n")

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
