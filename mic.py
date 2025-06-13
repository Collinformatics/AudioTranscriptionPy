import os
import platform
import speech_recognition as sr
import textwrap


# Define file paths
fileName = 'log'
pathDirLogs = 'logs'

# Length of printed strings
consoleWidth = 90

def logConversation(pathDirectory, messages):
    print('\n')
    for message in messages:
        message = message.strip()
        if message:
            message = textwrap.fill(message,
                                    width=consoleWidth,
                                    subsequent_indent="     ")
            print(f'{message}\n')

    # Make the directory
    if not os.path.exists(pathDirectory):
        os.makedirs(pathDirectory)

    # Log the message
    pathDirLogs = os.path.join(pathDirectory, fileName + '.txt')
    if platform.system() != 'Darwin':  # 'Darwin' means macOS
        # Adjust path for Windows (if not on macOS)
        pathDirLogs = pathDirLogs.replace('/', '\\')
    with open(pathDirLogs, 'a') as file:
        # Append: 'a'
        # Write: 'w'
        file.write(messages[-1] + '\n\n')


def loadMessages(pathDirectory):
    # Make the directory
    if not os.path.exists(pathDirectory):
        os.makedirs(pathDirectory)

    # Load the messages
    pathLog = os.path.join(pathDirectory, fileName + '.txt')
    if os.path.exists(pathLog):
        with open(pathLog, 'r') as file:
            messages = file.readlines()
    else:
        messages = []

    return messages


def recordAudio(messages, pathDirectory):
    # Setup microphone
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Records and transcribe audio
    with (microphone as source):
        recognizer.adjust_for_ambient_noise(source)
        try:
            print('Mic On')
            audio = recognizer.listen(source, timeout=None)
            print('Mic Off')
            print('Processing Audio')
            text = f'{recognizer.recognize_faster_whisper(audio).strip()}'

            if text != '' and text != '.  .  .  .':
                messages.append(text)
                logConversation(pathDirectory, messages)

        except sr.UnknownValueError:
            print('_text_Error: I could not understand the audio.')
        except sr.RequestError:
            print('_text_Error: Transcription failed, check your internet connection.')
        except sr.WaitTimeoutError:
            print("Mic Off")


# Convert audio to text
messages = loadMessages(pathDirLogs)
recordAudio(messages, pathDirLogs)
