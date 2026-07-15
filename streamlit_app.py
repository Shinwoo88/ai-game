import random
import streamlit as st

st.set_page_config(page_title="영단어 게임", page_icon="📚", layout="centered")

WORDS = [
    {"word": "friendly", "meaning": "친절한", "hint": "사람을 반갑게 맞이해요"},
    {"word": "brave", "meaning": "용감한", "hint": "위험이 있어도 두려워하지 않아요"},
    {"word": "delicious", "meaning": "맛있는", "hint": "음식이 아주 맛있어요"},
    {"word": "library", "meaning": "도서관", "hint": "책을 읽는 장소예요"},
    {"word": "imagine", "meaning": "상상하다", "hint": "눈에 보이지 않는 것을 머릿속에 그려요"},
    {"word": "exercise", "meaning": "운동하다", "hint": "몸을 움직여 건강을 챙겨요"},
    {"word": "protect", "meaning": "지키다", "hint": "위험으로부터 안전하게 지켜요"},
    {"word": "curious", "meaning": "호기심이 많은", "hint": "왜냐고 자꾸 궁금해해요"},
    {"word": "schedule", "meaning": "일정", "hint": "해야 할 일을 시간 순서대로 적어요"},
    {"word": "celebrate", "meaning": "축하하다", "hint": "기쁜 일을 함께 기뻐해요"},
]

MAX_QUESTIONS = 10


def build_question():
    base = random.choice(WORDS)
    distractors = random.sample(
        [item["meaning"] for item in WORDS if item["word"] != base["word"]],
        3,
    )
    choices = distractors + [base["meaning"]]
    random.shuffle(choices)
    return {
        "word": base["word"],
        "meaning": base["meaning"],
        "hint": base["hint"],
        "choices": choices,
    }


def start_game():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.current_question = build_question()
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.finished = False


def check_answer(choice):
    current = st.session_state.current_question
    st.session_state.answered = True
    st.session_state.selected = choice
    if choice == current["meaning"]:
        st.session_state.score += 1


def next_question():
    if st.session_state.current_index + 1 >= MAX_QUESTIONS:
        st.session_state.finished = True
    else:
        st.session_state.current_index += 1
        st.session_state.current_question = build_question()
        st.session_state.answered = False
        st.session_state.selected = None


if "current_index" not in st.session_state:
    start_game()

st.title("📚 중학생 영단어 게임")
st.write("영단어의 뜻을 골라 점수를 올려보세요. 쉬운 단어로 만든 게임입니다.")

with st.sidebar:
    st.header("📖 단어장")
    for item in WORDS:
        st.write(f"{item['word']} - {item['meaning']}")
    st.button("새 게임 시작", on_click=start_game)

if st.session_state.finished:
    st.success(f"게임 종료! 총 {MAX_QUESTIONS}문제 중 {st.session_state.score}개 맞췄어요.")
    st.write("한 번 더 도전해 볼까요?")
    st.button("다시 시작", on_click=start_game)
else:
    current = st.session_state.current_question
    st.subheader(f"문제 {st.session_state.current_index + 1}/{MAX_QUESTIONS}")
    st.write("아래 영어 단어의 뜻으로 가장 알맞은 것을 고르세요.")
    st.markdown(f"### {current['word']}")
    st.caption(f"힌트: {current['hint']}")

    for choice in current["choices"]:
        if st.button(choice, key=f"{st.session_state.current_index}-{choice}"):
            check_answer(choice)

    if st.session_state.answered:
        if st.session_state.selected == current["meaning"]:
            st.success("정답입니다! 👍")
        else:
            st.error(f"아쉽네요. 정답은 {current['meaning']}입니다.")

        st.write(f"현재 점수: {st.session_state.score}점")
        st.button("다음 문제", on_click=next_question)
