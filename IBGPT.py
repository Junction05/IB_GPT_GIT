import streamlit as st
import openai
from openai import OpenAI
import time

# 페이지 설정
st.set_page_config(page_title="IB GPT 챗봇)", page_icon="🛠")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# 사이드바에 API 키 입력 필드 추가
with st.sidebar:
    st.title("설정")
    api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")
    assistant_id = "asst_RnCrKj7G4US5N9EkRwx6UiFC"  # 고정된 Assistant ID

# 메인 페이지 제목
st.title("IB GPT ChatBot 💬")

# API 키가 입력되었을 때만 채팅 기능 활성화
if api_key:
    try:
        # OpenAI 클라이언트 초기화
        client = OpenAI(api_key=api_key)

        # Thread ID가 없으면 새로운 Thread 생성
        if st.session_state.thread_id is None:
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id

        # 사용자 입력 처리
        if prompt := st.chat_input("메시지를 입력하세요!"):
            # 메시지 추가
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # OpenAI API에 메시지 전송
            message = client.beta.threads.messages.create(
                thread_id=st.session_state.thread_id,
                role="user",
                content=prompt
            )

            # 실행 생성 및 응답 대기
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant_id
            )

            # 실행 완료 대기
            while run.status in ["queued", "in_progress"]:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state.thread_id,
                    run_id=run.id
                )
                time.sleep(0.5)

            # 응답 받기
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id
            )
            
            # 최신 응답 저장
            assistant_message = messages.data[0].content[0].text.value
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})

        # 채팅 히스토리 표시
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
else:
    st.warning("계속하려면 사이드바에 OpenAI API 키를 입력해주세요.")
    st.write("""
### 🎓 IB GPT 챗봇 0.1.0-beta (개발 버전)  

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


# 새로운 대화 시작 버튼
if st.button("새로운 대화 시작"):
    st.session_state.messages = []
    st.session_state.thread_id = None
    st.experimental_rerun()