import json
import boto3
import urllib
import re
import os
import random
import time
import mysql.connector as mydb

ARTIST_ID = 1 # DBに事前に登録するアーティストのID
 
class CotohaApi():
    def __init__(self):
        self.COTOHA_ACCESS_INFO = {
            "grantType": "client_credentials",
            "clientId": os.environ['COTOHA_CLIENTID'],
            "clientSecret": os.environ['COTOHA_CLIENTSECRET']
        }
        self.ACCESS_TOKEN_PUBLISH_URL = 'https://api.ce-cotoha.com/v1/oauth/accesstokens'
        self.BASE_URL = 'https://api.ce-cotoha.com/api/dev/'

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
            host = os.environ['DB_HOST'],
            port = os.environ['DB_PORT'],
            user = os.environ['DB_USER'],
            password = os.environ['DB_PASS'],
            database = os.environ['DB_NAME'],
            charset='utf8'
        )

        self.conn.ping(reconnect=True)
        self.cur = self.conn.cursor()
        
class Search():
    def __init__(self, message_text):
        self.SEARCH_SCOPE = [0.01, 0.1, 0.3] # 検索するスコアの幅 SCORE±SEARCH_SCOPEの範囲でリストの順に検索
        self.message_text = message_text

    def execute(self):
        
        cotoha_api= CotohaApi()
        sentiment_result = cotoha_api.sentiment_analysis(self.message_text)['result']
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
            reply_message = "{} [{}]".format(phrase_chosen[0], phrase_chosen[1])
        else:
            reply_message = 'いい歌詞が見つからなかった。'
        
        db.conn.close()
        
        return reply_message
        
 
def lambda_handler(event, context):

    url = "https://api.line.me/v2/bot/message/reply"
    method = "POST"
    headers = {
        'Authorization': 'Bearer ' + os.environ['LINE_TOKEN'],
        'Content-Type': 'application/json'
    }

    reply_token = event['events'][0]['replyToken']
    message_text = event['events'][0]['message']['text']
    
    searcher = Search(message_text)
    reply_message = searcher.execute()
    
    message = [
        {
            "type": "text",
            "text": reply_message
        }
    ]

    params = {
        "replyToken": reply_token,
        "messages": message
    }
    request = urllib.request.Request(url, json.dumps(params).encode("utf-8"), method=method, headers=headers)
    with urllib.request.urlopen(request) as res:
        body = res.read()
    return 0
