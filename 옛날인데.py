import time
import datetime
import urllib.parse
import urllib.request
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
from selenium import webdriver
from wordcloud import WordCloud
def mini():
    # input 받는 부분
    search_word = input("어떤 검색어를 입력할까요? : ")
    start_date, end_date = input("기간을 설정해주세요(yyyymmdd~yyyymmdd): ").split('~')
    choose = int(input("1.이미지검색, 2.텍스트검색 (숫자를 골라주세요): "))
    # 사용자의 선택에 따라 실행되는 함수
    if choose == 1:
        search_image(search_word, start_date, end_date)
    if choose == 2:
        search_text(search_word, start_date, end_date)
def search_image(search_word, start_date, end_date):
    binary = 'C:\\chrome_driver\\chromedriver.exe'
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
    soup = BeautifulSoup(html, "lxml")
    img_list = soup.find_all("img", class_="_image _listImage")
    # 출력
    s_date = datetime.datetime.strptime(start_date, '%Y%m%d').date()
    e_date = datetime.datetime.strptime(end_date, '%Y%m%d').date()
    params = []
    for i in img_list:
        if i.get("data-lazy-src") is not None:
            params.append(i.get("data-lazy-src"))
            print(i.get("data-lazy-src"))
        else:
            params.append(i.get("src"))
            print(i.get("src"))
    print('\n{}부터 {} 사이에 {}은(는) {}개이고 내용은 위와 같습니다.'.format(s_date, e_date, search_word, len(img_list)))
    # 이미지 다운로드
    download_image(params,search_word)
def search_text(search_word, start_date, end_date):
    list_title = []
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
        for i in title:
            list_title.append(i["title"])
        # 반복 여부 체크
        check = soup.find("a", class_="btn_next")
        if check["aria-disabled"] == "true":
            break
        else:
            idx += 10
    # 출력
    s_date = datetime.datetime.strptime(start_date, '%Y%m%d').date()
    e_date = datetime.datetime.strptime(end_date, '%Y%m%d').date()
    title_str = ""
    for i in list_title:
        title_str += i + " "
        print(i)
    print('\n{}부터 {} 사이에 {}은(는) {} 개이고 내용은 위와 같습니다.'.format(s_date, e_date, search_word, len(list_title)))
    # 워드클라우드로 출력
    wordcloud = WordCloud(max_font_size=200, font_path='/content/drive/My Drive/Colab Notebooks/malgun.ttf',
                          background_color='white',
                          width=1200, height=800).generate(title_str)
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.show()

def download_image(params, search_word):
    for idx, p in enumerate(params,1):
        p1 = p.split('?src=')[1]
        p2 = p1.split('&type')[0]
        p3 = urllib.parse.unquote(p2)
        print(p3)
        # 다운받을 폴더 경로 입력
        urllib.request.urlretrieve(p3, "C:\\image\\{}{}.jpg".format(search_word, str(idx)))

        if idx == 50:
            break

# def download_image(params):
#     for idx, p in enumerate(params, 1):
#         # 다운받을 폴더 경로 입력
#         urllib.request.urlretrieve(p, "C:\pwork\Test\\" + str(idx) + ".png")
#         if idx == 50:
#             break
if __name__ == '__main__':
    mini()