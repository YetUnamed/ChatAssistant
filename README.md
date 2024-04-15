# Voice Assistant Script

This Python script is a basic voice assistant that allows users to record audio, convert speech to text, communicate with OpenAI's GPT-3.5 model for generating responses, convert text to speech, and perform various actions based on user commands.

## Features

- Record audio from the microphone and save it to a WAV file.
- Convert speech from an audio file to text using OpenAI's GPT-3.5 model.
- Interact with OpenAI's GPT-3.5 model to generate responses based on user prompts.
- Convert text to speech using OpenAI's text-to-speech model.
- Play audio files.

## Prerequisites

- Python 3.x
- Required Python packages: `pyaudio`, `pydub`, `keyboard`, `openai`
- An OpenAI API key for GPT-3.5 and TTS models

## Usage

1. Install the required Python packages by running `pip install -r requirements.txt`.
2. Set up an OpenAI API key and replace `API_KEY` in the script with your key.
3. Update the `apps` dictionary with the paths to the applications you want to open using voice commands.
4. Run the script using `python aiChatAssistant.py`.
5. Hold the specified key (default: `shift`) to start recording. Release the key to stop recording.
6. Once recording is complete, the script will convert the speech to text, interact with GPT-3.5 for generating responses, convert the response to speech, and play the audio.

## License

This script is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.