# HAL 9000 AI

A Python-based AI inspired by HAL 9000, designed to interact with users through speech. This project was developed on a Raspberry Pi 4 running Ubuntu Jammy and utilizes Python 3.11.5. HAL 9000 brings voice-activated responses and advanced text-to-speech (TTS) functionality with a sleek, dark-themed interface powered by PyQt.

## Features
- **Voice Commands**: Communicate directly with HAL 9000 through voice commands.
- **Audio Feedback**: Real-time, natural TTS responses.
- **Dynamic GUI**: A responsive PyQt interface with visualizations for a more engaging user experience.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)

## Getting Started
To get HAL 9000 up and running, follow the steps below to install dependencies and configure your environment.

## Prerequisites
Ensure you have the following libraries installed, as they are required for this project:
- `PyQt5`
- `pyqtgraph`
- `qdarkstyle`
- `openai`
- `speech_recognition`
- `pydub`

You may also need additional drivers for microphone and speaker compatibility on the Raspberry Pi.

## Installation
1. **Set Up Python Environment**: Install Python 3.11.5 if you haven't already. [Python Installation Guide](https://www.python.org/downloads/).
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/hal9000-ai.git
   cd hal9000-ai
   ```
3. **Install Dependencies**
   ```bash
   pip3 install PyQt5 pyqtgraph qdarkstyle openai speech_recognition pydub
   ```
4. **Configure Audio Drivers**: Install any necessary drivers for your microphone and speaker. You can follow an audio configuration guide for Raspberry Pi.

## Usage
1. **Launch the program:**
   ```bash
   python3 hal9000.py
   ```
2. **Interact with HAL 9000:"
- Speak commands into the microphone to interact with HAL 9000.
- HAL will respond with TTS audio feedback and update its GUI in real time.
3. **Graphical Interface:"
- The PyQt interface includes visualizations that reflect audio waveform and feedback.
- An interactive shutdown protocol from HAL is provided.
- A logger displaying the status of the system **OR** the dialog between the user and HAL.

## Troubleshooting
- **Audio Issues:** Ensure microphone and speaker drivers are correctly installed and configured. Verify settings in the OS’s audio settings panel.
- **Library Installation:** Double-check that all Python dependencies are installed, especially if you're experiencing module import errors.

## License
- Navigate to the **LICENSES** directory to understand how to use the code legally.


[![Demo Video](https://img.youtube.com/vi/PkM0fvH8Xlw/0.jpg)](https://www.youtube.com/watch?v=PkM0fvH8Xlw)
