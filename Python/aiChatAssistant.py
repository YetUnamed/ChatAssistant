import time, wave, pathlib
import pyaudio, pydub # type: ignore
import keyboard, logging
import openai, subprocess
import pydub.playback # type: ignore

FORMAT = pyaudio.paInt16
CHANNELS = 2
SAMPLE_RATE = 44100
CHUNK = 1024
RECORDING_KEY = "shift"
API_KEY = "sk-"
CHATGPT = openai.OpenAI(api_key=API_KEY)

SYST_32 = pathlib.Path("C:/Windows/System32")
APPDATA = pathlib.Path.home() / "AppData" / "Roaming"

apps = {
    "calculator": SYST_32 / "calc.exe",
    "spotify": APPDATA / "Spotify" / "Spotify.exe",
    "notepad": SYST_32 / "notepad.exe",
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def record_audio(filepath: str, duration: int | None=None):
    if duration == None or duration <= 0 :
        duration = 10
    """Record audio from the microphone and save it to a WAV file.

    Args:
        filepath (str): Path to save the recorded audio file.
        duration (float, optional): Duration of recording in seconds. Defaults to 10.
    """
    frames: list[bytes] = []

    P = pyaudio.PyAudio()

    stream = P.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE,
                          input=True, frames_per_buffer=CHUNK)

    logger.info(f"Hold {RECORDING_KEY.upper()} key to record!")
    keyboard.wait(RECORDING_KEY)
    logger.info("Recording started...")

    start_time = time.time()
    while keyboard.is_pressed(RECORDING_KEY) and (time.time() - start_time) <= duration:
        data = stream.read(CHUNK)
        frames.append(data)

    logger.info("Recording stopped.")
    stream.stop_stream()
    stream.close()

    P.terminate()

    with wave.open(filepath, "wb") as wv:
        wv.setnchannels(CHANNELS)
        wv.setsampwidth(P.get_sample_size(FORMAT))
        wv.setframerate(SAMPLE_RATE)
        wv.writeframes(b''.join(frames))

    logger.info(f"Audio recorded and saved to '{filepath}' successfully!")

def fetch_response(prompt: str, messages: list[dict[str, str]]) -> str | None:
    """Fetch AI response given a prompt and conversation history.

    Args:
        prompt (str): Prompt to generate a response.
        messages (list): Conversation history.

    Returns:
        str | None: Generated response from AI.
    """
    default_conversation = {"role": "system", "content": "You are a helpful AI with a word limit of 1024 words."}
    if messages[0] != default_conversation:
        messages[0] = default_conversation
    messages.append({"role": "user", "content": prompt})
    response = (
        CHATGPT.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages, # type: ignore
            temperature=0.5,
            max_tokens=1024,
        )
        .choices[0]
        .message.content
    )
    if response != None:
        messages.append({"role": "assistant", "content": response})
    return response

def speech_to_text(filepath: str) -> str:
    """Convert speech from an audio file to text.

    Args:
        filepath (str): Path to the audio file.

    Returns:
        str: Text transcription of the speech.
    """
    return CHATGPT.audio.transcriptions.create(
        model="whisper-1", file=open(filepath, "rb")
    ).text

def text_to_speech(response: str | None, filename: str) -> None:
    if response == None:
        response = "Error: Text input for text to speech is None."
    """Convert text to speech and save to an audio file.

    Args:
        response (str): Text to convert to speech.
        filename (str): Path to save the audio file.
        voice (str, optional): Voice to use for speech synthesis. Defaults to "alloy".
    """
    with CHATGPT.audio.speech.with_streaming_response.create(
        model="tts-1", voice="alloy", input=response
    ) as audio:
        audio.stream_to_file(filename)

def play_soundfile(filepath: str) -> None:
    """Play an audio file.

    Args:
        filepath (str): Path to the audio file.
    """
    song = pydub.AudioSegment.from_file(filepath) # type: ignore
    pydub.playback.play(song) # type: ignore

def main():
    while True:
        message: list[dict[str, str]] = []
        filepath = str(pathlib.Path(__file__).resolve().parent.joinpath("test.wav"))
        try:
            record_audio(filepath)
            text = speech_to_text(filepath)

            if text[:4].lower() == "open":
                subprocess.Popen(apps.get(text.split()[1].lower().replace(".", ""), ""))
            elif text[:4].lower() == "exit":
                exit()
            else:
                logger.info(f"Prompt: {text}")
                responds = fetch_response(text, message)
                logger.info(f"Result: {responds}")
                
                text_to_speech(responds, filepath)
                play_soundfile(filepath)

        except KeyboardInterrupt:
            logger.info("Recording interrupted by user.")

        except Exception:
            logger.error("An error occurred:", exc_info=True)

if __name__ == "__main__":
    main()
