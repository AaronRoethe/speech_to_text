from pydub import AudioSegment
import speech_recognition as sr

count = 2
# files                                                                         
src = f"test.mp3"
dst = f"test.wav"

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(src)
sound.export(dst, format="wav")

# create a speech recognition object
r = sr.Recognizer()
# open the audio file using pydub

with sr.AudioFile(dst) as source:
    audio_listened = r.record(source)
    # try converting it to text
    text = r.recognize_google(audio_listened)

with open(f"out.txt", 'w') as file:
    file.write(text)