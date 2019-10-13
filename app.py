# coding: utf-8
import pytz
from flask import Flask
from flask import request
from lineworks import *
import os
import bloom

# LINE WORKS AIP情報
API_ID = os.environ['APIID']
PRIVATE_KEY = os.environ['PRIVATEKEY']
SERVER_API_CONSUMER_KEY = os.environ['CONSUMERKEY']
SERVER_ID = os.environ['SERVERID']
BOT_NO = os.environ['BOTNO']
ROOM_ID = None
DOMAIN_ID = os.environ['DOMAINID']

conference_room_small = list()
conference_room_big = list()

app = Flask(__name__)

@app.route('/')
def index():
    return "Start.", 200


@app.route('/callback', methods=['POST'])
def callback():
    header = request.headers
    body = request.json
    if body["type"] == "message":
        talkbot = TalkBotApi(
            api_id=API_ID,
            private_key=PRIVATE_KEY,
            server_api_consumer_key=SERVER_API_CONSUMER_KEY,
            server_id=SERVER_ID,
            bot_no=BOT_NO,
            account_id=body["source"]["accountId"],
            room_id=ROOM_ID,
            domain_id=DOMAIN_ID
        )

        condition = body.get('content').get('text') if body.get('content').get('text') else datetime.datetime.now(pytz.timezone('Asia/Tokyo')).strftime(
                                 "%Y/%m/%d")
        session = bloom.fetch_login()
        reservations = bloom.fetch_reservations_tokyo(session, '110', condition)
        message = bloom.create_message("会議室大\n", reservations)
        talkbot.send_text_message(send_text=message)
        
        reservations = bloom.fetch_reservations_tokyo(session, '111', condition)
        message = bloom.create_message("会議室小\n", reservations)
        talkbot.send_text_message(send_text=message)
        return "OK."


if __name__ == '__main__':
    app.run(debug=True)
