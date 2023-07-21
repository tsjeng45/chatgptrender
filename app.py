from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
line_bot_api = LineBotApi('7KCNLCVhBNzOKdSEpZz3Epn4JMaycwvmM5M+DkpEsbeHl6RK03w2hKL9QgZBCE3GmlDDuD2tHCR6lS99OFPr4HAPW/nP7/jylm1+KZu3HZU+aXDqoj9aQ+AGIejSOq3d9aBqdPXQKGjCvS1tLW0ojgdB04t89/1O/w1cDnyilFU=')
handler1 = WebhookHandler('46e5e29aad3071d691dba271dbca82a2')

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler1.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler1.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text1=event.message.text
    response = openai.ChatCompletion.create(
        messages=[
            {"role": "user", "content": text1}
        ],
        model="gpt-3.5-turbo",
        temperature = 0.5,
    )
    try:
        ret = response['choices'][0]['message']['content'].strip()
    except:
        ret = '發生錯誤！'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=ret))

if __name__ == '__main__':
    app.run()