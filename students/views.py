from django.shortcuts import render
from studentsapp.models import student
from django.http import HttpResponse

import logging
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime
from flask import Flask
from flask import request
from flask import abort
from linebot.models import *
logger = logging.getLogger("django")

"""
line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
parser  = WebhookParser(settings.LINE_CHANNEL_SECRET)
"""
app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('W3cJZwxPee8Xg74vRZ0KvQ7Sy0sjPpzlCnuhE59pXLUJrBUghurpxP7K9uqEK/cXYZyIgD6B8J926PB2Bfc73pT1tscfORX8koAxTWJZesgAF9LdzgKrlRnURH2m32Mm96s81v//uGWYdEE7cfZ2uwdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('02e59494ae3f01a49a87f538ff81ffb0')

line_bot_api.push_message('U7638b973e5e09749f86ecf44256f64d4', TextSendMessage(text='你可以開始了'))

@csrf_exempt
@require_POST
def callback(request):
    signature = request.META['HTTP_X_Line_Signature']
    body = request.body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        messages = ( "Invalid signature. Please check your channel access token/channel secret.")
        HttpResponseForbidden()

    return HttpResponse('OK',status=200)


@handler.add(event=MessageEvent, message=TextMessage)
def handl_message(event: MessageEvent):
           line_bot_api.reply_message(
            reply_token=event.reply_token,
            messages=TextSendMessage(text=event.message.text),
        )
