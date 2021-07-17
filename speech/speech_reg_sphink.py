import speech_recognition as sr
import time

r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    print("Say something")
    audio = r.listen(source)

time.sleep(3)

try:
    print("Sphinx thinks you said " + r.recognize_sphinx(audio))
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Sphinx service; {0}".format(e))
