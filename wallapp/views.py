from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FileMessage, PostbackEvent, AudioMessage, ImageMessage

from urllib.parse import parse_qsl

from wallapp import qanda, ai_interview, ai_qus, aboutuni, nav, ai_dress

callbackUrl = "https://localhost:8080"
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt
def callback(request):
    if request.method is not 'POST':
        return HttpResponseBadRequest()
    
    signature = request.META['HTTP_X_LINE_SIGNATURE'] 
    body = request.body.decode('utf-8')
    
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()
    
    for event in events:
        user_id = event.source.user_id
        if isinstance(event, MessageEvent):
            # Check if message is a text
            if isinstance(event.message, TextMessage):
                arg = event.message.text
                # Check if user in interview session
                if ai_interview.isInSession(user_id):
                    result, response =  ai_interview.handle(user_id, arg)
                    if not result:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='結束面試'))
                    else:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=response))
                    continue
                # If not then
                if arg == '@面試':
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_interview.start_chat(user_id)))
                elif arg == '@面試數據':
                    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_interview.showStats(user_id)))
                elif arg == '@QA':
                    line_bot_api.reply_message(event.reply_token, qanda.getImgmap())
                elif arg == '@關於中原':
                    line_bot_api.reply_message(event.reply_token, aboutuni.getAboutButton())
                elif arg == '@介紹學院':
                    line_bot_api.reply_message(event.reply_token, aboutuni.getQuickreply())
                elif arg == '@學校地址':
                    line_bot_api.reply_message(event.reply_token, aboutuni.getUniPosition())
                elif arg == '@功能導覽':
                    line_bot_api.reply_message(event.reply_token, nav.nav())
                elif arg == '@備審':
                    line_bot_api.reply_message(event.reply_token, nav.pdf())
                elif arg == '@備審延伸功能介紹':
                    line_bot_api.reply_message(event.reply_token, nav.pdf_fun())
                elif arg == '@聯絡資管':
                    line_bot_api.reply_message(event.reply_token, nav.nav_cont())
                else:
                    # Check if keyword is in Q&A
                    hasAns, answer = qanda.getAns(arg)
                    if hasAns:
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=answer))
            # Check if message is a file
            elif isinstance(event.message, FileMessage):
                file = line_bot_api.get_message_content(event.message.id)
                line_bot_api.reply_message(event.reply_token, ai_qus.generateQuestion(user_id,file) if file.content_type == 'application/pdf' else TextSendMessage(text='請傳送PDF檔案'))
            # Check if message is an image
            elif isinstance(event.message, ImageMessage):
                file = line_bot_api.get_message_content(event.message.id)
                line_bot_api.reply_message(event.reply_token,  TextSendMessage(text=ai_dress.generateContent(user_id, file)))
            # Check if message is an audio
            elif isinstance(event.message, AudioMessage):
                if not ai_interview.isInSession(user_id):
                    continue
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_interview.handleVoice(user_id, line_bot_api.get_message_content(event.message.id))))
        elif isinstance(event, PostbackEvent):
            backdata = dict(parse_qsl(event.postback.data))
            goal = backdata['goal']
            if goal == 'ai_qus':
                if not ai_qus.isInSession(user_id):
                    continue
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=ai_qus.postback(backdata,user_id)))
            elif goal == 'about':
                line_bot_api.reply_message(event.reply_token, TextSendMessage(text=aboutuni.postback(backdata)))
    return HttpResponse()