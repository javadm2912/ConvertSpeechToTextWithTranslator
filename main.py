import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
from googletrans import Translator


r = sr.Recognizer()

def write_text(text, fileName):
    with open(fileName + ".txt", "w", encoding="utf-8") as f:
        f.write(text)

def get_online_audio_transcription():
    whole_text = ""
    whole_trans_text = ""
    with sr.Microphone() as source:
        print("Talk")
        r.adjust_for_ambient_noise(source,0.2)
        audio_listened = r.listen(source)
        try:
            text = r.recognize_google(audio_listened, language=sound_lng)
            # text = r.recognize_google(audio_listened)
            translator = Translator()
            trasText = translator.translate(text, dest=trns_lng, src=sound_lng[:2])
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            print(text)
            print(trasText.text)
            whole_text += text
            whole_trans_text += trasText.text
   

def get_large_audio_transcription(path):
    # open the audio file using pydub
    sound = AudioSegment.from_wav(path)
    # split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(
        sound,
        # experiment with this value for your target audio file
        min_silence_len=500,
        # adjust this per requirement
        silence_thresh=sound.dBFS - 14,
        # keep the silence for 1 second, adjustable as well
        keep_silence=500,
    )
    folder_name = "audio-chunks"
    # create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""
    whole_trans_text = ""
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
                text = r.recognize_google(audio_listened, language=sound_lng)
                # text = r.recognize_google(audio_listened)
                print(text)
                translator = Translator()
                trasText = translator.translate(text, dest=trns_lng, src=sound_lng[:2])
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(trasText.text)
                whole_text += text
                whole_trans_text += trasText.text
    # return the text for all chunks detected

    
    print('*************END*************')
    write_text(whole_text,'original')
    write_text(whole_trans_text,'translate')


path = input('wav file address : ')
sound_lng = input('sound language (example : fa-IR , en-US) : ')
trns_lng = input('translate language (example : fa , en) : ')
get_large_audio_transcription(path)
# while(True):
#     get_online_audio_transcription()
print('end')
input()
