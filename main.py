#hiddenimports=['pygame','json','requests','time','bs4'],
import requests
from pygame import mixer
import time
import json
from bs4 import BeautifulSoup
mixer.init()
def do_alarm():
    mixer.music.load('./alarm.mp3')
    mixer.music.play()
if __name__ == "__main__":
    print(">>> 코인빗 공지사항 감시 프로그램")
    DELAY =  int( input(">>> 감시 주기 초단위 입력 ( 정수 ) ::"))
    print(">>> [코인빗] 감시 시작 ")
    print("_"*30)
    html = requests.get('https://www.coinbit.co.kr/webbbsmain/noticelists/chno-100/&page=1/&subject=')
    jsonStr = json.loads(html.text)
    bbsNoList = []
    # Init build DB
    for article in jsonStr:
        bbsNoList.append(article['bbs_no'])

    idx = 0
    # Monitor
    while True:
        idx += 1
        if idx == 5:
            bbsNoList.remove('28061')
        while True:
            try:
                html = requests.get('https://www.coinbit.co.kr/webbbsmain/noticelists/chno-100/&page=1/&subject=')
                jsonStr = json.loads(html.text)
                break
            except:
                print("\t>>> 네트워크 지연 감지 계속 반복해서 뜰시 연락 부탁드립니다.")
                time.sleep(2)
        # Init build DB
        for article in jsonStr:
            if article['bbs_no'] not in bbsNoList:
                do_alarm()
                bbsNoList.append(article['bbs_no'])
                now = time.localtime()
                s = "%04d-%02d-%02d %02d:%02d:%02d" % (
                    now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
                bs = BeautifulSoup(article['content'], 'lxml')
                print(">>> [코인빗] 감지   : ", s)
                print(">>> [코인빗] TITLE  : ", article['subject'])
                print(">>> [코인빗] CONTENT : ", bs.get_text())
        time.sleep(DELAY)