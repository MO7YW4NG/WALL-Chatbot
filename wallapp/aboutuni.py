from linebot.models import TextSendMessage,LocationSendMessage,TemplateSendMessage,ButtonsTemplate,MessageTemplateAction,URITemplateAction,QuickReply,QuickReplyButton,PostbackAction
from wallapp.models import school

# 大學座標
def getUniPosition():
    try:
        return LocationSendMessage(
            title="中原大學",
            address="320桃園市中壢區中北路200號",
            latitude=24.9573505,
            longitude=121.240587
        )
    except:
        return TextSendMessage(text='發生錯誤!')

# 關於中原
def getAboutButton():
    try:
        message = TemplateSendMessage(
            alt_text='按鈕模板',
            template=ButtonsTemplate(
                thumbnail_image_url='https://www.cycu.edu.tw/wp-content/uploads/%E9%A6%96%E9%A0%81-3.jpg',
                title='關於中原',
                text='請選擇',
                actions=[
                    MessageTemplateAction(
                        label='介紹學院',
                        text='@介紹學院'
                    ),
                    MessageTemplateAction(
                        label='學校地址',
                        text='@學校地址'
                    ),
                    URITemplateAction(
                        label='學校官網',
                        uri='https://www.cycu.edu.tw/'
                    )
                ]
            )
        )
        return message
    except:
       return TextSendMessage(text='發生錯誤!')

# 介紹學院
def getQuickreply():
    try:
        message = TextSendMessage(
            text="請選擇想要了解的學院",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=PostbackAction(
                            label=school.name, data=f"goal=about&school={school.name}"
                        )
                    ) for school in school.objects.all()
                ]
            )
        )
        return message
    except:
        return TextSendMessage(text='傳送圖片發生錯誤!')

def postback(backdata):
    return school.objects.filter(name = backdata['school']).first().info