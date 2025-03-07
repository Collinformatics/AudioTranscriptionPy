# Requirements:

If you have an NVIDIA GPU install:

- NVIDIA (R) Cuda compiler driver V12.5.40

- NVIDIA cuDNN V12.5

# Installing Program:

Modules:

- For MacOS, or if your computer does not have an NVIDIA GPU:

        pip install torch torchvision torchaudio

- If your computer has an NVIDIA GPU:

        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

- Install the remaining modules:

        pip install deepmultilingualpunctuation
    
        pip install faster-whisper
    
        pip install PyAudio
    
        pip install soundfile
    
        pip install SpeechRecognition

# Testing installation:

Run test.py to evaluate:

- If the Python interpreter was setup correctly

- GPU Usage

    - Only relevant if your computer has an NVIDIA graphics card

# Running The Program:

The program will save your transcribed messages in the "logs" folder

- Open "log.txt" to view and edit the text
