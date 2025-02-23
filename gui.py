import platform
import sys
import threading
import speech_recognition as sr
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QScrollArea, QVBoxLayout, QWidget)
from screeninfo import get_monitors


class ApplicationInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.myName = 'Collin'
        self.initialMessage = f'Hi {self.myName}, what can I write down for you?'
        self.messages = ''
        self.initialRun = True
        self.counts = 0
        self.messageMicOn = '\n\nListening'
        self.messageTranscribeAudio = '\n\nProcessing Audio'


        # Set: Window size
        OS = platform.system()
        self.monitor = get_monitors()[0]
        if OS == "Darwin":
            # macOS
            self.heightWindow = self.monitor.height # No taskbar adjustment
            textboxSpacer = 0
        else:
            # Windows or Linux
            taskbarHeight = 613
            self.heightWindow = self.monitor.height - taskbarHeight
            textboxSpacer = 130
        self.widthWindow = 800
        self.resize(self.widthWindow, self.heightWindow)

        # Position the window at the center of the screen
        centerX = (self.monitor.width - self.widthWindow) // 2
        # print(f'Calculated X Position: {centerX}\n'
        #       f'{self.monitor.width}, {self.widthWindow}')
        if OS == "Darwin":
            centerY = (self.monitor.height - self.heightWindow) // 2
        else:
            centerY = 0
        self.move(centerX, centerY)

        # Parameters: Window
        self.font = 'Serif'
        self.fontSize = 25
        self.message = QLabel(f'')
        self.setWindowTitle('Application Name')
        self.setStyleSheet('background-color: #171717;')

        # Parameters: Buttons
        self.buttonWidth, self.buttonHeight = 220, 60
        self.isRecording = False
        self.endRecording = True
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.audioThread = None  # Thread for recording

        # Set the central widget
        self.appWindow = QWidget(self)
        self.setCentralWidget(self.appWindow)

        # Create: Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 0)

        # Create: Text box
        self.textBox = QScrollArea()
        self.textBox.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.textBox.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.message.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.textBox.setWidgetResizable(True)
        self.textBox.setWidget(self.message)
        self.message.setWordWrap(True)
        self.textBox.setFixedHeight(self.heightWindow - textboxSpacer)
        self.textBox.setStyleSheet(styleTextBox)

        # Add: Text box to the layout
        layout.addWidget(self.textBox)
        layout.addStretch(2)

        # Make: Button
        self.button = QPushButton('Record')
        self.button.setFixedSize(self.buttonWidth, self.buttonHeight)
        self.button.clicked.connect(self.toggleRecording)
        self.button.setStyleSheet(styleButton)
        self.button.setAutoDefault(False)

        # Add: Button to the layout
        layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(3)

        # Set the layout to the main window
        self.appWindow.setLayout(layout)


    def toggleRecording(self):
        # Start or stop recording based on button press
        if self.isRecording:
            self.button.setText('Record')
            self.button.setStyleSheet(styleButton)
            self.isRecording = False
            self.endRecording = True
        else:
            self.button.setText('Stop Recording')
            self.button.setStyleSheet(styleButtonPress)
            self.isRecording = True
            self.endRecording = False
            self.audioThread = threading.Thread(target=self.recordAudio)
            self.audioThread.start()
            self.initialRun = False


    def recordAudio(self):
        # Records and transcribe audio
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.isRecording:
                try:
                    textCurrent = self.message.text()
                    if textCurrent == '':
                        self.messages = self.initialMessage
                        self.message.setText(self.messages)
                    else:
                        self.message.setText(self.messages + self.messageMicOn)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    self.message.setText(self.messages + self.messageTranscribeAudio)
                    text = f'{self.recognizer.recognize_faster_whisper(audio).strip()}'
                    if self.isRecording:
                        self.toggleRecording() # Stop recording due to pause
                    if text != '':
                        self.updateMessage(text)
                except sr.UnknownValueError:
                    self.message.setText(self.messages +
                                         f'\nCould not understand the audio.')
                except sr.RequestError:
                    self.message.setText(self.messages +
                                         f'\nCould not request results, '
                                         f'check your internet connection.')


    def updateMessage(self, text):
        # Filter message
        if self.initialMessage in self.messages:
            self.messages = self.messages.replace(self.initialMessage, '')
        self.counts += 1

        # Update the message on the main thread
        if self.messages == '':
            self.messages = text
        else:
            self.messages += '\n' + text
        print(f'Message: {self.counts}\n'
              f'{self.messages}\n')
        self.message.setText(self.messages)



    def keyPressEvent(self, event):
        if event.key() == 16777216: # Qt.Key_Escape
            sys.exit()


# ===================== Define Button Parameters =====================
red = '#FF0000'
redDark = '#560000'
green = '#39FF14'
greenDark = '#002000'
greyLight = '#404040'
grey = '#252525'
black = '#202020'

styleButton = f"""
                QPushButton {{
                    color: {green};
                    background-color: {black};
                    border: 2px solid {green};
                    border-radius: 5px;
                    font-family: Serif;
                    font-size: 20px;
                    padding: 10px;
                    margin: 0;
                }}
                # QPushButton:hover {{
                #     color: {red};
                #     background-color: {greenDark};
                #     border: 2px solid {green};
                # }}
              """
styleButtonPress = f"""
                    QPushButton {{
                        color: {red};
                        background-color: {redDark};
                        border: 2px solid {red};
                        border-radius: 5px;
                        font-family: Serif;
                        font-size: 20px;
                        padding: 10px;
                        margin: 0;
                    }}
                    # QPushButton:hover {{
                    #     color: {green};
                    #     background-color: {redDark};
                    #     border: 2px solid {red};
                    # }}
                  """


styleTextBox = f"""
                QLabel {{
                    color: #3CD124;
                    background-color: {grey};
                    border: 2px solid {greyLight};
                    border-radius: 0px;
                    font-family: Serif;
                    font-size: 25px;
                    margin: 0px;
                }}
              """


# ===================== Run The Code =====================
app = QApplication(sys.argv)
gui = ApplicationInterface()
gui.show()
app.exec()
