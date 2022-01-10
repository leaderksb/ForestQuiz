# -*- coding: utf-8 -*- 파일 인코딩

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from playsound import playsound

import choiceScreen
import overScreen
import socket

#HOST = "121.142.63.15"
HOST = "172.30.1.54"
PORT = 62302

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

questionanswer = []  # 리스트 선언
score = 0
hp = 3

# Qt Designer 로 만든 UI 파일
playUI = r'.\designer\playScreen.ui'


class PlayMainWindow(QMainWindow):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(playUI, self)  # UI 불러오기
        self.setFixedSize(1024, 768)  # 창크기 고정

        # UI에 이미지 추가
        hp_pix = QPixmap()  # QPixmap 객체 생성
        hp_pix.load('image/hp3.png')  # QPixmap 객체에 이미지 불러오기
        self.hp_label.setPixmap(hp_pix)  # hp_label 배경 이미지 설정
        self.answer_btn.setStyleSheet('image:url(image/send.png); border:0px;')  # answer_btn 이미지, 테두리 투명하게 설정

        if choiceScreen.choice == "rabbit":
            # UI에 이미지 추가
            choiceBackground_pix = QPixmap()  # QPixmap 객체 생성
            choiceBackground_pix.load('image/playScreen_background_rabbit.jpg')  # QPixmap 객체에 이미지 불러오기
            self.choiceBackground_label.setPixmap(choiceBackground_pix)  # choiceBackground_label 배경 이미지 설정

        elif choiceScreen.choice == "bear":
            # UI에 이미지 추가
            choiceBackground_pix = QPixmap()  # QPixmap 객체 생성
            choiceBackground_pix.load('image/playScreen_background_bear.jpg')  # QPixmap 객체에 이미지 불러오기
            self.choiceBackground_label.setPixmap(choiceBackground_pix)  # choiceBackground_label 배경 이미지 설정

        self.Question()

        # 버튼 클릭시 함수호출
        self.answer_btn.clicked.connect(self.SubmitAnswer)

    def Question(self):
        global questionanswer
        self.answer_lineEdit.setText("")  # answer_lineEdit 공백 클리어

        # 이제부터 문제 정보를 저장
        client_socket.send('question'.encode())
        # 문제 정보 수신
        question = client_socket.recv(1024)
        questionanswer = question.decode().split('\n')

        print(questionanswer)
        self.question_label.setText(questionanswer[0])  # question_label 문제 제시

    def SubmitAnswer(self):
        global score, hp, questionanswer  # 전역변수 선언
        if self.answer_lineEdit.text() == questionanswer[1]:  # 정답일 경우
            playsound("sound/correct.mp3")
            score += 5
            self.score.setText(str(score))
            self.Question()

        else:  # 오답일 경우
            playsound("sound/wrong.mp3")
            hp -= 1
            if hp == 2:
                # UI에 이미지 추가
                hp_pix = QPixmap()  # QPixmap 객체 생성
                hp_pix.load('image/hp2.png')  # QPixmap 객체에 이미지 불러오기
                self.hp_label.setPixmap(hp_pix)  # hp_label 배경 이미지 설정
            elif hp == 1:
                # UI에 이미지 추가
                hp_pix = QPixmap()  # QPixmap 객체 생성
                hp_pix.load('image/hp1.png')  # QPixmap 객체에 이미지 불러오기
                self.hp_label.setPixmap(hp_pix)  # hp_label 배경 이미지 설정
            elif hp == 0:
                # 이제부터 순위 정보를 저장
                client_socket.send('score'.encode())
                # 점수 전송
                client_socket.send(str(score).encode())

                self.hide()
                overScreen.OverMainWindow = overScreen.OverMainWindow()
                overScreen.OverMainWindow.show()

    def closeEvent(self, event):  # 창닫기 X 버튼 클릭 시
        # 이제부터 IP 접속 여부를 전송
        client_socket.send('connectChk'.encode())
        # 접속 종료 여부 전송
        client_socket.send('connectNo'.encode())
        self.deleteLater()  # 모든 창 종료
