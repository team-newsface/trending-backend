import requests
from bs4 import BeautifulSoup
import time


headers = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}

i = int(0)
ranking = []


while True:
    _url = f'https://www.nate.com/?f=news'  # 네이트 실시간 이슈 키워드
    r1 = requests.get(_url, headers=headers)
    time.sleep(1)
    if r1.ok:
        soup = BeautifulSoup(r1.text, 'html.parser')
        keyword = soup.select_one(
            '#olLiveIssueKeyword > li:nth-child(1) > a > span.txt_rank')
        # print(keyword.text)
        url = f'https://news.nate.com/search?q={keyword.text.strip()}'
        r2 = requests.get(url, headers=headers)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        a_tags = soup2.select(
            '#search-option > form:nth-child(1) > fieldset > div.issue-kwd > span.kwd-list > a')
    print(time.strftime('%Y.%m.%d - %H:%M:%S'))
    for a_tag in a_tags:
        i += 1
        print(str(i)+". "+a_tag.text)
        ranking.append(a_tag.text)
    print("\n"+str(ranking))
    ranking = []
    i = 0
    print("\n")
    time.sleep(1)
