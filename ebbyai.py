from PyQt5.QtWidgets import QWidget,QSlider,QApplication,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QLineEdit,QTextEdit
from PyQt5.QtGui import QFont , QPixmap
from PyQt5.QtCore import Qt ,QSize
import sys
import pyttsx3
import speech_recognition
import os
import openai
api = r"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"
openai.api_key = api

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.root()
        
    def root(self):
        self.pixmap  = QPixmap(r"C:\Users\walri\Desktop\Python\Artificial Intelligence\GPT-CHATBOT\whoami.PNG")
        self.picture = self.pixmap.scaled(500, 889)
        self.resim      = QLabel()
        self.resim.setPixmap(self.picture)
        
        
        
        self.slider_text = QLabel("Creativity : ")
        self.slider_text.setFont(QFont("Arial",15))
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,100)
        self.slider.setPageStep(10)

        
        
        self.ai = QTextEdit()
        self.ai.setFont(QFont('Arial',15))
        self.ui = QTextEdit()
        self.ui.setFont(QFont('Arial', 15))
        self.mic = QPushButton("Mic")
        self.mic.setFont(QFont('Arial', 13))
        self.send = QPushButton("Send")
        self.send.setFont(QFont('Arial', 13))

        hbox = QHBoxLayout()
        slider_hbox = QHBoxLayout()
        slider_hbox.addWidget(self.slider_text)
        slider_hbox.addWidget(self.slider)
        vbox_picture = QVBoxLayout()
        vbox_picture.addWidget(self.resim)
        vbox = QVBoxLayout()
        vbox.addWidget(self.ai)
        vbox.addWidget(self.ui)
        vbox.addLayout(slider_hbox)

        vbox.addWidget(self.mic)
        vbox.addWidget(self.send)
        
        hbox.addLayout(vbox_picture)
        hbox.addLayout(vbox)
        
        self.send.clicked.connect(self.send_data)
        self.mic.clicked.connect(self.take_commands)
        #self.setFixedSize(1200,900)
        self.setFixedHeight(900)
        self.setMaximumWidth(1920)
        self.setMinimumWidth(1200)
        self.setLayout(hbox)
        self.setWindowTitle("EbbyAI")
        self.show()
        
    def send_data(self):
        data = self.ui.toPlainText()

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=data,
            temperature=float(self.slider.value()/100),
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=[" Human:", " AI:"]
            )

        text = response['choices'][0]['text']
        self.ai.setText(str(text))
    
    def take_commands(self):

        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            print('Listening')
            recognizer.pause_threshold = 0.7
            audio = recognizer.listen(source)
            try:
                print("Recognizing")
                Query = recognizer.recognize_google(audio)
                self.ui.setText(str(Query))
                self.send_data()
                engine = pyttsx3.init()
                engine.say(str(self.ai.toPlainText()))
                engine.runAndWait()
            except Exception as e:
                print(e)
                print("Say that again")
                return "None"
        
                
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
