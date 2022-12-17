
# !pip install SpeechRecognition
# !pip install moviepy
# ! pip install pydub


import speech_recognition as sr
import moviepy.editor as mp
from pydub import AudioSegment
from pydub.silence import split_on_silence
import shutil
import os


# create a directory to store the audio chunks
def create_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    return folder_name

def rename_file(start, files, step2):
    for file in files:
        name_date = file.split('_')[1:4]
        new_name =  "_".join(name_date).replace(' ', '-')
        # print(name_date)
        # print(new_name)
        ## move files to next step
        shutil.copy(f"{start}/{file}", f"{step2}/{new_name}.mp4")

# a function that splits the audio file into chunks
# and applies speech recognition
def get_large_audio_transcription(path):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """
    # create a speech recognition object
    r = sr.Recognizer()
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)  
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
        # experiment with this value for your target audio file
        min_silence_len = 500,
        # adjust this per requirement
        silence_thresh = sound.dBFS-14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    # process each chunk 
    for i, audio_chunk in enumerate(chunks, start=1):
        # export audio chunk and save it in
        # the `folder_name` directory.
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")
        # recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)
            # try converting it to text
            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                error = {}
                error['count'] += 1
            finally:
                text = f"{text.capitalize()}. "
                # print(chunk_filename, ":", text)
                whole_text += text
    # return the text for all chunks detected
    shutil.rmtree('audio-chunks')
    print(path, error.items())
    return whole_text

def speech_to_text(src, files, batch_name):
    import pandas as pd
    pd.DataFrame(columns=['name','date','text']).to_csv(batch_name,index=False)
    for file in files:
        name_date = file.split('_')[:2]
        whole_text = get_large_audio_transcription(f'{src}/{file}')
        name_date.append(whole_text)

        df = pd.read_csv(batch_name)
        try:
            s = pd.Series(name_date, index=['name','date','text'])
            df = df.append(s, ignore_index=True)

            df.to_csv(batch_name,index=False)
        except:
            print('error')


start = create_folder('dat/raw')
files = os.listdir(start)

step2 = create_folder('data/named')
rename_file(start, files, step2)

step3 = create_folder('data/audio')
! FOR %i IN (data/named/*.mp4) DO ffmpeg -i named/%i -acodec pcm_s16le -ar 16000 data/audio/%i.wav

step4 = os.listdir(step3)
speech_to_text(step3, step4, "data/load/final.csv")


