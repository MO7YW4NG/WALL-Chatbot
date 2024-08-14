from wallapp.model_manager import imgModel
import pathlib
import os

def generateContent(user_id, file):
    path = 'static/dress/'
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path,user_id + '.jpg')
    with open(path, 'wb') as fd:
        for chunk in file.iter_content():
            fd.write(chunk)
    picture = {
        'mime_type': 'image/jpg',
        'data': pathlib.Path(path).read_bytes()
    }
    prompt = '就使用者面試服裝圖片提供100字內建議，response in Traditional Chinese plain text, instead of markdown format.'
    response = imgModel.generate_content([picture,prompt])
    return response.text.strip()