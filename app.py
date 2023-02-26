
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
model = whisper.load_model('base')

# Upload an audio file (WAV or MP3) from the sidebar
audio_file = st.sidebar.file_uploader('Upload Audio', type=['wav', 'mp3'])

# Record an audio clip using the microphone

audio_bytes = audio_recorder(
    energy_threshold=(-2.0, 2.0),
    pause_threshold=10.0,
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
    st.audio(audio_file)

# If the "Transcribe Audio" button is clicked, transcribe the audio
if st.sidebar.button('Transcribe Audio'):
    if audio_file is not None:
        transcription = model.transcribe(audio_file.name)
        if transcription:
            st.header('Transcription')
            st.markdown(f'<h3 class="transcription-heading">Transcription:</h3>', unsafe_allow_html=True)
        else:
            st.sidebar.error('Something went wrong')
    elif audio_bytes is not None:
        transcription = model.transcribe(filename)
        if transcription:
            st.header('Transcription')
            st.markdown(f'<h3 class="transcription-heading">Transcription:</h3>', unsafe_allow_html=True)
            st.markdown(f'<ul class="transcription-list">{transcription["text"]}</ul>', unsafe_allow_html=True)
        else:
            st.sidebar.error('Something went wrong')
    else:
        st.error('You need to record/upload an audio file')
