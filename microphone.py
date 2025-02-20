import speech_recognition as sr
from deepmultilingualpunctuation import PunctuationModel

def speechToText():
    recognizer = sr.Recognizer()
    model = PunctuationModel()  # Load punctuation model

    with sr.Microphone() as source:
        print('The 🎙️is listening:')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        textPunctuated = model.restore_punctuation(text)
        print(textPunctuated)
        return textPunctuated
    except sr.UnknownValueError:
        print('Sorry, I could not understand the audio.')
    except sr.RequestError:
        print('Could not request results, check your internet connection.')

speechToText()
