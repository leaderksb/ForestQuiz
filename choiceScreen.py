# -*- coding: utf-8 -*- 파일 인코딩

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from tkinter import messagebox as msgBox
from tkinter import *

import playScreen
import socket

tk = Tk()
tk.withdraw()  # msgBox 호출로 인해 기본적으로 생성되는 창 제거

#HOST = "121.142.63.15"
HOST = "172.30.1.54"
PORT = 62302

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

choice = ""

# Qt Designer 로 만든 UI 파일
choiceUI = r'.\designer\choiceScreen.ui'


class ChoiceMainWindow(QMainWindow):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(choiceUI, self)  # UI 불러오기
        self.setFixedSize(1024, 768)  # 창크기 고정

        # 버튼 클릭시 함수호출
        self.rabbit_rad.clicked.connect(self.Groupbox)
        self.bear_rad.clicked.connect(self.Groupbox)
        self.choice_btn.clicked.connect(self.Choice)

        # UI에 이미지 추가
        choiceBackground_pix = QPixmap()  # QPixmap 객체 생성
        choiceBackground_pix.load('image/choiceBackground.png')  # QPixmap 객체에 이미지 불러오기
        self.choiceBackground_label.setPixmap(choiceBackground_pix)  # background_label 배경 이미지 설정
        self.choice_btn.setStyleSheet('image:url(image/choice.png); border:0px;')  # choice_btn 이미지, 테두리 투명하게 설정

    def Groupbox(self):
        global choice
        if self.rabbit_rad.isChecked():  # rabbit 선택
            choice = "rabbit"
        elif self.bear_rad.isChecked():  # bear 선택
            choice = "bear"
        else:
            choice = ""

    def Choice(self):
        if len(choice):  # 캐릭터를 선택했을 경우에만
            self.hide()  # choice_mainWindow 닫기
            playScreen.play_mainWindow = playScreen.PlayMainWindow()
            playScreen.play_mainWindow.show()
        else:  # 캐릭터를 선택하지 않았다면
            msgBox.showinfo("CHOICE", "캐릭터를 선택하세요.")

    def closeEvent(self, event):  # 창닫기 X 버튼 클릭 시
        # 이제부터 IP 접속 여부를 전송
        client_socket.send('connectChk'.encode())
        # 접속 종료 여부 전송
        client_socket.send('connectNo'.encode())
        self.deleteLater()  # 모든 창 종료
