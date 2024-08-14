from linebot.models import MessageImagemapAction,ImagemapArea,ImagemapSendMessage,BaseSize,TextSendMessage
from wallapp.models import qanda
import wallapp.views as v

def getAns(question:str) -> (bool | str):
    objs = qanda.objects.filter(question__icontains=question)
    return objs.count() != 0, objs.first().answer.replace('\\n','\n') if objs.count() != 0 else None
    
def getImgmap():
    try:
        image_url = v.callbackUrl+"/static/qanda"
        imgwidth = 1040
        imgheight = 1946
        block_width = imgwidth
        block_height = imgheight // 9

        actions = []
        for i, entry in enumerate(qanda.objects.all()):
            actions.append(MessageImagemapAction(
                text=entry.question,
                area=ImagemapArea(
                    x=0,
                    y=i * block_height,
                    width=block_width,
                    height=block_height,
                )
            ))
        message = ImagemapSendMessage(
            base_url=image_url,
            alt_text='圖片地圖',
            base_size=BaseSize(height=imgheight, width=imgwidth),
            actions=actions
        )
        return message
    except Exception as e:
        return TextSendMessage(text='發生錯誤: {}'.format(e))