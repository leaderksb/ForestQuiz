# -*- coding: utf-8 -*- 파일 인코딩

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

import socket

#HOST = "121.142.63.15"
HOST = "172.30.1.54"
PORT = 62302

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Qt Designer 로 만든 UI 파일
overUI = r'.\designer\overScreen.ui'


class OverMainWindow(QMainWindow):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(overUI, self)  # UI 불러오기
        self.setFixedSize(1024, 768)  # 창크기 고정

        # UI에 이미지 추가
        overBackground_pix = QPixmap()  # QPixmap 객체 생성
        overBackground_pix.load('image/overScreenBackground.png')  # QPixmap 객체에 이미지 불러오기
        self.overBackground_label.setPixmap(overBackground_pix)  # overBackground_label 배경 이미지 설정
        self.exit_btn.setStyleSheet('image:url(image/exit.png); border:0px;')  # exit_btn 이미지, 테두리 투명하게 설정

        # 이제부터 순위 정보를 전송
        client_socket.send('rank'.encode())

        # 순위 정보 수신
        rank = client_socket.recv(1024)
        namescore = rank.decode().split('\n')

        self.fstname.setText(namescore[0])
        self.fstscore.setText(namescore[1])
        self.sndname.setText(namescore[2])
        self.sndscore.setText(namescore[3])
        self.trdname.setText(namescore[4])
        self.trdscore.setText(namescore[5])
        self.myname.setText(namescore[6])
        self.myscore.setText(namescore[7])

        self.exit_btn.clicked.connect(self.exitClicked)

    def exitClicked(self):
        # 이제부터 IP 접속 여부를 전송
        client_socket.send('connectChk'.encode())
        # 접속 종료 여부 전송
        client_socket.send('connectNo'.encode())
        self.deleteLater()

    def closeEvent(self, event):  # 창닫기 X 버튼 클릭 시
        # 이제부터 IP 접속 여부를 전송
        client_socket.send('connectChk'.encode())
        # 접속 종료 여부 전송
        client_socket.send('connectNo'.encode())
        self.deleteLater()  # 모든 창 종료
