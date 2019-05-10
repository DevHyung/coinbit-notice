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
    ''' ===== CONFIG AREA START ===== '''
    print(">>> 코인빗 공지사항 감시 프로그램")
    DELAY =  int( input(">>> 감시 주기 초단위 입력 ( 정수 ) ::"))
    print(">>> [코인빗] 감시 시작 ")
    print("_"*30)

    ''' ===== Init build DB ===== '''
    bbsNoList = []

    html = requests.get('https://www.coinbit.co.kr/webbbsmain/noticelists/chno-100/&page=1/&subject=')
    jsonStr = json.loads(html.text)

    for article in jsonStr:
        bbsNoList.append(article['bbs_no'])

    ''' ===== MONITOR ===== '''
    while True:
        # Get json source code
        while True:
            try:
                html = requests.get('https://www.coinbit.co.kr/webbbsmain/noticelists/chno-100/&page=1/&subject=')
                jsonStr = json.loads(html.text)
                break
            except:
                print("\t>>> 네트워크 지연 감지 계속 반복해서 뜰시 연락 부탁드립니다.")
                time.sleep(2)

        # SEARCH bbs to bbsNoList
        for article in jsonStr:
            if article['bbs_no'] not in bbsNoList:
                do_alarm()
                bbsNoList.append(article['bbs_no'])
                now = time.localtime()
                s = "%04d-%02d-%02d %02d:%02d:%02d" % (
                    now.tm_year, now.tm_mon, now.tm_mday,
                    now.tm_hour, now.tm_min, now.tm_sec)

                print(">>> [코인빗] 감지   : ", s)
                try:
                    print(">>> [코인빗] TITLE  KR : ", article['subject_kr'])
                except:
                    print(">>> [코인빗] TITLE  ALL: ", article['subject'])

                try:
                    bs = BeautifulSoup(article['content_kr'], 'lxml')
                    print(">>> [코인빗] CONTENT KR : ", bs.get_text())
                except:
                    bs = BeautifulSoup(article['content'], 'lxml')
                    print(">>> [코인빗] CONTENT ALL: ", bs.get_text())

        print("감시중 .. \n")
        time.sleep(DELAY)