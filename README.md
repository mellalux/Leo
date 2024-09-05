# Hey Siri like project

This project uses OpenAI functions to act like Siri.

This project is a Python-based application that utilizes the OpenAI API, records audio, plays back sound, and handles environment variables securely with `.env` files. It also includes audio processing using `pyaudio` and `numpy`.

## Features
- Uses the **OpenAI API** for text generation.
- Records audio using **PyAudio**.
- Detects silence and stops recording automatically.
- Plays sound using **playsound**.
- Handles sensitive environment variables using **python-dotenv**.
- Basic audio processing using **numpy**.

## Prerequisites

Before running the project, ensure you have the following installed:
- Python 3.6+
- Pip (Python package installer)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/mellalux/Leo
    cd Leo
    ```

2. **Create a virtual environment**:
    - On Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      python -m venv venv
      source venv/bin/activate
      ```

3. **Install the required dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file**: in the root directory and add your OpenAI API key:

## Usage

1. **Run the script**:
    ```bash
    python Leo.py
    ```

2. **Recording audio**: The script will start recording audio from your microphone. It will stop recording when silence is detected.

3. **API integration**: The script will generate a response from OpenAI based on user input, convert text to speech, and play it back using `playsound`.

4. **Stopping script**: To stop the script, the user must say "stop listening" or "bye for now" during script listening.

## Example `.env` File

    This project uses the `.env` file to manage the OpenAI API key. Here’s an example of what your `.env` file should look like:
    ```bash
    OPENAI_API_KEY=your_openai_api_key_here
    ```
    Make sure to replace `your_openai_api_key_here` with your actual OpenAI API key.

## Project Structure **:
    Leo/| 
        ├── venv/ # Virtual environment directory 
        ├── Leo.py # Main Python script 
        ├── requirements.txt # List of required Python packages 
        ├── .env # Environment variables file (not included in version control) 
        └── README.md # This documentation file

### Dependencies

    This project requires the following Python libraries:

- **openai**: For interaction with the OpenAI API.
- **pyaudio**: For recording and processing audio.
- **playsound**: For playing audio files.
- **numpy**: For audio processing (detecting silence).
- **python-dotenv**: For handling environment variables securely.

    All required packages can be installed using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### Troubleshooting

- **playaudio**: To install it on Windows, you can use this command:

    ```bash
    pip install playsound@git+https://github.com/taconi/playsound
    ```

- **PyAudio**: Installation: If you run into issues installing pyaudio, you may need to install it manually for your system. On Windows, you can use a pre-built binary from this page.

    On Linux:
    ```bash
    sudo apt-get install portaudio19-dev python-pyaudio
    ```
- **OpenAI API key**: Missing OpenAI API Key: Ensure that your .env file is correctly configured and contains the OpenAI API key.