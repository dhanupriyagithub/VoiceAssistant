import openai
import pyttsx3
import speech_recognition as sr
import random


openai.api_key = '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'
model_id = 'gpt-3.5-turbo'

engine = pyttsx3.init()

engine.setProperty('rate',180)

voices = engine.getProperty('voices')

if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)
else:
    engine.setProperty('voice', voices[0].id)

interaction_counter = 0

def transcribe_audio_to_text(filename):
    recongnizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recongnizer.record(source)
        try:
            return recongnizer.recognize_google(audio)
        except:
            print("")

def chatGPT_conversation(conversation):
    messages = [{'role': message['role'], 'content': message['content']} for message in conversation]
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=messages
    )
    api_usage=response['usage']
    print('Total token consumed {0}'.format(api_usage['total_tokens']))
    conversation.append({'role':response.choices[0].message.role,'content':response.choices[0].message.content})
    return conversation


def speak_text(text):
    engine.say(text)
    engine.runAndWait()
    
conversation=[]
conversation.append({'role': 'user','content': 'please act like friday AI from ironman,make a one sentence phrase introducing yourself without saying something that sounds like this chat'})
conversation = chatGPT_conversation(conversation)
print('{0}: {1} \n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))
speak_text(conversation[-1]['content'.strip()])


def activate_assistant():
    starting_chat_phrases = ["Yes sir, how may i assist you?","Yes, what can i do for you ?","how can i help you sir?","Friday here, how can i help you today?","Yes, what can i do for u today?",
                             "Yes sir, what's on your mind?","Friday ready to assist, what can i do for you?","At your command sir.how may i help you today?", "Yes boss, Iam here to help . what do you need from me?","Yes,I',m listening. what can i do for you,sir?","How can I assist you today ,sir?","Yes, sir. how can i make your day easier?","Yes boss , what's the plan?","Yes, what's on your mind , sir?"]
    continued_chat_phrases = ["Yes","Yes, sir","Yes, boss","I'm all ears"]

    random_chat = ""
    if(interaction_counter == 1):
        random_chat = random.choice(starting_chat_phrases)
    else: 
        random_chat = random.choice(continued_chat_phrases)

    return random_chat


def append_to_log(text):
    with open("chat_log.txt","a") as f:
        f.write(text + "\n")

while True:
    print("Say 'Friday' to start....")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            transcription = recognizer.recognize_google(audio)
            if "friday" in transcription.lower():
                interaction_counter +=1
                filename = "input.wav"
                redayToWork = activate_assistant()
                speak_text(redayToWork)
                print(redayToWork)
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    source.pause_thershold = 1
                    audio = recognizer.listen(source,phrase_time_limit=None,timeout=None)
                    with open(filename,"wb") as f:
                        f.write(audio.get_wav_data())

                text = transcribe_audio_to_text(filename)

                if text:
                    print(f"You said:{text}")
                    append_to_log(f"You:{text}\n")

                    print(f"Friday says:{conversation}")

                    prompt = text
                    conversation.append({'role':'user','content':prompt})
                    conversation = chatGPT_conversation(conversation)

                    print('{0}:{1}\n'.format(conversation[-1]['role'].strip(),conversation[-1]['content']))

                    append_to_log(f"Friday:{conversation[-1]['content'].strip()}\n")

                    speak_text(conversation[-1]['content'].strip())

        except Exception as e:
            continue

            





