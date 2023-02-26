import streamlit as st
import whisper
from audio_recorder_streamlit import audio_recorder
import soundfile as sf


st.title('My Whisper transcriber')
sample_rate=16_000


model = whisper.load_model('base')


# upload an audio file mp3/wav
audio_file = st.sidebar.file_uploader('Upload Audio', type=['wav','mp3']) 


audio_bytes = audio_recorder(
    energy_threshold=(-1.0, 1.0),
    pause_threshold=30.0,
    sample_rate=sample_rate,
    text="Recording audio",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="user",
    icon_size="6x",
)

filename = "audio_record.wav"
if audio_bytes: 
    with open(filename, "wb") as f_out:
        f_out.write(audio_bytes)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")


if audio_file is not None:
    st.audio(audio_file)
    
if st.sidebar.button('Transcrib Audio'):
    model = whisper.load_model('base')
    if audio_file is not None :
        transcribtion = model.transcribe(audio_file.name)
        if transcribtion: 
            st.sidebar.success('Audio transcripted')
        else: 
            st.sidebar.error('something wrong')
        st.write(transcribtion['text'])
    elif audio_bytes is not None :
        transcribtion = model.transcribe(filename)
        if transcribtion: 
            st.sidebar.success('Audio transcripted')
        else: 
            st.sidebar.error('something wrong')
        st.write(transcribtion['text'])
    else:
        st.error('you need to record/upload an audio file')
        

       
