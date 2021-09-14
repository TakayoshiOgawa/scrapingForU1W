import csv
import json
import requests
import sys
from bs4 import BeautifulSoup

# 引数から入力と出力を取得
args = sys.argv
url = args[1] #'https://unityroom.com/unity1weeks/53'
output = './u1w.csv' if len(args) <= 2 else args[2]

# URLからHTML構文を取得
soup = BeautifulSoup(requests.get(url).text, "html.parser")
# 特定のタグを対象に解析を開始
cards = soup.select('div.card-body', limit=None)
# print(f'cards:{len(cards)}')
# print(f'sample:{cards[0]}')

# 解析できたゲームは配列に格納
games = []
for card in cards:
    # ゲーム情報は連想配列に保持
    game = {}
    # タイトル、作者名、URL
    a = card.find_all('a')
    game['title'] = a[0].get_text()
    game['author'] = a[1].get_text()
    game['url'] = f"{url}{a[0]['href']}"
    # print(f"url:{game['url']}")

    # 閲覧数、評価数、コメント数
    span = card.select('span.ml-1', limit=None)
    game['fa_eye'] = span[0].get_text()
    game['fa_star'] = span[1].get_text()
    game['fa_comments'] = span[2].get_text()

    # ゲームを配列に追加
    games.append(game)

# 評価終了後のランキングによる重複を削除
games = list(map(json.loads, set(map(json.dumps, games))))
# print(f'games:{len(games)}')

# CSVに出力
with open(output, 'w') as f:
    # 連想配列のキーが見出し行になる
    writer = csv.DictWriter(f, ['title', 'author', 'fa_eye', 'fa_star', 'fa_comments', 'url'])
    writer.writeheader()
    for game in games:
        writer.writerow(game)