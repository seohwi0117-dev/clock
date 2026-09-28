import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import time

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="시계 읽기 연습", page_icon="⏰", layout="wide")

# --- 2. 세션 상태(Session State) 초기화 ---
if 'initialized' not in st.session_state:
    st.session_state.hour = 12
    st.session_state.minute = 0
    st.session_state.total = 0
    st.session_state.correct = 0
    st.session_state.wrong = 0
    st.session_state.initialized = True

# 문제 생성 함수
def generate_problem():
    level = st.session_state.difficulty
    st.session_state.hour = random.randint(1, 12)
    
    if level == "1단계: 정시 읽기":
        st.session_state.minute = 0
    elif level == "2단계: 30분 단위 읽기":
        st.session_state.minute = random.choice([0, 30])
    elif level == "3단계: 5분 단위 읽기":
        st.session_state.minute = random.choice(range(0, 60, 5))
    elif level == "4단계: 1분 단위 읽기":
        st.session_state.minute = random.randint(0, 59)

# 처음 실행 시 문제 하나 생성
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = "1단계: 정시 읽기"
    generate_problem()

# --- 3. 시계 그리기 함수 ---
def draw_clock(hour, minute):
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_aspect('equal')
    ax.axis('off')

    # 시계 테두리
    circle = plt.Circle((0, 0), 1, color='#333333', fill=False, linewidth=4)
    ax.add_artist(circle)
    inner_circle = plt.Circle((0, 0), 0.98, color='#f9f9f9', fill=True, zorder=0)
    ax.add_artist(inner_circle)

    # 눈금 및 숫자 그리기
    for i in range(60):
        angle = np.deg2rad(90 - i * 6)
        # 5분(1시간) 단위 눈금
        if i % 5 == 0:
            ax.plot([0.85 * np.cos(angle), 0.95 * np.cos(angle)],
                    [0.85 * np.sin(angle), 0.95 * np.sin(angle)], color='black', lw=3)
            # 숫자 위치 계산 (조금 더 안쪽으로)
            num_angle = np.deg2rad(90 - (i // 5) * 30)
            num = 12 if i == 0 else i // 5
            ax.text(0.72 * np.cos(num_angle), 0.72 * np.sin(num_angle) - 0.02, str(num),
                    ha='center', va='center', fontsize=22, weight='bold', color='#333333')
        # 1분 단위 눈금
        else:
            ax.plot([0.9 * np.cos(angle), 0.95 * np.cos(angle)],
                    [0.9 * np.sin(angle), 0.95 * np.sin(angle)], color='gray', lw=1)

    # 시침 그리기 (분침의 이동에 따라 시침도 자연스럽게 이동하도록 각도 계산)
    h_angle = np.deg2rad(90 - ((hour % 12) * 30 + minute * 0.5))
    ax.plot([0, 0.45 * np.cos(h_angle)], [0, 0.45 * np.sin(h_angle)], color='blue', lw=7, solid_capstyle='round')

    # 분침 그리기
    m_angle = np.deg2rad(90 - minute * 6)
    ax.plot([0, 0.75 * np.cos(m_angle)], [0, 0.75 * np.sin(m_angle)], color='red', lw=4, solid_capstyle='round')

    # 중심점
    ax.plot(0, 0, marker='o', markersize=12, color='#333333')

    return fig

# --- 4. 화면 레이아웃 ---
st.title("⏰ 아날로그 시계 읽기 연습")
st.markdown("시계를 보고 몇 시 몇 분인지 맞혀보세요!")

# 상단: 난이도 설정 및 점수판
top_col1, top_col2 = st.columns([1, 1])

with top_col1:
    st.selectbox(
        "난이도 선택", 
        ["1단계: 정시 읽기", "2단계: 30분 단위 읽기", "3단계: 5분 단위 읽기", "4단계: 1분 단위 읽기"], 
        key='difficulty', 
        on_change=generate_problem
    )

with top_col2:
    st.info(f"📊 **총 문제수:** {st.session_state.total} | 🟢 **정답:** {st.session_state.correct} | 🔴 **오답:** {st.session_state.wrong}")

st.divider()

# 좌측 시계, 우측 입력창
col1, col2 = st.columns([1, 1])

with col1:
    fig = draw_clock(st.session_state.hour, st.session_state.minute)
    st.pyplot(fig)

with col2:
    st.subheader("정답을 입력하세요")
    
    # 입력 필드
    input_h = st.number_input("시 (1~12)", min_value=1, max_value=12, step=1, value=12)
    input_m = st.number_input("분 (0~59)", min_value=0, max_value=59, step=1, value=0)
    
    # 알림 메시지를 띄울 빈 공간
    msg_placeholder = st.empty()
    
    # 정답 확인 버튼
    if st.button("✅ 정답 확인", use_container_width=True):
        st.session_state.total += 1
        
        # 정답일 때
        if input_h == st.session_state.hour and input_m == st.session_state.minute:
            st.session_state.correct += 1
            st.balloons()
            msg_placeholder.success("🎉 정답입니다! 참 잘했어요! (새로운 문제로 이동합니다)")
            
            # 1.5초 대기 후 새로운 문제 출제 및 화면 새로고침
            time.sleep(1.5)
            generate_problem()
            st.rerun()
            
        # 오답일 때
        else:
            st.session_state.wrong += 1
            msg_placeholder.error(f"아쉽네요! 정답은 **{st.session_state.hour}시 {st.session_state.minute}분** 입니다. 다시 도전해 보세요!")
            # 오답 시에는 문제를 재생성하지 않으므로 화면 그대로 유지
