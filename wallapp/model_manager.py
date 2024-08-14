import google.generativeai as genai
import whisper
import os

api_key = os.getenv("GEMINI_API_KEY") 
genai.configure(api_key = api_key)

model = genai.GenerativeModel('gemini-1.5-flash',
                        system_instruction='你是大學資訊管理學系的入學面試官，說話簡短、嚴肅，用來審核欲申請大學的高中職學生，你總是提供既正確、專業又有用的經過深思熟慮地回答。以台灣繁體中文問答。',
                        generation_config= {
                            "temperature": 2.0,
                            })

imgModel = genai.GenerativeModel('gemini-1.5-pro',
                        system_instruction='你是大學入學面試官，兼具服裝專業。以台灣繁體中文問答。',
                        generation_config={
                            'max_output_tokens': 100,
                        })

voiceModel = whisper.load_model('small', download_root='./model/')