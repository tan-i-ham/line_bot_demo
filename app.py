from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('rTl/PcLy6oXYIxl2V30E+930qtUqDz59DCJ4uBAlYcx7p35JFCe/vUzTNXIgtPoEBJPABhj7/9HoEq/GRrP2ipVTOnlGmOSQaiUQ361nQObTO96ALNVcZr+8TlrQy8vzYgxTypr4Swkm69/dbjdcswdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('6656e2a268d134c41c47d0ed5bd5597d')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     # message = TextSendMessage(text=event.message.text)
#     # line_bot_api.reply_message(
#     #     event.reply_token,
#     #     message)
#     message = TemplateSendMessage(
#         alt_text='Buttons template',
#         template=ButtonsTemplate(
#             thumbnail_image_url='https://example.com/image.jpg',
#             title='Who is Yi-Han Chen?',
#             text='Student from NTUST, Taiwan . Familiar with Python and Java',
#             actions=[
#                 PostbackTemplateAction(
#                     label='postback',
#                     text="you just sned "+k,
#                     data='action=buy&itemid=1'
#                 ),
#                 MessageTemplateAction(
#                     label='What is my side project recently?',
#                     text='side project'
#                 ),
#                 URITemplateAction(
#                     label='My Linkedin',
#                     uri='https://www.linkedin.com/in/hannah-chen-326918101/'
#                 )
#             ]
#         )
#     )
#     line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_text = event.message.text

    if user_text == 'profile':
        # message = TextSendMessage(text=event.message.text)
        message = TextSendMessage(text=user_text)
        
        line_bot_api.reply_message(
            event.reply_token,
            message)
    elif user_text == 'buttons':
        buttons_template = ButtonsTemplate(
            title='My buttons sample', text='Hello, my buttons', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

# if __name__ == "__main__":
#     arg_parser = ArgumentParser(
#         usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
#     )
#     arg_parser.add_argument('-p', '--port', type=int, default=5000, help='port')
#     arg_parser.add_argument('-d', '--debug', default=False, help='debug')
#     options = arg_parser.parse_args()

#     # create tmp dir for download content
#     # make_static_tmp_dir()

#     app.run(debug=options.debug, port=options.port)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

