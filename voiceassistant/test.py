import openai
from twilio.rest import Client
import sys
import speech_recognition as sr

# Set your OpenAI API key here
openai.api_key = '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'

# Twilio API configuration
twilio_account_sid = 'AC4cc5b473630fa06d6b8f864f9c743582'
twilio_auth_token = '74998b5f06388dc6f7e8af97ff4d0935'
twilio_phone_number = '+19802245395'
recipient_phone_number = '+919791753399'

# Initialize the Twilio client
client = Client(twilio_account_sid, twilio_auth_token)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

def make_tts_callout(text):
    call = client.calls.create(
        twiml=f'<Response><Say>{text}</Say></Response>',
        to=recipient_phone_number,
        from_=twilio_phone_number
    )
    return call

ai_responses = []

try:
    while True:
        with sr.Microphone() as source:
            print("Speak something: ")
            audio = recognizer.listen(source)

        user_input = recognizer.recognize_google(audio)

        if user_input.lower() == 'exit':
            break  # Exit the loop

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=200
        )

        ai_response = response.choices[0].text.strip()
        ai_responses.append(ai_response)

        print("AI: " + ai_response)

except KeyboardInterrupt:
    print("Exiting the program.")

if ai_responses:
    full_ai_response = ' '.join(ai_responses)
    make_tts_callout(full_ai_response)  # Make the call after collecting AI responses