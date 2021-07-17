import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

AZURE_SPEECH_KEY = "c43b877e4bf046b583c5b7779c0ad473"

print("Say something")

with m as source:
    audio = r.listen(source)

try:
    print("Microsoft Azure Speech thinks you said " + r.recognize_bing(audio, key=AZURE_SPEECH_KEY))
except sr.UnknownValueError:
    print("Microsoft Azure Speech could not understand audio")
except sr.RequestError as e:
    print("Could not request results from MAS service; {0}".format(e))
