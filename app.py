import streamlit as st
import random

# Setup page
st.set_page_config(page_title="🎮 Math Game for Kids", layout="centered")
st.title("🧠 Math Game untuk Anak SMP")
st.caption("Belajar matematika sambil main 🎯")

# Session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "question" not in st.session_state:
    st.session_state.question = ""
    st.session_state.answer = 0
if "level" not in st.session_state:
    st.session_state.level = "Mudah"

# LEVEL PILIHAN
st.sidebar.title("🎚️ Level Kesulitan")
level = st.sidebar.radio("Pilih level:", ["Mudah", "Sedang", "Sulit"])
st.session_state.level = level

# Range angka per level
if level == "Mudah":
    batas = 10
elif level == "Sedang":
    batas = 50
else:
    batas = 100

# Generate new question
def generate_question():
    a = random.randint(1, batas)
    b = random.randint(1, batas)
    op = random.choice(["+", "-", "*"])
    question = f"{a} {op} {b}"
    answer = eval(question)
    return question, answer

# Soal awal
if st.session_state.question == "":
    q, ans = generate_question()
    st.session_state.question = q
    st.session_state.answer = ans

# TAMPILKAN SOAL
st.subheader("📘 Soal Matematika:")
st.markdown(f"### `{st.session_state.question}`")

# Input jawaban
jawaban = st.number_input("💬 Masukkan jawaban kamu:", step=1)

# Cek jawaban
if st.button("✅ Cek Jawaban"):
    if jawaban == st.session_state.answer:
        st.success("🎉 Benar! Kamu pintar banget!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Salah. Jawaban yang benar: `{st.session_state.answer}`")

    # Soal baru
    q, ans = generate_question()
    st.session_state.question = q
    st.session_state.answer = ans

# Tampilkan skor
st.markdown(f"### 🏆 Skor Kamu: `{st.session_state.score}`")

# Reset
if st.button("🔁 Reset Skor"):
    st.session_state.score = 0
    st.success("Skor sudah direset ke 0!")