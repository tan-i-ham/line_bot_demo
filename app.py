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
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent, 
    RichMenu, RichMenuArea, RichMenuBound
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
        if isinstance(event.source, SourceUser):
            profile = line_bot_api.get_profile(event.source.user_id)
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(
                        text='Display name: ' + profile.display_name
                    ),
                    TextSendMessage(
                        text='Status message: ' + profile.status_message
                    )
                ]
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't use profile API without user ID"))
        

    elif user_text == 'buttons':
        buttons_template = ButtonsTemplate(
            thumbnailImageUrl='https://drive.google.com/file/d/0B5-xPoQ36Sb7V3czWHF1QUY5UTQ/view?usp=sharing',
            title='Yi-Han Chen', 
            text='Student from NTUST', 
            actions=[
                URITemplateAction(
                    label='My Linkedin', uri='https://www.linkedin.com/in/hannah-chen-326918101/'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='side project', text='side project')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif user_text == 'side project':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='4/18 event', title='MSP', actions=[
                URITemplateAction(
                    label='Github', uri='https://github.com/tp6hannah/scraper_bing_speech_api'),
                MessageTemplateAction(label='Scraper', text='udn news'),
                MessageTemplateAction(label='people?', text='25')
            ]),
            CarouselColumn(text='Brand promote', title='Drinkbar', actions=[
                URITemplateAction(
                    label='GIF Previews', uri='https://giphy.com/gifs/drinkbar-1lvW7lrbIA3yq4gQGx'),
                MessageTemplateAction(label='Function 1', text='Vote'),
                MessageTemplateAction(label='Function 2', text='Drink Picker')                
            ]),
            # CarouselColumn(text='hoge2', title='fuga2', actions=[
            #     PostbackTemplateAction(
            #         label='ping with text', data='ping',
            #         text='ping'),
            #     MessageTemplateAction(label='Translate Rice', text='米')
            # ]),
        ])

        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    else:
        rich_menu_to_create = RichMenu(
                            size=RichMenuBound(
                                width=2500,
                                height=1686
                            ),
                            selected= False,
                            name="nice richmenu",
                            chatBarText="touch me",
                            areas=[
                                RichMenuArea(
                                    RichMenuBound(
                                        x=0,
                                        y=0,
                                        width=2500,
                                        height=1686
                                    ),
                                    URITemplateAction(
                                        uri='line://nv/location'
                                    )
                                )
                            ]
                        )
        rich_menu_id = line_bot_api.create_rich_menu(data=rich_menu_to_create)
        print(rich_menu_id)
        user_text += str(rich_menu_id)
        
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=user_text))


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

