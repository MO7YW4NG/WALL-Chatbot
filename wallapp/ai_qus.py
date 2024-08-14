from linebot.models import BubbleContainer, BoxComponent, TextComponent, ButtonComponent, FlexSendMessage, PostbackAction

from wallapp.model_manager import model

import pdfplumber as pdfile
import os
import json

session = dict()

# Check user is in session
def isInSession(user_id) -> bool:
    return user_id in session

# Generate questions according to resume
def generateQuestion(user_id,pdfContent):
    if isInSession(user_id):
        del session[user_id]

    path = f"static/"
    path = os.path.join(path,f'{user_id}.pdf')
    
    with open(path, 'wb') as fd:
        for chunk in pdfContent.iter_content():
            fd.write(chunk)
    
    tot_text = ''

    # Extract text from PDF
    with pdfile.open(path) as pdf:
        total_pages = len(pdf.pages)
        start_page = max(0, total_pages -4)
        for i, page in enumerate(pdf.pages[start_page:], start=start_page + 1):
            txt = page.extract_text()
            tot_text += (txt)
            
    prompt = '''
        根據這位高中生的書面審查資料，精選後限制列六個重點關鍵字與問題。
        依以下JSON格式回覆 
        {
            "response":
                [
                    {
                        "label": "<keyword1>",
                        "text": "<question2>"
                    },
                    {
                        "label": "<keyword2>",
                        "text": "<question2>"
                    }
                ]
        }
    '''
    response = model.generate_content([tot_text,prompt],generation_config={"response_mime_type":"application/json"})
    message = response.text.strip()

    result = dict()
    data = json.loads(message)
    
    for entry in data['response']:
        result[entry['label']] = entry['text']
    
    # Tag user with result
    session[user_id] = result

    bubble = BubbleContainer(
        direction = 'ltr',
        header=BoxComponent(
            layout = 'vertical',
            contents=[
                TextComponent(text='備審模擬問題', weight='bold', size='xl'),
            ]
        ),
        body=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text='點選關鍵字查看問題', size='md'),
                BoxComponent(
                    layout='vertical',
                    contents=[
                        ButtonComponent(
                            style='secondary',
                            height='sm',
                            margin='md',
                            action=PostbackAction(label=label,data=f"goal=ai_qus&question={i}"),
                        ) for i, (label,_) in enumerate(result.items())
                    ]
                ),
            ],
        ),
        footer=BoxComponent(
            layout='vertical',
            contents=[
                TextComponent(text='同學，瓦力',color='#888888', size='sm', align='center'),
            ]
        ),
    )
    return FlexSendMessage(alt_text="備審問題彈性配置", contents=bubble)        

def postback(backdata,user_id):
    result = session[user_id]
    return result[list(result.keys())[int(backdata['question'])]]