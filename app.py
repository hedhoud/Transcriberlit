
import whisper
from audio_recorder_streamlit import audio_recorder
import streamlit as st

# This script allows the user to transcribe an audio file or a recorded audio clip using the Whisper library.

# Add custom CSS styles
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    </style>
    
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .transcription {
        border : 'bold','1px';
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-size: 16px;
        color: #333;
    }
    </style>
    
    """,
    unsafe_allow_html=True
)



# Add content to your app
st.title('My Whisper transcriber')
st.write('Welcome to my app!')
st.header('Instructions')
st.write('To use this app, upload an audio file or record a clip using the microphone. Then click the "Transcribe Audio" button to transcribe the audio.')


sample_rate = 16_000

# Load the Whisper model
Tiny = 'tiny'
Base = 'base'
Medium = 'medium'
if model_selection := st.sidebar.checkbox(
    'Select to change a Model', value=False
):
    model = st.sidebar.radio('Choose the Whisper Model:', [Tiny, Base, Medium])
    model = whisper.load_model(model)
else:
    model = whisper.load_model("base")

# Upload an audio file (WAV or MP3) from the sidebar
audio_file = st.file_uploader("Upload an audio File:",type=['wav', 'mp3'])


# Record an audio clip using the microphone
audio_bytes = audio_recorder(
    energy_threshold=(-2.0, 2.0),
    pause_threshold=15.0,
    sample_rate=sample_rate,
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_size="2x",
)

# If an audio clip was recorded, write it to a file
if audio_bytes:
    filename = "audio_record.wav"
    try:
        with open(filename, "wb") as audio_file:
            audio_file.write(audio_bytes)
    except Exception as e:
        st.error(f"Error writing audio file: {e}")
    else:
        # Play the recorded audio clip using st.audio
        st.audio(audio_bytes, format="audio/wav")

# If an audio file was uploaded, play it using st.audio
if audio_file is not None:
    st.success("File uploaded successfully!")
    st.audio(audio_file.read())


# If the "Transcribe Audio" button is clicked, transcribe the audio
if st.sidebar.button('Transcribe Audio'):
    if audio_file is not None:
        if transcription := model.transcribe(audio_file.name):
            st.header('Transcription')
            st.markdown(f'<ul class="transcription-list">{transcription["text"]}</ul>', unsafe_allow_html=True)

        else:
            st.sidebar.error('Something went wrong')
    elif audio_bytes is not None:
        if transcription := model.transcribe(filename):
            st.header('Transcription:')
            st.markdown(f'<ul class="transcription-list">{transcription["text"]}</ul>', unsafe_allow_html=True)
        else:
            st.sidebar.error('Something went wrong')
    else:
        st.error('You need to record/upload an audio file')
