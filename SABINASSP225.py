import streamlit as st
import sqlite3
import pandas as pd
import datetime

# --- Функции БД ---
def init_db():
    conn = sqlite3.connect('fitness.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS activity 
                 (date TEXT, type TEXT, value REAL)''')
    conn.commit()
    conn.close()

# --- ЛОГИКА ВХОДА ---
st.set_page_config(page_title="Fitness Companion", page_icon="💪")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("Вход в систему")
    password = st.text_input("Введите пароль", type="password")
    if st.button("Войти"):
        if password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Неверный пароль")

# --- ОСНОВНОЕ ПРИЛОЖЕНИЕ ---
def main_app():
    init_db()
    st.title("💪 Fitness Companion")
    
    with st.sidebar:
        st.header("Добавить запись")
        date = st.date_input("Дата", datetime.date.today())
        entry_type = st.selectbox("Тип активности", ["Вода (мл)", "Тренировка (мин)"])
        value = st.number_input("Значение", min_value=0.0, step=1.0)
        
        if st.button("Сохранить"):
            if value > 0:
                conn = sqlite3.connect('fitness.db')
                c = conn.cursor()
                c.execute("INSERT INTO activity VALUES (?, ?, ?)", (str(date), entry_type, value))
                conn.commit()
                conn.close()
                st.success("Данные сохранены!")
            else:
                st.error("Введите корректное значение!")

    st.subheader("Статистика")
    conn = sqlite3.connect('fitness.db')
    df = pd.read_sql_query("SELECT * FROM activity", conn)
    conn.close()

    if not df.empty:
        st.dataframe(df)
        chart_data = df.pivot_table(index='date', columns='type', values='value', aggfunc='sum')
        st.line_chart(chart_data)
    else:
        st.info("Нет данных. Добавьте первую запись в боковой панели.")

# --- ВЫЗОВ ---
if not st.session_state.logged_in:
    login()
else:
    main_app()
    if st.sidebar.button("Выйти"):
        st.session_state.logged_in = False
        st.rerun()