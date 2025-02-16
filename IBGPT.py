import os
import openai
import streamlit as st
import time
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Assistant ID (Playground에서 사용한 Assistant ID 확인 필요)
assistant_id = "asst_RnCrKj7G4US5N9EkRwx6UiFC"

# OpenAI 클라이언트 설정
client = OpenAI(api_key=api_key)

# Streamlit UI 설정
st.set_page_config(page_title="IB GPT Chatbot", page_icon="🎓")

# 세션 상태 초기화 (대화 기록 및 Thread ID 유지)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# API 연결 및 Assistant 실행 함수
def run_assistant(user_input):
    if st.session_state.thread_id is None:
        # 새로운 Thread 생성 (Playground와 동일한 Assistant ID 사용)
        thread = client.beta.threads.create()
        st.session_state.thread_id = thread.id

    # 사용자의 메시지를 Assistant에게 전달
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=user_input
    )

    # Assistant 실행
    run = client.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant_id
    )

    # 실행이 완료될 때까지 대기
    while run.status in ["queued", "in_progress"]:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id,
            run_id=run.id
        )

    # Assistant의 응답 받기
    messages = client.beta.threads.messages.list(
        thread_id=st.session_state.thread_id
    )

    # 최신 응답 가져오기
    assistant_reply = messages.data[0].content[0].text.value
    return assistant_reply

# Streamlit UI
st.title("🎓 IB GPT Chatbot")
st.write("IB 과목 학습을 돕는 AI 챗봇입니다. Playground의 Instructions를 반영합니다.")

else:
    st.warning("⚠️ 계속하려면 사이드바에 OpenAI API 키를 입력해주세요.")
    
    st.write("""
### 🎓 IB GPT 챗봇 0.1.1-beta (개발 버전)  
             
안녕하세요! 👋 **IB GPT 챗봇**은 IB Diploma Programme(DP) 학생들을 위한 **맞춤형 학습 도우미 AI**입니다.  

💡 **이 챗봇이 도와줄 수 있는 것:**  
✅ **과목별 개념 설명** – Biology, Chemistry, Math 등 다양한 IB 과목 지원  
✅ **IA & EE 가이드** – 주제 선정부터 작성 팁까지 맞춤형 조언 제공  
✅ **시험 대비 & 학습 전략** – IB 평가 기준에 맞춘 효과적인 학습법 제안  
✅ **TOK 및 논리적 사고 지원** – TOK Essay 및 Presentation 준비 도움  

🔑 **사용 방법:**  
1️⃣ **사이드바에 OpenAI API 키를 입력하세요.**  
2️⃣ **궁금한 점을 질문하면 AI가 답변해드립니다!**  
3️⃣ **필요하면 새로운 대화를 시작할 수 있습니다.**  

📌 **IB 학습을 더 쉽고 효율적으로!** 🚀  
지금 바로 질문을 입력하고 챗봇을 활용해 보세요! 😊
""")

# 사용자 입력 받기
user_input = st.chat_input("💬 질문을 입력하세요:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Assistant 호출
    response = run_assistant(user_input)

    # 응답 저장 및 출력
    st.session_state.messages.append({"role": "assistant", "content": response})

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 대화 초기화 버튼
if st.button("🗑 새로운 대화 시작"):
    st.session_state.messages = []
    st.session_state.thread_id = None
    st.experimental_rerun()
