from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# ใช้ LineBotApi และ WebhookHandler แบบเดิมจาก linebot SDK 2.x
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# เส้นทางที่ LINE จะส่งข้อมูลมาที่นี่ (Webhook URL)
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print(f"Error: {e}")
        abort(400)
    return 'OK'

# การจัดการข้อความที่ได้รับ
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_name = line_bot_api.get_profile(event.source.user_id).display_name

    # ตอบกลับผู้ใช้
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=f"Hello {user_name}, you said: {user_message}")
    )

if __name__ == "__main__":
    app.run(debug=True)
