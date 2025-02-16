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

# Streamlit UI
st.title("🎓 IB GPT Chatbot")

if not api_key:
    st.warning("⚠️ OpenAI API 키를 사이드바에 입력하세요.")
else:
    st.write("IB 과목 학습을 돕는 AI 챗봇입니다. Playground의 Instructions를 반영합니다.")

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

# 버전 정보 저장을 위한 세션 상태 초기화
if "version" not in st.session_state:
    st.session_state.version = None  # 버전 번호

if "version_info" not in st.session_state:
    st.session_state.version_info = None  # 버전 수정 내역

if user_input:
    # 버전 관리 명령어 처리
    if user_input.startswith("/버전 입력"):
        try:
            version_number = user_input.split('("')[1].split('")')[0]
            st.session_state.version = version_number
            response = f"✅ 버전 `{version_number}` 기록 완료!"
        except IndexError:
            response = "❌ 올바른 형식으로 입력해주세요: `/버전 입력 (\"버전번호\")`"

    elif user_input == "/버전 확인":
        if st.session_state.version:
            response = f"📌 현재 버전: `{st.session_state.version}`"
        else:
            response = "❌ 기록된 버전이 없습니다."

    elif user_input.startswith("/버전 정보 입력"):
        try:
            version_info = user_input.split('("')[1].split('")')[0]
            st.session_state.version_info = version_info
            response = "✅ 버전 정보 기록 완료!"
        except IndexError:
            response = "❌ 올바른 형식으로 입력해주세요: `/버전 정보 입력 (\"버전 수정 내역\")`"

    elif user_input == "/버전 정보":
        if st.session_state.version_info:
            response = f"📜 버전 수정 내역:\n{st.session_state.version_info}"
        else:
            response = "❌ 기록된 버전 수정 내역이 없습니다."

    else:
        # 기본 Assistant 응답 처리
        st.session_state.messages.append({"role": "user", "content": user_input})
        response = run_assistant(user_input)

    # 응답 저장 및 출력
    st.session_state.messages.append({"role": "assistant", "content": response})

# 채팅 기록 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
