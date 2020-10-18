import speech_recognition as sr

def audio_to_text():#converts a recording into text
    r=sr.Recognizer()
    source_audio= sr.WavFile('speech.wav')
    with source_audio as source1:
        audio=r.record(source1)
        try:
            a = (r.recognize_google(audio,language="en-IN"))
            a = a[0].upper() + a[1:]# makes the first word capital letter

            return(a)
        except :
            print('Unrecognised Audio')
            return('E')#Returns False if unrecognised


