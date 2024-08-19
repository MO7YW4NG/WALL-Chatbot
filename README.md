<div align="center">
  <img width="256px" height="256px" src="https://i.imgur.com/IZsbJdq.jpg" />
  <h1>同學，瓦力 WALL-Chatbot</h1>
  <p>中原資管備審及面試輔助 Line Bot</p>
  <p>AI-Powered Line Bot for University Applicant</p>
</div>

## 使用技術
* Django
* Line Bot
* Google Gemini
* OpenAI Whisper

## 功能導覽

### 認識中原
  
1. 學校官網
2. 學院介紹
3. 學校地址

### 模擬資管面試

> **面試過程**

```mermaid
flowchart TD;

自我介紹 --> 詢問科系相關延伸問題 --> 詢問資訊科技相關英文時事問題 --> 總結並評分;
```

> **技術流程**

```mermaid
flowchart LR;

A[用戶傳送文字/語音訊息] --> |Whisper STT|B[GeminiAPI];
B -->|根據回覆與階段生成問題| A;
```

### 備審延伸題目

```mermaid
flowchart LR;
    傳送備審PDF --> 擷取文字 --> GeminiAPI --> 生成模擬問題;
```
### 申請常見問題
如自傳如何撰寫、學習歷程自述方向等。

### 面試服裝建議

```mermaid
flowchart LR;
    傳送個人服裝圖片 --> GeminiAPI --> 給予面試穿搭建議;
```



