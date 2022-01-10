import pymysql

srchNum = 0  # 쿼리 검색 결과 개수
qno = ""
quiz = ""
answer = ""
rank = []  # 리스트 선언


# 해당하는 쿼리의 결과 개수 검색
def numSelect(sql):
    global srchNum  # 전역변수 사용
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute(sql)
            srchNum = curs.rowcount  # 검색한 row 개수를 전역변수에 저장
            # rs = curs.fetchall()
    finally:
        conn.close()


# 닉네임 검색
def nickSelect(id):
    global nickname  # 전역변수 사용
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select nickname from information where id = '" + id + "';")
            rs = curs.fetchall()
            nickname = rs[0][0]  # id 값으로 검색한 nickname 전역변수에 저장
    finally:
        conn.close()


# 회원정보 삽입
def signUpInsert(id, pw, nickname):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("insert into information values ('" + id + "', '" + pw + "', '" + nickname
                         + "', curdate(), 1, 0);")  # 가입일자, 기본 1레벨, 경험치 0
        conn.commit()
    finally:
        conn.close()


# 문제 검색
def questionSelect():
    global qno, quiz, answer  # 전역변수 사용
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("select * from question order by rand() limit 1;")
            rs = curs.fetchall()
            qno = rs[0][0]  # 문제 번호
            quiz = rs[0][1]  # 문제 내용
            answer = rs[0][2]  # 정답

    finally:
        conn.close()


# 점수 삽입
def scoreInsert(nickname, score):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("insert into score values ('" + nickname + "', '" + score + "');")  # 닉네임, 점수
        conn.commit()
    finally:
        conn.close()


# 순위 검색
def rankSelect():
    global rank  # 전역변수 리스트 사용
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            # 문자열 타입 숫자의 내림차순
            curs.execute("select * from score order by score * 1 desc limit 3;")
            cnt = curs.rowcount  # 검색한 row 개수를 변수에 저장
            rs = curs.fetchall()

            if cnt == 0:
                rank.clear()
                rank.append("1등 공석")  # 1등 이름
                rank.append("0")  # 1등 점수
                rank.append("2등 공석")  # 2등 이름
                rank.append("0")  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)
            elif cnt == 1:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append("2등 공석")  # 2등 이름
                rank.append("0")  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)
            elif cnt == 2:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append(rs[1][0])  # 2등 이름
                rank.append(rs[1][1])  # 2등 점수
                rank.append("3등 공석")  # 3등 이름
                rank.append("0")  # 3등 점수
                print(rank)

            else:
                rank.clear()
                rank.append(rs[0][0])  # 1등 이름
                rank.append(rs[0][1])  # 1등 점수
                rank.append(rs[1][0])  # 2등 이름
                rank.append(rs[1][1])  # 2등 점수
                rank.append(rs[2][0])  # 3등 이름
                rank.append(rs[2][1])  # 3등 점수
                print(rank)
    finally:
        conn.close()


# 접속한 IP 주소 삽입
def connectInsert(ip):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("insert into connect values ('" + ip + "');")  # IP 주소
        conn.commit()
    finally:
        conn.close()


# 접속했던 IP 주소 삭제
def connectDelete(ip):
    conn = pymysql.connect(host='localhost', user='root', passwd='11386013', db='tcpip', charset='utf8')
    try:
        with conn.cursor() as curs:
            curs.execute("delete from connect where ip = '" + ip + "';")
        conn.commit()
    finally:
        conn.close()
