import openai
import streamlit as st
import time
from openai import OpenAI

# Assistant ID (Playground에서 사용한 Assistant ID 확인 필요)
assistant_id = "asst_RnCrKj7G4US5N9EkRwx6UiFC"

# Streamlit UI 설정
st.set_page_config(page_title="IB GPT Chatbot", page_icon="🎓")

# API 키 입력 받기 (자동 로드 제거)
api_key = st.sidebar.text_input("🔑 OpenAI API 키 입력", type="password")

# OpenAI 클라이언트 설정
if api_key:
    client = OpenAI(api_key=api_key)
else:
    client = None

# 세션 상태 초기화 (대화 기록 및 Thread ID 유지)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# API 연결 및 Assistant 실행 함수
def run_assistant(user_input):
    if not client:
        return "❌ OpenAI API 키를 입력하세요."

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

# ✅ API 입력 전/후 UI 다르게 표시
st.title("🎓 IB GPT Chatbot")

if not api_key:
    # 🔴 API 입력 전 UI
    st.warning("⚠️ 계속하려면 사이드바에 OpenAI API 키를 입력해주세요.")
    
    st.markdown("""
    ## IB GPT 챗봇 0.1.2-alpha (개발 버전)
    안녕하세요! 👋 **IB GPT 챗봇**은 IB Diploma Programme(DP) 학생들을 위한 **맞춤형 학습 도우미 AI**입니다.

    ### 🔑 **사용 방법:**
    1️⃣ **사이드바에 OpenAI API 키를 입력하세요.**  
    2️⃣ **help(임시 명령어)를 입력해서 도움받을 과목을 확인하세요.**  
    3️⃣ **필요하면 새로운 대화를 시작할 수 있습니다.**  

    🚀 **IB 학습을 더 쉽고 효율적으로!**  
    지금 바로 질문을 입력하고 챗봇을 활용해 보세요! 😊  
    """)
    st.stop()  # ✅ API 키가 없으면 이후 코드 실행 방지

else:
    # 🟢 API 입력 후 UI
    st.success("✅ OpenAI API 키가 입력되었습니다. 챗봇을 사용할 준비가 완료되었습니다!")
    st.markdown("""
    ## IB GPT 챗봇 사용 안내
    - **과목별 개념 설명 및 학습 지원**
    - **IA & EE 가이드라인 제공**
    - **IB 시험 대비 및 학습 전략 제공**
    - **논리적 사고 및 TOK 지원**
    
    ✨ help (임시 명령어)를 입력해보세요! 💬
    """)

if not api_key:
    st.warning("⚠️ 계속하려면 사이드바에 OpenAI API 키를 입력해주세요.")
    st.stop()  # ✅ API 키가 없으면 이후 코드 실행 방지

# ✅ 사용자 입력 필드를 한 번만 선언 (중복 제거됨)
user_input = st.chat_input("💬 질문을 입력하세요:", key="chat_input")

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
    st.rerun()  # ✅ 최신 Streamlit 버전에서 사용 가능

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#Streamlit 캐시 삭제
if st.sidebar.button("🧹 캐시 삭제"):
    st.cache_data.clear()  # ✅ Streamlit 캐시 삭제
    st.session_state.clear()  # ✅ 세션 상태 초기화
    st.rerun()  # ✅ 페이지 새로고침
