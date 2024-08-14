import re
import json
from typing import Union
from wallapp.models import history
from wallapp.model_manager import model, voiceModel
import traceback
import os

ans_pattern = re.compile(r'<ans>(.*?)</ans>', re.S)
resp_pattern = re.compile(r'role: "user"[\s\S]*?text: "(.*?)"', re.S)

counter = dict()
session = dict()

# Check if user is in session
def isInSession(user_id: str) -> bool:
    return user_id in session

# Start interview session
def start_chat(user_id: str):
    message = "出現錯誤，請再嘗試一遍..."
    chatSession = model.start_chat(history=[])
    try:
        response = chatSession.send_message("請向打開程式的學生要求簡短200字自我介紹，並告知使用者可以輸入quit中途退出面試。")
        message = response.text.strip()
    except Exception as e:
        print("{}".format(e))
        pass
    finally:
        session[user_id] = chatSession
        counter[user_id] = 0
    return message

# Interview audio to text handler
def handleVoice(user_id: str, audio):
    try:
        path = 'static/voice/'
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path,user_id + '.aac')
        with open(path, 'wb') as fd:
            for chunk in audio.iter_content():
                fd.write(chunk)
        result = voiceModel.transcribe(path)
        text = result['text']
        return handle(user_id,text)[1]
    except Exception:
        traceback.print_exc()

# Interview handler
def handle(user_id: str, text: str) -> Union[bool,str]:
    # history.objects.all().delete()
    if "quit" in text:
        counter.pop(user_id, None)
        session.pop(user_id, None)
        return False, None
    try:
        chat = session[user_id]
        id = counter[user_id]
        
        instructions = {
            0: '根據這段自我介紹，延伸詢問相關領域的一個問題。',
            1: '根據這段回答，簡短總結一下你作為面試官的想法。並詢問一個資訊科技相關時事問題，務必要求面試者用「英文」回答。',
            2: '''若非以英語回答，予以指責。
            根據此段「英文」回答與先前的回答，給出面試中「具體」、包含「缺點」的建議，最後告知面試者面試結束，
            並以 0.0 - 10.0 分打一個客觀、中立的面試總結分數。
            依JSON格式回傳 {"score": "<分數>", "message": "<文字>"}
            '''
        }
        
        instruction = instructions.get(id, "未知的指令")
        
        
        generation_config = {"response_mime_type": "application/json"} if id == 2 else {}
        response = chat.send_message(f'<ans>{text}</ans> \n以上是學生的回覆，{instruction}', generation_config=generation_config)
        message = response.text.strip()

        if id == 2:
            # print(message)
            ans = json.loads(message)
            score = float(ans['score'])
            message =  f"{ans['message']}\n你的面試評分為：{score} / 10 分"
            handleHistory(str(chat.history), score, ans['message'],user_id)
            counter.pop(user_id, None)
            session.pop(user_id, None)

    except json.JSONDecodeError:
        message = "JSON 解碼錯誤，請再嘗試一遍..."
        traceback.print_exc()
    except KeyError:
        message = "主鍵錯誤，請再嘗試一遍..."
        traceback.print_exc()
    except Exception:
        message = "出現錯誤，請再嘗試一遍..."
        traceback.print_exc()
    finally:
        if user_id in counter:
            counter[user_id] += 1

    return True, message

# Show avg interview score
def showStats(user_id):
    allHistories =  history.objects.all()
    if allHistories.count() == 0:
        return f'尚無面試資料！'
    histories = history.objects.filter(user=user_id).all()
    userAvgScore = sum([history.score for history in histories]) / len(histories)
    avgScore = sum([history.score for history in allHistories]) / allHistories.count()
    return f'你的平均面試分數：{userAvgScore} / 10\n總體平均面試分數：{avgScore} / 10'

# Log interview history
def handleHistory(chatHistory: str, score: float, sum: str, user_id: str):
    answers = [x.replace('\\n', '').strip() for x in ans_pattern.findall(chatHistory)]
    responses = [x.replace('\\n', '').strip() for x in resp_pattern.findall(chatHistory)]
    unit = history.objects.create(user=user_id,ans1=answers[0],q1=responses[1],ans2=answers[1],q2=responses[2],ans3=answers[2],sum=sum,score=score)
    unit.save()