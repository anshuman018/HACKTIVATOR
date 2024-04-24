import openai
import pyttsx3
import speech_recognition as sr
import smtplib
import ssl
from email.message import EmailMessage
import webbrowser
import os
from config import apikey

openai.api_key = apikey

email_sender = 'anshumanacadmic@gmail.com'
email_password = 'lsnsjggbxbwglvly'
smtp_server = 'smtp.gmail.com'
smtp_port = 465


def init_tts_engine():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # Set to a male voice (change index if necessary)
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


def edit_email_body(email_body):
    print("Current email body:")
    print(email_body)
    edit_option = input("Do you want to edit the email body? (yes/no): ")
    if edit_option.lower() == "yes":
        new_email_body = input("Enter the new email body: ")
        return new_email_body
    else:
        return email_body


def browse_web(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)


def play_music():
    song_path = r"C:\My Projects\Smart India Hackathon\On-My-Way.mp3"
    os.startfile(song_path)
    say("Playing music sir...")


def say(text):
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    engine = init_tts_engine()
    recognizer = init_speech_recognizer()

    print("Welcome to Nisha - your virtual assistant")
    say("Welcome to Nisha - your virtual assistant")

    voice_command_mode = False

    while True:
        if not voice_command_mode:
            user_input_text = input("You (Text): ").strip().lower()

            if user_input_text == 'exit' or user_input_text == 'quit':
                say("Goodbye!")
                print("Nisha: Goodbye!")
                break

            if 'your name' in user_input_text:
                say("My name is Nisha. How can I help you?")
                print("Nisha: My name is Nisha. How can I help you?")

            elif '`' in user_input_text:
                voice_command_mode = True
                print("Nisha is now listening for voice commands...")
                say("Nisha is now listening for voice commands.")

            elif 'send email' in user_input_text:
                recipient = input("Recipient: ")
                subject = input("Subject: ")
                email_body = generate_email_body(subject)
                edited_email_body = edit_email_body(email_body)
                print("Edited email body:")
                print(edited_email_body)
                confirmation = input("Do you want to send this email? (yes/no): ")
                if confirmation.lower() == "yes":
                    send_email(subject, edited_email_body, recipient)
                    say("Email sent successfully!")
                    print("Nisha: Email sent successfully!")
                else:
                    say("Email not sent.")
                    print("Nisha: Email not sent.")

            elif 'browse' in user_input_text:
                query = user_input_text.split('browse', 1)[-1].strip()
                browse_web(query)

            elif 'play music' in user_input_text:
                play_music()

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
                say(nisha_response)

        else:
            print("You can start speaking your command:")

            with sr.Microphone() as source:
                print("Listening...")
                say("Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)

            try:
                user_input_voice = recognizer.recognize_google(audio, language="en-in")
                print(f"You (Voice): {user_input_voice}")

                if 'email' in user_input_voice:
                    recipient = input("Recipient: ")
                    subject = input("Subject: ")
                    email_body = generate_email_body(subject)
                    edited_email_body = edit_email_body(email_body)
                    print("Edited email body:")
                    print(edited_email_body)
                    confirmation = input("Do you want to send this email? (yes/no): ")
                    if confirmation.lower() == "yes":
                        send_email(subject, edited_email_body, recipient)
                        say("Email sent successfully!")
                        print("Nisha: Email sent successfully!")
                    else:
                        say("Email not sent.")
                        print("Nisha: Email not sent.")

                elif 'browse' in user_input_voice:
                    query = user_input_voice.split('browse', 1)[-1].strip()
                    browse_web(query)

                elif 'play music' in user_input_voice:
                    play_music()

                else:
                    response = openai.Completion.create(
                        engine="gpt-3.5-turbo-instruct",
                        prompt=user_input_voice,
                        max_tokens=100,
                        temperature=0.7,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    nisha_response = response.choices[0].text.strip()
                    print(f"Nisha: {nisha_response}")
                    say(nisha_response)

            except sr.UnknownValueError:
                print("You (Voice): (Silence)")
            except sr.RequestError:
                print("You (Voice): Sorry, there was an issue connecting to Google's servers.")
                say("Sorry, there was an issue connecting to Google's servers.")
