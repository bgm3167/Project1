import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import json
import csv

file=open("news0802.csv",mode="w",encoding="utf-8",newline="")
writer=csv.writer(file)
start_date = datetime(2023, 8, 2)
end_date = datetime(2023, 8, 2)
oid = '001'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
headers2 ={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}

while start_date <= end_date:
    date = start_date.strftime('%Y%m%d')
    page = 1


    while True:
        params = {
            'mode': 'LPOD',
            'mid': 'sec',
            'oid': '001',
            'date': date,
            'page': str(page)
        }

        res = requests.get('https://news.naver.com/main/list.naver', params=params, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        now_page = int(soup.select_one('div.paging strong').text.strip())

        if page != now_page:
            break
        
        list1 = soup.select('ul.type06_headline > li')
        list2 = soup.select('ul.type06 > li')
        lists = list1 + list2

        for idx, list in enumerate(lists):
            url = list.select_one('a').attrs['href']
            part = url.split('/')[-1]
            res_content = requests.get(url, headers=headers)
            soup_content = BeautifulSoup(res_content.text, 'html.parser')
            url2 = 'https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery33108123303875121677_1694998617015&q=JOURNALIST%5B56791(period)%5D%7CNEWS%5Bne_001_{0}%5D&isDuplication=false&cssIds=MULTI_MOBILE%2CNEWS_MOBILE&_=1694998617016'.format(part)
            res2 = requests.get(url2, headers=headers2)
            url3 = 'https://sports.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery1113009776804219006707_1695014223676&q=SPORTS%5Bne_001_{0}%5D%7CJOURNALIST%5B56754(period)%5D%7CSPORTS_MAIN%5Bne_001_0014164626%5D&isDuplication=false&cssIds=MULTI_PC%2CSPORTS_PC&_=1695014223677'.format(part)
            res3 = requests.get(url3, headers=headers2)
            url4 = 'https://news.like.naver.com/v1/search/contents?suppress_response_codes=true&callback=jQuery111108346120242703736_1695015332108&q=ENTERTAIN%5Bne_001_{0}%5D%7CENTERTAIN_MAIN%5Bne_001_0014199923%5D&isDuplication=false&cssIds=MULTI_PC%2CENTERTAIN_PC&_=1695015332109'.format(part)
            res4 = requests.get(url4, headers=headers2)

            title = ''
            content = ''

            if soup_content.select_one('h2#title_area') != None:
                title = soup_content.select_one('h2#title_area').text.strip()
                content = soup_content.select_one('article#dic_area').text.replace('\n', '').strip()
                section = soup_content.select_one('#contents > div.media_end_categorize > a > em')
                if section is not None:
                   section = section.text.strip()
                else:
                   section = '기타'
                json_data = re.search(r'\(({.*})\)', res2.text).group(1)
                emoge ={}
                emog = [0,0,0,0,0]
                emotion = ['쏠쏠정보',"흥미진진","공감백배","분석탁월","후속강추"]
                pdata = json.loads(json_data)
                react = pdata['contents']
                for reac in react:
                    uful = reac['reactions']
                for ful in uful:
                    type = ful['reactionType']
                    if type == 'useful':
                       emog[0] = ful['count']
                    elif type == 'wow':
                       emog[1] = ful['count']
                    elif type == 'touched':
                       emog[2] = ful['count']
                    elif type == 'analytical':
                       emog[3] = ful['count']
                    elif type == 'recommend':
                       emog[4] = ful['count']
                    else:
                       continue
                emoge = dict(zip(emotion,emog))

            elif soup_content.select_one('div.news_headline h4') != None:
                title = soup_content.select_one('div.news_headline h4').text.strip()
                content = soup_content.select_one('div#newsEndContents').text.replace('\n', '').strip()
                section = '스포츠'
                emoge={}
                emog = [0,0,0,0,0]
                emotion = ['좋아요',"슬퍼요","화나요","팬이에요","후속기사 원해요"]
                json_data = re.search(r'\(({.*})\)', res3.text).group(1)
                pdata = json.loads(json_data)
                react = pdata['contents']
                for reac in react:
                    uful = reac['reactions']
                    for ful in uful:
                        type = ful['reactionType']
                        if type == 'like':
                           emog[0] = ful['count']
                        elif type == 'sad':
                           emog[1] = ful['count']
                        elif type == 'angry':
                           emog[2] = ful['count']
                        elif type == 'fan':
                           emog[3] = ful['count']
                        elif type == 'want':
                           emog[4] = ful['count']
                        else:
                            continue
                    emoge = dict(zip(emotion,emog))

            elif soup_content.select_one('h2.end_tit') != None:
                title = soup_content.select_one('h2.end_tit').text.strip()
                content = soup_content.select_one('#articeBody').text.strip()
                section = '연예'
                emoge = {}
                emog = [0,0,0,0,0,0]
                emotion = ['좋아요','응원해요','축하해요','기대해요','놀랐어요','슬퍼요']
                json_data = re.search(r'\(({.*})\)', res2.text).group(1)
                pdata = json.loads(json_data)
                react = pdata['contents']
                for reac in react:
                    uful = reac['reactions']
                    for ful in uful:
                        type = ful['reactionType']
                        if type == 'like':
                           emog[0] = ful['count']
                        elif type == 'cheer':
                           emog[1] = ful['count']
                        elif type == 'congrats':
                           emog[2] = ful['count']
                        elif type == 'expect':
                           emog[3] = ful['count']
                        elif type == 'surprise':
                           emog[4] = ful['count']
                        elif type == 'sad':
                           emog[5] = (ful['count'])
                        else:
                           continue
                    emoge = dict(zip(emotion,emog))
            else:
                print('오류')
                print(url)
                
            writer.writerow([date,title,content,emoge,section])
            print(page)

        page += 1

    start_date += timedelta(days=1)

file.close()
print("크롤링 종료")

