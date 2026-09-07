import streamlit as st
import plotly.graph_objects as go
import random
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="인터랙티브 구구단 탐구소",
    page_icon="🔢",
    layout="wide"
)

# 세션 상태 초기화 (상태 관리)
if 'quiz_dan' not in st.session_state:
    st.session_state.quiz_dan = random.randint(2, 9)
    st.session_state.quiz_num = random.randint(1, 9)
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.feedback = None

def generate_new_quiz():
    """새로운 퀴즈 문제 생성 함수"""
    st.session_state.quiz_dan = random.randint(2, 9)
    st.session_state.quiz_num = random.randint(1, 9)
    st.session_state.feedback = None

def render_dot_matrix(dan, num):
    """곱셈의 기하학적 개념(행렬/격자)을 시각화하는 Plotly 차트 생성"""
    x_coords = [i for i in range(1, num + 1) for _ in range(dan)]
    y_coords = [j for j in range(1, dan + 1)] * num

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_coords,
        y=y_coords,
        mode='markers',
        marker=dict(
            size=18,
            color='#3182CE',
            symbol='circle',
            line=dict(width=2, color='#2B6CB0')
        ),
        hoverinfo='none'
    ))

    fig.update_layout(
        title=f"<b>{dan}개씩 {num}묶음 (개수: {dan * num}개)</b>",
        title_font_size=16,
        xaxis=dict(range=[0, max(num + 1, 10)], dtick=1, showgrid=True, zeroline=False),
        yaxis=dict(range=[0, max(dan + 1, 10)], dtick=1, showgrid=True, zeroline=False),
        width=450,
        height=350,
        margin=dict(l=30, r=30, t=50, b=30),
        plot_bgcolor='#F7FAFC'
    )
    return fig

# 메인 타이틀
st.title("🔢 인터랙티브 구구단 탐구소")
st.caption("수학적 시각화와 퀴즈를 통해 구구단의 원리를 완벽히 이해해 보세요.")

# 탭 구성
tab1, tab2 = st.tabs(["📘 원리 탐구 모드", "🧠 실력 테스트 모드"])

# ==========================================
# TAB 1: 원리 탐구 모드
# ==========================================
with tab1:
    st.subheader("구구단 시각화 및 수열 분석")
    
    col_input, col_chart = st.columns([1, 1])

    with col_input:
        selected_dan = st.slider("학습할 단을 선택하세요 (2~9단)", min_value=2, max_value=9, value=2)
        selected_num = st.slider("곱할 수를 선택하세요 (1~9)", min_value=1, max_value=9, value=5)
        
        product = selected_dan * selected_num
        
        st.markdown("---")
        st.markdown(f"### 📐 연산 식: **{selected_dan} × {selected_num} = {product}**")
        
        # 동차덧셈(Repeated Addition) 연산 수식 표현
        addition_str = " + ".join([str(selected_dan)] * selected_num)
        st.info(f"💡 **동차덧셈 표현:**\n\n{addition_str} = **{product}**")
        
        # 등차수열의 관점 제공
        st.success(f"📊 **{selected_dan}단의 공차(Common Difference):** +{selected_dan}")

    with col_chart:
        # 도트 매트릭스 시각화 출력
        fig = render_dot_matrix(selected_dan, selected_num)
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TAB 2: 실력 테스트 모드
# ==========================================
with tab2:
    st.subheader("무작위 구구단 퀴즈")
    
    col_q, col_score = st.columns([2, 1])
    
    with col_score:
        st.metric("현재 점수", f"{st.session_state.score} 점")
        st.metric("풀었던 총 문제 수", f"{st.session_state.total_questions} 개")
        if st.button("점수 초기화"):
            st.session_state.score = 0
            st.session_state.total_questions = 0
            generate_new_quiz()
            st.rerun()

    with col_q:
        q_dan = st.session_state.quiz_dan
        q_num = st.session_state.quiz_num
        correct_answer = q_dan * q_num
        
        st.markdown(f"### ❓ 문제: **{q_dan} × {q_num} = ?**")
        
        with st.form(key='quiz_form', clear_on_submit=True):
            user_answer = st.number_input("정답을 입력하세요:", min_value=0, max_value=81, step=1, key="user_input")
            submit_button = st.form_submit_button(label='정답 제출')

        if submit_button:
            st.session_state.total_questions += 1
            if user_answer == correct_answer:
                st.session_state.score += 10
                st.session_state.feedback = ("correct", f"🎉 정답입니다! ({q_dan} × {q_num} = {correct_answer})")
            else:
                st.session_state.feedback = ("wrong", f"❌ 아쉽네요. 정답은 **{correct_answer}**입니다. ({q_dan} × {q_num} = {correct_answer})")
            
            generate_new_quiz()
            st.rerun()

        # 피드백 출력
        if st.session_state.feedback:
            status, msg = st.session_state.feedback
            if status == "correct":
                st.balloons()
                st.success(msg)
            else:
                st.error(msg)
