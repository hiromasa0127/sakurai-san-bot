# -*- coding: utf-8 -*-

import random, requests, json, sys, time
import urllib.request
import mysql.connector as mydb
import pandas as pd

from bs4 import BeautifulSoup

ARTIST_ID = 1 # DBに事前に登録するアーティストのID
AGENT_NAME = '桜井さん' # 答えてくるエージェントの名前

class CotohaApi():
    def __init__(self):
        self.COTOHA_ACCESS_INFO = {
            "grantType": "client_credentials",
            "clientId": "<ご自身のClient ID>",
            "clientSecret": "<ご自身のClient Secret>"
        }
        self.ACCESS_TOKEN_PUBLISH_URL = '<ご自身のAccess Token Publish URL>'
        self.BASE_URL = '<ご自身のAPI Base URL>'

        self.ACCESS_TOKEN = self.get_access_token()

    def get_access_token(self):
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        access_data = json.dumps(self.COTOHA_ACCESS_INFO).encode()
        request_data = urllib.request.Request(self.ACCESS_TOKEN_PUBLISH_URL, access_data, headers)
        token_body = urllib.request.urlopen(request_data)
        token_body = json.loads(token_body.read())
        self.access_token = token_body["access_token"]
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'Authorization': 'Bearer {}'.format(self.access_token)
        }

    def sentiment_analysis(self, text):
        request_body = {
            'sentence': text
        }
        url = self.BASE_URL + 'nlp/v1/sentiment'
        text_data = json.dumps(request_body).encode()
        request_data = urllib.request.Request(url, text_data, headers=self.headers, method='POST')
        sentiment_result = urllib.request.urlopen(request_data)
        sentiment_result = json.loads(sentiment_result.read())
        return sentiment_result

    def convert_sentiment(self, sentiment_in_word):
        if sentiment_in_word == 'Positive':
            return 1
        elif sentiment_in_word == 'Neutral':
            return 0
        elif sentiment_in_word == 'Negative':
            return -1

class DBHandler():
    def __init__(self):
        self.conn = mydb.connect(
            host = '<DBのホスト名>',
            port = '<DBのポート番号>',
            user = '<DBのユーザ名>',
            password = '<DBのパスワード>',
            database = '<DB名>',
            charset='utf8'
        )

        self.conn.ping(reconnect=True)
        self.cur = self.conn.cursor()

class Learn():
    def __init__(self):
        self.FILE_NAME = 'list.csv'
        self.ARTIST_NUMBER = '684' # 歌ネットのアーティストNo.（事前に調査）
        self.MAX_PAGE = 2 # 歌ネットのアーティスト名検索時の検索結果のページ数（事前に調査）

    def gather_lyric(self):
        #スクレイピングしたデータを入れる表を作成
        list_df = pd.DataFrame(columns=['曲名', '歌詞'])

        for page in range(1, self.MAX_PAGE + 1):
            #曲ページ先頭アドレス
            base_url = 'https://www.uta-net.com'

            #歌詞一覧ページ
            url = 'https://www.uta-net.com/artist/' + self.ARTIST_NUMBER + '/0/' + str(page) + '/'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
            links = soup.find_all('td', class_='sp-w-100 pt-0 pt-lg-2')

            for link in links:
                a = base_url + (link.a.get('href'))

                #歌詞詳細ページ
                response = requests.get(a)
                soup = BeautifulSoup(response.text, 'lxml')
                title = soup.find('h2').text
                print(title)
                song_lyrics = soup.find('div', itemprop='text')
                
                for lyric in song_lyrics.find_all("br"):
                    lyric.replace_with('\n')
                song_lyric = song_lyrics.text

                #サーバーに負荷を与えないため1秒待機
                time.sleep(1)

                #取得した歌詞を表に追加
                tmp_se = pd.DataFrame([title, song_lyric], index=list_df.columns).T
                list_df = list_df.append(tmp_se)

        #csv保存
        list_df.to_csv(self.FILE_NAME, mode = 'a', encoding='utf8')

    def add_lyric(self):
        db = DBHandler()
        df_file = pd.read_csv(self.FILE_NAME, encoding='utf8')
        song_titles = df_file['曲名'].tolist()
        song_lyrics = df_file['歌詞'].tolist()
        
        # 注意：曲数が多いとCOTOHAの1日に実行できるAPIの上限にひっかかかる（1日100曲程度が目安）
        for i in range(len(song_titles)):

            # タイトルの追加
            title = song_titles[i]

            print("Info: Saving {}...".format(title), end="")
            db.cur.execute(
                """
                insert into title (title, artist_id)
                values (%s, %s);
                """,
                (title, ARTIST_ID)
            )
            db.conn.commit()
            db.cur.execute(
                """
                select title_id from title
                where title= %s
                and artist_id = %s;
                """,
                (title, ARTIST_ID)
            )
            title_id = db.cur.fetchall()[-1][0]

            # 歌詞のフレーズの感情分析結果を登録
            # 二回改行が出現した場合をフレーズ区切りにする
            lyric = song_lyrics[i]
            lyric_phrases = lyric.split('\n\n')
            lyric_phrases = [lyric.replace('\u3000', ' ').replace('\n', ' ') for lyric in lyric_phrases]
            
            cotoha_api= CotohaApi()
            for phrase in lyric_phrases:
                sentiment_result = cotoha_api.sentiment_analysis(phrase)['result']
                sentiment = cotoha_api.convert_sentiment(sentiment_result['sentiment'])
                score = sentiment_result['score']
                
                db.cur.execute(
                    """
                    insert into lyric (title_id, score, sentiment, phrase)
                    values (%s, %s, %s, %s);
                    """,
                    (title_id, score, sentiment, phrase)
                )
                db.conn.commit()

            print("Done")
                
        db.conn.close()
        if db.conn.is_connected() == False:
            print("Info: DB Disonnected")

    def execute(self):
        print("Info: 歌詞を収集中...")
        #self.gather_lyric()
        print("Info: 歌詞をDBに追加中...")
        self.add_lyric()

class Search():
    def __init__(self):
        self.SEARCH_SCOPE = [0.01, 0.1, 0.3] # 検索するスコアの幅 SCORE±SEARCH_SCOPEの範囲でリストの順に検索

    def execute(self):
        print("あなた：", end="")
        input_data = input()
        print("{}：".format(AGENT_NAME), end="")
        
        cotoha_api= CotohaApi()
        sentiment_result = cotoha_api.sentiment_analysis(input_data)['result']
        sentiment = cotoha_api.convert_sentiment(sentiment_result['sentiment'])
        score = sentiment_result['score']
        
        db = DBHandler()

        find_flag = 0
        for scope in self.SEARCH_SCOPE:

            # 最低1件あることを確認
            db.cur.execute(
                """
                select count(phrase_id) from lyric
                join title on lyric.title_id = title.title_id
                where sentiment = %s
                and score between %s and %s
                and artist_id = %s;
                """,
                (sentiment, score-scope, score+scope, ARTIST_ID)
            )
            hit_num = db.cur.fetchall()[-1][0]
            if hit_num > 0:
                find_flag = 1
                break
        
        if find_flag == 1:
            db.cur.execute(
                """
                select phrase,title from lyric
                join title on lyric.title_id = title.title_id
                where sentiment = %s
                and score between %s and %s
                and artist_id = %s;
                """,
                (sentiment, score-scope, score+scope, ARTIST_ID)
            )
            search_result = db.cur.fetchall()
            phrase_chosen = random.choice(search_result)
            print("{} [{}]".format(phrase_chosen[0], phrase_chosen[1]))
        else:
            print("いい歌詞が見つからなかった。")
        
        db.conn.close()
        

if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        process = args[1] # コマンドライン引数　learn: DBに歌詞情報を登録、search: DBから似た感情のフレーズを抽出
        if process == 'search':
            searcher = Search()
            searcher.execute()
        elif process == 'learn':
            learner = Learn()
            learner.execute()
        else:
            print("Error: コマンドライン引数を1つ指定 [learn/search]")
    else:
        print("Error: コマンドライン引数を1つ指定 [learn/search]")
