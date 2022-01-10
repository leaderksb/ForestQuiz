# -*- coding: utf-8 -*- 파일 인코딩

import sys

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from tkinter import messagebox as msgBox
from tkinter import *

import choiceScreen
import socket

tk = Tk()
tk.withdraw()  # msgBox 호출로 인해 기본적으로 생성되는 창 제거

#HOST = "121.142.63.15"
HOST = "172.30.1.54"
PORT = 62302

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Qt Designer 로 만든 UI 파일
startUI = r'.\designer\startScreen.ui'
signUpUI = r'.\designer\signUpScreen.ui'


class StartMainWindow(QMainWindow):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(startUI, self)  # UI 불러오기
        self.setFixedSize(1024, 768)  # 창크기 고정

        regExp = QRegExp("[A-Za-z0-9]*")  # 알파벳과 숫자만 임의의 개수만큼 가능
        self.idLog_lineEdit.setValidator(QRegExpValidator(regExp, self))  # idSign_lineEdit 에 영문 및 숫자 외 모든 문자 입력막기
        self.pwLog_lineEdit.setEchoMode(QLineEdit.Password)  # pwLog_lineEdit 패스워드로 설정

        # 버튼 클릭시 함수호출
        self.login_btn.clicked.connect(self.LoginClicked)
        self.signup_btn.clicked.connect(self.SignUpClicked)

        # UI에 이미지 추가
        background_pix = QPixmap()  # QPixmap 객체 생성
        background_pix.load('image/startBackground.png')  # QPixmap 객체에 이미지 불러오기
        self.background_label.setPixmap(background_pix)  # background_label 배경 이미지 설정
        self.login_btn.setStyleSheet('image:url(image/login.png); border:0px;')  # login_btn 이미지, 테두리 투명하게 설정
        self.signup_btn.setStyleSheet('image:url(image/signup.png); border:0px;')

        # 이제부터 IP 접속 여부를 전송
        client_socket.send('connectChk'.encode())

        # 현재 접속 중인 IP 개수 수신
        ipnum = client_socket.recv(1024)

        if ipnum.decode() == "1":  # 접속 중인 IP
            msgBox.showinfo("CONNECT FAIL", "이미 실행 중입니다.")
            self.deleteLater()  # 게임 강제종료

        # 접속 시작 여부 전송
        client_socket.send('connectYes'.encode())

    def LoginClicked(self):
        if len(self.idLog_lineEdit.text()):  # idLog_lineEdit 입력값이 있다면
            if len(self.pwLog_lineEdit.text()):  # pwLog_lineEdit 입력값이 있다면
                # 이제부터 로그인 정보를 전송
                client_socket.send('loginChk'.encode())
                # 아이디 \n 비밀번호 전송
                client_socket.send(
                    self.idLog_lineEdit.text().encode() + '\n'.encode() + self.pwLog_lineEdit.text().encode())

                # 로그인 성공 정보 수신
                loginChk = client_socket.recv(1024)
                print('Received from the server :', repr(loginChk.decode()))

                if repr(loginChk.decode()) == "'loginOk'":
                    start_mainWindow.hide()  # start_mainWindow 닫기
                    choiceScreen.choice_mainWindow = choiceScreen.ChoiceMainWindow()
                    choiceScreen.choice_mainWindow.show()
                else:
                    msgBox.showinfo("LOGIN FAIL", "아이디 또는 비밀번호를 확인하세요.")
            else:  # pwLog_lineEdit 입력값이 없다면
                msgBox.showinfo("LOGIN FAIL", "비밀번호를 입력하세요.")
        else:  # idLog_lineEdit 입력값이 없다면
            msgBox.showinfo("LOGIN FAIL", "아이디를 입력하세요.")

    def SignUpClicked(self):
        signUp_dialog = SignUpDialog()
        signUp_dialog.show()
        signUp_dialog.exec_()

    def closeEvent(self, event):  # 창닫기 X 버튼 클릭 시
        # 이제부터 IP 접속 여부를 전송
        client_socket.send('connectChk'.encode())
        # 접속 종료 여부 전송
        client_socket.send('connectNo'.encode())
        self.deleteLater()  # 모든 창 종료


class SignUpDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self, None)
        uic.loadUi(signUpUI, self)  # UI 불러오기
        self.setFixedSize(400, 500)  # 창크기 고정

        regExp = QRegExp("[A-Za-z0-9]*")  # 알파벳과 숫자만 임의의 개수만큼 가능
        self.idSign_lineEdit.setValidator(QRegExpValidator(regExp, self))  # idSign_lineEdit 에 영문 및 숫자 외 모든 문자 입력막기
        self.pwSign_lineEdit.setEchoMode(QLineEdit.Password)  # pwSign_lineEdit 패스워드로 설정
        self.pwSignCnf_lineEdit.setEchoMode(QLineEdit.Password)  # pwSignCnf_lineEdit 패스워드로 설정

        # 버튼 클릭시 함수호출
        self.ok_btn.clicked.connect(self.SignUp)  # ok 클릭시
        self.cancel_btn.clicked.connect(self.Cancel)

        # UI에 이미지 추가
        signUpBackground_pix = QPixmap()  # QPixmap 객체 생성
        signUpBackground_pix.load('image/signUpBackground.png')  # QPixmap 객체에 이미지 불러오기
        self.signUpBackground_label.setPixmap(signUpBackground_pix)  # background_label 배경 이미지 설정
        self.ok_btn.setStyleSheet('image:url(image/ok.png); border:0px;')  # ok_btn 이미지, 테두리 투명하게 설정
        self.cancel_btn.setStyleSheet('image:url(image/cancel.png); border:0px;')

    def SignUp(self):
        if len(self.idSign_lineEdit.text()):  # idSign_lineEdit 입력값이 있다면
            if len(self.pwSign_lineEdit.text()):  # pwSign_lineEdit 입력값이 있다면
                if len(self.pwSignCnf_lineEdit.text()):  # pwSignCnf_lineEdit 입력값이 있다면
                    if len(self.nick_lineEdit.text()):  # nick_lineEdit 입력값이 있다면
                        if self.pwSign_lineEdit.text() == self.pwSignCnf_lineEdit.text():  # 비밀번호 입력이 일치하는지 확인
                            # 이제부터 회원가입 정보를 전송
                            client_socket.send('signUpChk'.encode())
                            # 아이디 \n 비밀번호 \n 닉네임 전송
                            client_socket.send(self.idSign_lineEdit.text().encode() + '\n'.encode()
                                               + self.pwSign_lineEdit.text().encode() + '\n'.encode()
                                               + self.nick_lineEdit.text().encode())
                            # 아이디 중복 정보 수신
                            signUpChk = client_socket.recv(1024)
                            if repr(signUpChk.decode()) == "'signUpOk'":
                                msgBox.showinfo("SIGN UP SUCCESS", "회원가입이 완료되었습니다.")
                                self.Cancel()  # SignUpDialog 닫기
                            else:  # id 입력값이 DB에 존재한다면
                                msgBox.showinfo("SIGN UP FAIL", "이미 존재하는 아이디입니다.")
                        else:
                            msgBox.showinfo("SIGN UP FAIL", "비밀번호를 확인하세요.")
                    else:  # nick_lineEdit 입력값이 없다면
                        msgBox.showinfo("SIGN UP FAIL", "닉네임을 입력하세요.")
                else:  # pwSignCnf_lineEdit 입력값이 없다면
                    msgBox.showinfo("SIGN UP FAIL", "비밀번호를 확인하세요.")
            else:  # pwSign_lineEdit 입력값이 없다면
                msgBox.showinfo("SIGN UP FAIL", "비밀번호를 입력하세요.")
        else:  # idSign_lineEdit 입력값이 없다면
            msgBox.showinfo("SIGN UP FAIL", "아이디를 입력하세요.")

    def Cancel(self):
        self.close()  # signUp_dialog 닫기


app = QApplication(sys.argv)  # 기본적으로 프로그램을 실행
start_mainWindow = StartMainWindow()
start_mainWindow.show()
app.exec_()  # 프로그램을 무한루프 안에서 계속 실행시키고 프로그램에서 벌어지는 이벤드를 받아 처리하는 이벤트루프
