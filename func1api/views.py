from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
#from linebot.models import MessageEvent, TextSendMessage
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, PostbackEvent
from module import func
from urllib.parse import parse_qsl
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    mtext = event.message.text
                    if mtext == '@辨別洗錢小知識':
                       func.sendMulti(event)
       
                    elif mtext == '@法律資訊':
                        func.sendImage(event)
                
                    elif mtext == '@重要資訊':
                        func.sendButton(event)
    
                    elif mtext == '@國內相關組織':
                        func.sendQuickreply(event)
                
                    elif mtext == '@國外相關組織':
                        func.sendButton2(event)
    
                    elif mtext == '@其他資訊':
                        func.sendCarousel(event)
    
            if isinstance(event, PostbackEvent):  #PostbackTemplateAction觸發此事件
                backdata = dict(parse_qsl(event.postback.data))  #取得data資料
                if backdata.get('action') == 'sell':
                    func.sendData_sell(event, backdata)

            else:            
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    
        return HttpResponse()

    else:
        return HttpResponseBadRequest()
