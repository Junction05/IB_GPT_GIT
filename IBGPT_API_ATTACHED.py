import streamlit as st
import time

# 페이지 설정
st.set_page_config(page_title="IB GPT 챗봇", page_icon="🛠")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 미리 정의된 응답들
predefined_responses = {
    "안녕": "안녕하세요! IB GPT 챗봇입니다. 어떤 도움이 필요하신가요?",
    "ib": "IB(International Baccalaureate)는 국제적으로 인정받는 교육 프로그램입니다. 어떤 부분에 대해 알고 싶으신가요?",
    "tok": "TOK(Theory of Knowledge)는 IB 디플로마 프로그램의 핵심 요소입니다. TOK 에세이나 프레젠테이션에 대해 도움이 필요하신가요?",
    "default": "죄송합니다. 현재 이 기능은 개발 중입니다. 곧 더 나은 답변을 제공할 수 있도록 하겠습니다."
}

# 메인 페이지 제목
st.title("IB GPT ChatBot 💬")

# 챗봇 소개 정보
st.write("""
### 🎓 IB GPT 챗봇 0.1.0-beta (개발 버전)  

안녕하세요! 👋 **IB GPT 챗봇**은 IB Diploma Programme(DP) 학생들을 위한 **맞춤형 학습 도우미 AI**입니다.  

💡 **이 챗봇이 도와줄 수 있는 것:**  
✅ **과목별 개념 설명** – Biology, Chemistry, Math 등 다양한 IB 과목 지원  
✅ **IA & EE 가이드** – 주제 선정부터 작성 팁까지 맞춤형 조언 제공  
✅ **시험 대비 & 학습 전략** – IB 평가 기준에 맞춘 효과적인 학습법 제안  
✅ **TOK 및 논리적 사고 지원** – TOK Essay 및 Presentation 준비 도움  

📌 **IB 학습을 더 쉽고 효율적으로!** 🚀  
지금 바로 질문을 입력하고 챗봇을 활용해 보세요! 😊
""")

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요!~"):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 응답 생성
    time.sleep(1)  # 응답 시간 시뮬레이션
    
    # 키워드 기반 응답 선택
    response = None
    prompt_lower = prompt.lower()
    for key in predefined_responses:
        if key in prompt_lower:
            response = predefined_responses[key]
            break
    
    if response is None:
        response = predefined_responses["default"]
    
    # 어시스턴트 응답 추가
    st.session_state.messages.append({"role": "assistant", "content": response})

# 채팅 히스토리 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 새로운 대화 시작 버튼
if st.button("새로운 대화 시작"):
    st.session_state.messages = []
    st.experimental_rerun()