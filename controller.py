import datetime
import cx_Oracle
# 기능 함수
# 기간 예외처리
def check_period(period):
    # 기간입력 예외처리
    try:
        start_date_t, end_date_t = period.split('~')
    except ValueError as e:
        return "~를 이용해 입력해주세요."
    if len(start_date_t) != 8:
        return "시작 기간의 자릿수가 맞지 않습니다."
    if len(end_date_t) != 8:
        return "끝 기간의 자릿수가 맞지 않습니다."
    try:
        datetime.datetime.strptime(start_date_t, "%Y%m%d")
    except:
        return "시작 기간이 올바른 날짜가 아닙니다."
    try:
        datetime.datetime.strptime(end_date_t, "%Y%m%d")
    except:
        return "끝 기간이 올바른 날짜가 아닙니다."
    if datetime.datetime.strptime(start_date_t, "%Y%m%d") > datetime.datetime.strptime(end_date_t, "%Y%m%d"):
        return "시작 기간이 끝 기간보다 늦습니다."
    if datetime.datetime.strptime(end_date_t, "%Y%m%d") > datetime.datetime.now():
        return "끝 기간이 오늘 날짜를 넘었습니다."
    return True
# SQL 관련 함수
class SQL:
    def __init__(self):
        self.dsn = cx_Oracle.makedsn("localhost", 1521, 'xe')  # oracle 주소를 입력
        self.db = cx_Oracle.connect('scott', 'tiger', self.dsn)  # oracle 접속 유져 정보
        self.cur = self.db.cursor()
    # INSERT
    def insert_image(self, search_word, href, start_date, end_date):
        self.cur.callproc('INSERT_IMAGE', [search_word, href, start_date, end_date])

    def insert_news(self, search_word, href, etc, start_date, end_date):
        self.cur.callproc('INSERT_NEWS', [search_word, etc, href, start_date, end_date])
    # SELECT

    # SELECT SEARCH_WORD
    def select_all(self):   #DB목록보기
        result1 = self.db.cursor()
        result2 = self.db.cursor()
        self.cur.callproc("SELECT_IMAGE_SW", ["C_IMAGE", result1])
        self.cur.callproc("SELECT_NEWS_SW", ["C_NEWS", result2])
        return result1, result2

    def select_search_word(self, search_word, choose): #상세보기
        if choose == 'C_IMAGE':
            result = self.db.cursor()
            self.cur.callproc("SELECT_IMAGE", [search_word, result])
            return result
        if choose == 'C_NEWS':
            result = self.db.cursor()
            self.cur.callproc("SELECT_NEWS", [search_word, result])
            return result