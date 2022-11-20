import requests
import time
from bs4 import BeautifulSoup
from typing import Union
import asyncio
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

i = int(0)
app = FastAPI()

headers = {
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'
}

ranking = []
# ranking = ['정진상 구속에 무검유죄', '전략폭격기 B-1B 재전개', '스페인 총리 부인에', '붉은 악마 거리응원',
#            '15 KG↑ 한해', '시진핑 오해 줄이자', '29층 징계 위기', '빈 살만', '김예림', '김래원 거짓말 스타일']


async def ranking_cr():
    _url = f'https://www.nate.com/?f=news'  # 네이트 실시간 이슈 키워드
    r1 = requests.get(_url, headers=headers)
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
    global i
    global ranking
    print(time.strftime('%Y.%m.%d - %H:%M:%S'))
    ranking = []
    for a_tag in a_tags:
        i += 1
        print(str(i)+". "+a_tag.text)
        ranking.append(a_tag.text)
    print("\n"+str(ranking))
    i = 0
    print("\n")


@app.get("/")
async def read_root():
    await ranking_cr()
    return {"rankings": ranking}


@app.get("/rankings/{rankings_num}")
async def read_item(rankings_num: int):
    await ranking_cr()
    return {"rankings_num": rankings_num, "내용": ranking[int(rankings_num)]}


# while True:
#     ranking_cr()
