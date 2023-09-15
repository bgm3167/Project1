import requests
from bs4 import BeautifulSoup
import csv

file=open("outputs.csv",mode="w",encoding="utf-8",newline="")
writer=csv.writer(file)

for j in range(2, 5):
    url = 'https://finance.naver.com/item/sise_day.naver?code=005930&page={0}'.format(j)
    headers = {
    'authority': 'finance.naver.com',
    'method': 'GET',
    'path': '/item/sise_day.naver?code=005930&page=2',
    'scheme': 'https',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Cookie': 'NNB=RNCMCBGBDTWGI; nx_ssl=2; nid_inf=-1587947437; NID_JKL=VHwCjT9lNTEMf7IJbAlKBg3fyqMh23mUXYP49EhJ3l8=; NID_AUT=Dis8qKf/v1bu8uCv4yShLFA6+GOX58KeG3ApevTd1xrA+NXYKDb9oqD/Hq07j3kX; page_uid=idnxHsprvmsssDc3R7wssssstih-333939; naver_stock_codeList=005930%7C252670%7C; NID_SES=AAABqIO0blw4uXvzFWZ8M9CtMn2zwo/ICY+5K+x2hELmIszEztC7lnvsJYzRfkPSug+X32y9oJgvWpMyOQ+liqPBCR58BoEWKAu9VWKP7IGXkQxycDpR7F5HpH2tZnb71mtENCtG5+BD4LqOZ+7L282ZerOpI/52mLppVCxZPx5Lk3+iGkZVkUS2EpUWuJnYlTw828Qbn/hBRykivX2ugM/7FrKgHCtROb5jgfMCHGmQAwl6nQVbomZIbj6m0rQdEn0zLbdIdyVgUoaZmHS1RBZ5/20MQHvpXagf7d01yupR7UxGMS2CvKvWDSgDkl49Pd1aRaKSjghnoBjZtxynXQ/mLOU6kBG0J6ZxwuozyeM2a69OU0xYzx+pcqm3gHOlGya2SXtwegTlGwn5E0Pecqk7HbBMPF/YLvZV35YLwAS+F7UcOWu254Z6yo7R7QhTHzYKBnpy90W05nV0zRtCmBdRlz1oZc9xSgDgpOhSur8XEMTidF7dhK8v3AdzmERP1Hz6H50w04sGIPQvkuRRzuaHCO8ZwjMWTrLfbjB6Ift5v5nZ1Vdx250gaQpa92V3P2MqEQ==; JSESSIONID=9BEFB9C540E1C325E2C897BE3D2EF216',
    'Referer': 'https://finance.naver.com/item/sise_day.naver?code=005930&page=1',
    'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
     }

    sams = requests.get(url, headers=headers)
    soup = BeautifulSoup(sams.text, 'html.parser')

    i = 3

    while i != 16:
        datas = soup.select('table.type2 > tr:nth-child({0})'.format(i))
        for data in datas:
            date = data.select_one('td:nth-child(1)')
            price = data.select_one('td:nth-child(2)')

            if date is not None and price is not None:
                dat = date.text.strip()
                pric = price.text.strip()
                if dat.startswith("2023.08"):
                   writer.writerow([dat, pric])
            else:
                continue
        i += 1  

file.close()





