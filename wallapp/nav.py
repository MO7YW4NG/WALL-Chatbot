import wallapp.views as v
from linebot.models import TextSendMessage, TemplateSendMessage, MessageTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn

def nav():
    message = TemplateSendMessage(
        alt_text="@功能導覽",
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqyl5bX7kJUlxdVRw-fAl0KdZrC7PlMyB93Q&s',
                    title = '認識中原',
                    text = '關於中原的大小事',
                    actions=[
                        MessageTemplateAction(
                            label='點選進入',
                            text='@關於中原'
                        ),
                        URITemplateAction(
                            label='學校官網',
                            uri='https://www.cycu.edu.tw/'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://s.yimg.com/ny/api/res/1.2/o2z6nZQi5RBBoDtmMcOi9A--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTQ4MA--/https://media.zenfs.com/ko/taiwanhot.net.tw/da05173e0b62aacecd38dd5cb8a64b52',
                    title = '模擬資管面試',
                    text = '線上進行模擬面試',
                    actions=[
                        MessageTemplateAction(
                            label='點選進入',
                            text='@面試'
                        ),
                        MessageTemplateAction(
                            label='查看模擬面試紀錄',
                            text='@面試數據'
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.cycu.edu.tw/wp-content/uploads/01-%E4%B8%AD%E5%8E%9F%E5%A4%A7%E5%AD%B8%E8%BE%A6%E5%AD%B8%E7%B8%BE%E5%84%AA%E5%A4%A7%E8%BA%8D%E9%80%B2%EF%BC%8C%E6%A0%A1%E9%95%B7%E4%BA%92%E8%A9%95%E7%8D%B2%E4%BD%B3%E7%B8%BE%EF%BC%81.jpg',
                    title = '備審延伸題目',
                    text = '上傳備審，進行面試題目模擬',
                    actions=[
                        MessageTemplateAction(
                            label='點擊開始',
                            text='@備審'
                        ),
                        MessageTemplateAction(
                            label='認識功能',
                            text='@備審延伸功能介紹'
                        ),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://www.cycu.edu.tw/wp-content/uploads/c1e7458b-a2bd-497c-a112-7ededad3c0ee.jpg',
                    title = '面試問題諮詢',
                    text = '常見問題Q&A',
                    actions=[
                        MessageTemplateAction(
                            label='點擊開始',
                            text='@QA'
                        ),
                        MessageTemplateAction(
                            label='聯絡資管',
                            text='@聯絡資管'
                        ),
                    ]
                ),
            ]
        )
    )
    return message

def pdf():
    return TextSendMessage(text='傳送PDF檔備審開始模擬')

def pdf_fun():
    return TextSendMessage(text='面試老師看完你的備審資料後，可能想要詢問的延伸功能，傳送PDF備審開始模擬')

def nav_cont():
    return TextSendMessage(text='中原資管系辦：\nTel：886-3-265-5402 (總機)\nTel：886-3-265-5403(碩士專、實習)\nTel：886-3-265-5420(設備)\nTel：886-3-265-5401(大學課程)')