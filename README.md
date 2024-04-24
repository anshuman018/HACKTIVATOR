#
#
# Gui hai but complete all features nahi hai.
#
#
import tkinter as tk
from tkinter import messagebox
import pyttsx3
import speech_recognition as sr
import openai
from config import apikey

# Set up OpenAI API key
openai.api_key = apikey

# Initialize text-to-speech engine
engine = pyttsx3.init()


# Function to get chatbot response from OpenAI
def get_chatbot_response(user_input):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Choose the appropriate engine
        prompt=user_input,
        max_tokens=50  # Adjust as needed
    )
    return response.choices[0].text.strip()


# Function to handle user input
def handle_user_input():
    user_input = user_input_entry.get().strip()
    if user_input:
        chatbot_response = get_chatbot_response(user_input)
        chat_text.insert(tk.END, "\nYou: " + user_input, "user")
        chat_text.insert(tk.END, "\nChatbot: " + chatbot_response + "\n", "bot")
        user_input_entry.delete(0, tk.END)
        speak(chatbot_response)  # Speak chatbot response


# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to handle voice input
def handle_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        chat_text.insert(tk.END, "\nYou (Voice): " + user_input, "user")
        chatbot_response = get_chatbot_response(user_input)
        chat_text.insert(tk.END, "\nChatbot: " + chatbot_response + "\n", "bot")
        speak(chatbot_response)  # Speak chatbot response
    except sr.UnknownValueError:
        print("Could not understand audio.")
    except sr.RequestError as e:
        print("Error fetching results; {0}".format(e))


# Create main tkinter window
root = tk.Tk()
root.title("Chatbot")

# Set window size and position
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Set background color
root.configure(bg="#f0f0f0")

# Create GUI widgets with styling
chat_text = tk.Text(root, bg="#ffffff", fg="#000000", font=("Arial", 12), wrap="word")
user_input_entry = tk.Entry(root, bg="#ffffff", fg="#000000", font=("Arial", 12))
send_button = tk.Button(root, text="Send", command=handle_user_input, bg="#4caf50", fg="#ffffff", font=("Arial", 12),
                        padx=10)
voice_button = tk.Button(root, text="Voice", command=handle_voice_input, bg="#2196f3", fg="#ffffff", font=("Arial", 12),
                         padx=10)

# Add tags for text coloring
chat_text.tag_configure("user", foreground="#1e88e5", justify="right")
chat_text.tag_configure("bot", foreground="#4caf50")

# Create a frame to hold the chat input and buttons
input_frame = tk.Frame(root, bg="#f0f0f0", bd=1, relief=tk.RAISED)
input_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Place widgets in the window
chat_text.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
user_input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10, pady=10, ipady=5)
send_button.pack(side=tk.LEFT, padx=10, pady=10)
voice_button.pack(side=tk.LEFT, padx=10, pady=10)

# Focus on the entry field initially
user_input_entry.focus()

# Run the tkinter event loop
root.mainloop()
