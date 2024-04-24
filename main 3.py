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


if __name__ == '__main__':
    engine = init_tts_engine()
    recognizer = init_speech_recognizer()

    print("Welcome to Nisha - your virtual assistant")
    engine.say("Welcome to Nisha - your virtual assistant")
    engine.runAndWait()

    voice_command_mode = False

    while True:
        if not voice_command_mode:
            user_input_text = input("You (Text): ").strip().lower()

            if user_input_text == 'exit' or user_input_text == 'quit':
                engine.say("Goodbye!")
                print("Nisha: Goodbye!")
                engine.runAndWait()
                break

            if 'your name' in user_input_text:
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

        else:
            print("You can start speaking your command:")

            with sr.Microphone() as source:
                print("Listening...")
                engine.say("Listening...")
                engine.runAndWait()
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source)

            try:
                user_input_voice = recognizer.recognize_google(audio, language="en-in")
                print(f"You (Voice): {user_input_voice}")

                if 'exit' in user_input_voice or 'quit' in user_input_voice:
                    engine.say("Goodbye!")
                    print("Nisha: Goodbye!")
                    engine.runAndWait()
                    break

                if 'your name' in user_input_voice:
                    engine.say("My name is Nisha. How can I help you?")
                    print("Nisha: My name is Nisha. How can I help you?")
                    engine.runAndWait()

                elif 'send email' in user_input_voice:
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

                elif 'play music' in user_input_voice:
                    Song_path = r"C:\My Projects\Smart India Hackathon\On-My-Way.mp3"
                    os.startfile(Song_path)
                    say("Playing music sir...")

                elif 'open' in user_input_voice:
                    query = user_input_voice.replace('open', '').strip()
                    browse_web(query)

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

                    engine.say(nisha_response)
                    engine.runAndWait()

            except sr.UnknownValueError:
                print("You (Voice): (Silence)")
            except sr.RequestError:
                print("You (Voice): Sorry, there was an issue connecting to Google's servers.")
                engine.say("Sorry, there was an issue connecting to Google's servers.")
                engine.runAndWait()

            voice_command_mode = False
