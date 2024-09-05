from openai import OpenAI
import pyaudio
import wave
import playsound
import numpy as np
import time
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

client = OpenAI(
    api_key =  os.getenv("OPENAI_API_KEY")
)

def record_until_silence(filename, silence_threshold=500, chunk_size=1024, fs=44100, channels=1, silence_duration=1.0, min_record_duration=5):
    """
    Records audio from the microphone and stops when silence is detected.
    Ensures a minimum recording duration before stopping.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=fs,
                    input=True,
                    frames_per_buffer=chunk_size)

    frames = []
    silence_buffer = []
    start_time = time.time()
    print("Listening...\n")

    while True:
        data = stream.read(chunk_size)
        frames.append(data)

        # Convert buffer to numpy array for analysis
        audio_data = np.frombuffer(data, np.int16)
        silence_buffer.append(np.abs(audio_data).mean())

        # Ensure minimum recording duration
        if time.time() - start_time < min_record_duration:
            continue

        # If the average amplitude is below the threshold for the duration of `silence_duration`, stop recording
        if len(silence_buffer) > int(fs / chunk_size * silence_duration):
            silence_buffer.pop(0)  # Remove oldest element

        if np.mean(silence_buffer) < silence_threshold:
            print("Silence detected. Stopping recording.\n")
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

# Function to convert speech to text using OpenAI Whisper
def speech_to_text_whisper(filename):
    """
    Transcribes speech to text using OpenAI Whisper.
    """
    audio_file = open(filename, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return transcript.text

# Generate response using OpenAI GPT
def get_response(prompt):
    """
    Generate a response from OpenAI's GPT.
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        # max_tokens=200,
        # n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Function to convert text to speech using Openai
def text_to_speech(text, filename="output.mp3"):
    """
    Converts text to speech and saves the output as an mp3 file.
    """
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="onyx",
        input=text
    ) as  response:
        response.stream_to_file(filename)

# Function to play audio file
def play_audio(filename):
    """
    Plays the specified audio file.
    """
    playsound.playsound(filename)

# Define the wake words
wake_words = ["hi leo", "hey leo", "hello", "listen", "leo"]

end = False

print(get_response("Hi there!"), "\n")

# Define the conversation loop
while True:
    # Listen for the wake words
    # print("Waiting for wake word...")
    record_until_silence("input.wav")
    text = speech_to_text_whisper("input.wav")
    if not text: 
        continue
    
    text = text.lower()
    # if any(wake_word in text for wake_word in wake_words):
    #     print("Wake word detected!")
    response = "How can I help you?"
    # Keep the conversation going until the user says "stop"
    while True:
        if len(response) > 2:
            print("Response:",response,"\n")
            text_to_speech(response, "response.mp3")
            play_audio("response.mp3")
        
        # Listen for the user's response
        record_until_silence("input.wav")
        
        user_input = speech_to_text_whisper("input.wav")
        print("User Input:",user_input,"\n")

        # Exit the conversation loop if the user says "stop" or "bye"
        if "stop listening" in user_input.lower() or "bye for now" in user_input.lower():
            print("Bye!")
            end = True
            break

        if not user_input: 
            response = ""
            continue
        else:
            # Generate a response with ChatGPT
            user_input = user_input.lower()
            response = get_response(user_input)
              
    if end: break
    # else:
    #     print("Could not detect wake word. Listening again...")
