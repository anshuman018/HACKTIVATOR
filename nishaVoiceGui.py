#
#
#
# gui hai but problem ye hai ki text display in ho raha uspe.
#
#
#
import tkinter as tk
import os
import webbrowser
import pyttsx3
import speech_recognition as sr
import smtplib
import ssl
from email.message import EmailMessage
import openai
from config import apikey

openai.api_key = apikey

email_sender = 'anshumanacadmic@gmail.com'
email_password = 'lsnsjggbxbwglvly'
smtp_server = 'smtp.gmail.com'
smtp_port = 465


def init_tts_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    new_rate = 150
    engine.setProperty('rate', new_rate)
    return engine


def init_speech_recognizer():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    return recognizer


def send_email(subject, body, recipient):
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(email_sender, email_password)
            message = EmailMessage()
            message.set_content(body)
            message['Subject'] = subject
            message['From'] = email_sender
            message['To'] = recipient
            server.send_message(message)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


def generate_email_body(subject):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"Compose an email body for the subject: {subject}.",
        max_tokens=100,
        temperature=0.7,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    email_body = response.choices[0].text.strip()
    return email_body


def browse_web(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        print("Opening browser with search results...")
    except Exception as e:
        print(f"Error browsing the web: {str(e)}")


def say(text):
    engine.say(text)
    engine.runAndWait()


def handle_user_input(event=None):
    user_input_text = user_input_entry.get().strip().lower()
    user_input_entry.delete(0, tk.END)

    if user_input_text == 'exit' or user_input_text == 'quit':
        engine.say("Goodbye!")
        print("Nisha: Goodbye!")
        engine.runAndWait()
        root.destroy()
    elif 'your name' in user_input_text:
        engine.say("My name is Nisha. How can I help you?")
        print("Nisha: My name is Nisha. How can I help you?")
        engine.runAndWait()
    elif '`' in user_input_text:
        voice_command_mode = True
        print("Nisha is now listening for voice commands...")
        engine.say("Nisha is now listening for voice commands.")
        engine.runAndWait()
    elif 'send email' in user_input_text:
        recipient = input("Recipient: ")
        subject = input("Subject: ")
        email_body = generate_email_body(subject)
        print("Generated email body:")
        print(email_body)
        confirmation = input("Do you want to send this email? (yes/no): ")
        if confirmation.lower() == "yes":
            send_email(subject, email_body, recipient)
            engine.say("Email sent successfully!")
            print("Nisha: Email sent successfully!")
            engine.runAndWait()
        else:
            engine.say("Email not sent.")
            print("Nisha: Email not sent.")
            engine.runAndWait()
    elif 'play music' in user_input_text:
        Song_path = r"C:\My Projects\Smart India Hackathon\On-My-Way.mp3"
        os.startfile(Song_path)
        say("Playing music sir...")
    elif 'open' in user_input_text:
        query = user_input_text.replace('open', '').strip()
        browse_web(query)
    else:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=user_input_text,
            max_tokens=100,
            temperature=0.7,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )

        nisha_response = response.choices[0].text.strip()
        print(f"Nisha: {nisha_response}")

        engine.say(nisha_response)
        engine.runAndWait()


def handle_voice_input():
    # Placeholder function for handling voice input
    print("Voice input is not implemented yet.")


if __name__ == '__main__':
    engine = init_tts_engine()
    recognizer = init_speech_recognizer()

    root = tk.Tk()
    root.title("Nisha - Virtual Assistant")

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
    send_button = tk.Button(root, text="Send", command=handle_user_input, bg="#4caf50", fg="#ffffff",
                            font=("Arial", 12),
                            padx=10)
    voice_button = tk.Button(root, text="Voice", command=handle_voice_input, bg="#2196f3", fg="#ffffff",
                             font=("Arial", 12),
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

    root.mainloop()
