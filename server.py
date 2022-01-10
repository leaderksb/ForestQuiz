import DB
import socket
from _thread import *
import threading
from time import sleep

nickDictionary = {}  # 현재 연결된 IP 주소 : 닉네임
scoreDictionary = {}  # 현재 연결된 IP 주소 : 점수
nickLock = threading.Lock()  # 뮤텍스
scoreLock = threading.Lock()


# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신
def threaded(client_socket, addr):
    print('Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복
    while True:
        global nickDictionary, scoreDictionary
        try:
            # 어떤 데이터를 주고받을 것인지 판단할 문자열 저장
            data = client_socket.recv(1024)

            if not data:
                print('Disconnected by ' + addr[0], ':', addr[1])
                break

            print('Received from ' + addr[0], ':', addr[1], ':', data.decode())

            if data.decode() == 'connectChk':
                print('@@@@  connectChk  @@@@')

                DB.numSelect("select * from connect where ip = '" + addr[0] + "';")  # 현재 접속 중인 IP 개수 검색
                client_socket.send(str(DB.srchNum).encode())

                connect = client_socket.recv(1024)

                if connect.decode() == 'connectYes':  # IP 주소에서 게임을 시작 했다면
                    DB.connectInsert(addr[0])
                elif connect.decode() == 'connectNo':  # IP 주소에서 게임을 종료 했다면
                    DB.connectDelete(addr[0])

            # 로그인 정보 확인
            if data.decode() == 'loginChk':
                print('@@@@  loginChk  @@@@')
                login = client_socket.recv(1024)
                idpw = login.decode().split('\n')

                DB.numSelect("select * from information where id = '" + idpw[0]
                             + "' and pw = '" + idpw[1] + "';")

                if DB.srchNum >= 1:
                    DB.nickSelect(idpw[0])

                    nickLock.acquire()  # 다른 Thread 접근 불가 하도록 잠금
                    sleep(0.1)  # 지연

                    nickDictionary[addr[0]] = DB.nickname  # 딕셔너리에 키 : 밸류 형식으로 닉네임 저장

                    nickLock.release()  # 다른 Thread 접근 가능 하도록 잠금 해제

                    client_socket.send('loginOk'.encode())
                else:  # 존재하지 않는 아이디라면
                    client_socket.send('loginNo'.encode())

            # 회원가입 정보 저장
            if data.decode() == 'signUpChk':
                print('@@@@  signUpChk  @@@@')
                signUp = client_socket.recv(1024)
                print(signUp.decode())
                idpwnick = signUp.decode().split('\n')

                DB.numSelect("select * from information where id = '" + idpwnick[0]
                             + "' and pw = '" + idpwnick[1] + "';")
                if DB.srchNum == 0:
                    DB.signUpInsert(idpwnick[0], idpwnick[1], idpwnick[2])
                    client_socket.send('signUpOk'.encode())
                else:  # 이미 존재하는 아이디라면
                    client_socket.send('signUpNo'.encode())

            # 문제와 정답 정보 전송
            if data.decode() == 'question':
                print('@@@@  question  @@@@')

                DB.questionSelect()  # 랜덤으로 문제와 정답 하나 가져옴
                print("[ 문제 : " + DB.quiz + " ] [ 정답 : " + DB.answer + " ]")

                client_socket.send(DB.quiz.encode() + '\n'.encode() + DB.answer.encode())

            # 순위 정보 저장
            if data.decode() == 'score':
                print('@@@@  score  @@@@')
                score = client_socket.recv(1024)

                scoreLock.acquire()  # 다른 Thread 접근 불가 하도록 잠금
                sleep(0.1)  # 지연

                scoreDictionary[addr[0]] = score.decode()  # 딕셔너리에 키 : 밸류 형식으로 점수 저장

                DB.scoreInsert(nickDictionary[addr[0]], scoreDictionary[addr[0]])
                scoreLock.release()  # 다른 Thread 접근 가능 하도록 잠금 해제

            # 순위 정보 전송
            if data.decode() == 'rank':
                print('@@@@  rank  @@@@')
                sleep(0.3)  # 실행순서 오류가 발생하여 지연으로 처리속도의 시간차를 맞춤

                scoreLock.acquire()  # 다른 Thread 접근 불가 하도록 잠금
                sleep(0.1)  # 지연

                DB.rankSelect()

                client_socket.send(DB.rank[0].encode() + '\n'.encode() + DB.rank[1].encode() + '\n'.encode()
                                    + DB.rank[2].encode() + '\n'.encode() + DB.rank[3].encode() + '\n'.encode()
                                    + DB.rank[4].encode() + '\n'.encode() + DB.rank[5].encode() + '\n'.encode()
                                    + nickDictionary[addr[0]].encode() + '\n'.encode() + scoreDictionary[addr[0]].encode() )

                scoreLock.release()  # 다른 Thread 접근 가능 하도록 잠금 해제

        except ConnectionResetError as e:
            print('Disconnected by ' + addr[0], ':', addr[1])
            print(e)
            break

    client_socket.close()


HOST = '172.30.1.54'
PORT = 62302

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

print('server start')

while True:
    print('wait')

    client_socket, addr = server_socket.accept()  # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴
    start_new_thread(threaded, (client_socket, addr))  # 새로운 쓰레드에서 해당 소켓을 사용해 통신

server_socket.close()
