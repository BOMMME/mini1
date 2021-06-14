import time
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver


# 사용자의 입력과 선택을 받는 함수
class Crawl:

    def __init__(self, search_word, start_date, end_date, choose):
        self.search_word = search_word
        self.start_date = start_date
        self.end_date = end_date
        self.choose = choose

    def mini(self):
        # 사용자의 선택에 따라 실행되는 함수
        if self.choose == 1:
            return self.search_image(self.search_word, self.start_date, self.end_date)
        if self.choose == 2:
            return self.search_text(self.search_word, self.start_date, self.end_date)

    # 입력을 전달받아 이미지를 검색하는 함수
    def search_image(self, search_word, start_date, end_date):
        binary = 'C:\\chromedriver\\chromedriver.exe'
        browser = webdriver.Chrome(binary)
        url = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query={0}&nso=p%3Afrom{1}to{2}" \
            .format(search_word, start_date, end_date)
        browser.get(url)
        # 무한 스크롤
        prev_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            # 스크롤을 화면 가장 아래로 내린다
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(3)
            curr_height = browser.execute_script("return document.body.scrollHeight")
            if (curr_height == prev_height):
                break
            else:
                prev_height = curr_height
        time.sleep(3)
        # 소스코드 다운 & 원하는 값 추출
        html = browser.page_source
        browser.close()
        soup = BeautifulSoup(html, "lxml")
        img_list = soup.find_all("img", class_="_image _listImage")

        params = []
        for idx, val in enumerate(img_list):
            if val.get("data-lazy-src") is not None:
                params.append(val.get("data-lazy-src"))
            else:
                params.append(val.get("src"))
        # 이미지 다운로드
        self.img_num = self.download_image(params, search_word)
        return params, self.img_num

    # 입력을 전달받아 뉴스를 검색하는 함수

    def search_text(self, search_word, start_date, end_date):
        list_title = []
        address = []
        idx = 1  # url 페이지 넘기기 위한 인덱스
        parse_word = urllib.parse.quote(search_word)  # 한글인식이 안되서 url 파싱
        # 소스코드 다운 & 원하는 값 추출 반복
        while True:
            url_str = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=0&' \
                      'photo=0&field=0&pd=3&ds={1}&de={2}&cluster_rank=46&mynews=0&office_type=0&' \
                      'office_section_code=0&news_office_checked=&nso=so:r,p:from20200101to20200201,a:all&' \
                      'start={3}'.format(parse_word, start_date, end_date, idx)
            url = urllib.request.Request(url_str)
            result = urllib.request.urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(result, "html.parser")
            title = soup.find_all("a", class_="news_tit")
            for val in title:
                list_title.append(val["title"])
                address.append(val["href"])
            # 반복 여부 체크
            check = soup.find("a", class_="btn_next")
            if check["aria-disabled"] == "true":
                break
            else:
                idx += 10
        cnt = len(list_title)
        return address, list_title, cnt

    def download_image(self, params, search_word):
        a = 0
        for idx, p in enumerate(params, 1):
            # 다운받을 폴더 경로 입력
            urllib.request.urlretrieve(p, "C:\\image\\{}{}.jpg".format(search_word, str(idx)))
            a = idx
            if idx == 50:
                break
        return a
