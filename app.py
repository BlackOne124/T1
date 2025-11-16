import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime

# Настройка страницы
st.set_page_config(
    page_title="Карьера на автопилоте",
    page_icon="🚀",
    layout="wide"
)

# Инициализация состояния сессии
if 'user_level' not in st.session_state:
    st.session_state.user_level = 1
if 'user_xp' not in st.session_state:
    st.session_state.user_xp = 0
if 'user_coins' not in st.session_state:
    st.session_state.user_coins = 0
if 'badges' not in st.session_state:
    st.session_state.badges = []
if 'career_plan' not in st.session_state:
    st.session_state.career_plan = []

# Данные для демонстрации
CAREER_PATHS = {
    "Data Scientist": ["Python", "SQL", "Машинное обучение", "Статистика"],
    "Frontend Developer": ["JavaScript", "React", "HTML/CSS", "TypeScript"],
    "Project Manager": ["Управление проектами", "Коммуникация", "Agile", "Презентации"]
}

QUESTS = [
    {"id": 1, "name": "Пройди курс по Python", "xp": 100, "coins": 50, "skill": "Python"},
    {"id": 2, "name": "Посмотри вебинар по Agile", "xp": 80, "coins": 40, "skill": "Agile"},
    {"id": 3, "name": "Прочитай статью о React", "xp": 60, "coins": 30, "skill": "React"},
    {"id": 4, "name": "Попроси фидбэк у коллеги", "xp": 120, "coins": 60, "skill": "Коммуникация"}
]

BADGES = {
    "python_beginner": {"name": "Новичок Python", "description": "Выполнил первое задание по Python"},
    "active_learner": {"name": "Активный ученик", "description": "Выполнил 5 заданий"},
    "team_player": {"name": "Командный игрок", "description": "Получил фидбэк от коллеги"}
}


def level_up():
    """Проверка повышения уровня"""
    xp_needed = st.session_state.user_level * 100
    if st.session_state.user_xp >= xp_needed:
        st.session_state.user_level += 1
        st.session_state.user_xp = 0
        st.success(f"🎉 Поздравляем! Вы достигли {st.session_state.user_level} уровня!")
        return True
    return False


def complete_quest(quest_id):
    """Завершение задания"""
    quest = next(q for q in QUESTS if q["id"] == quest_id)
    st.session_state.user_xp += quest["xp"]
    st.session_state.user_coins += quest["coins"]

    # Проверка на получение бейджей
    if quest["skill"] == "Python" and "python_beginner" not in st.session_state.badges:
        st.session_state.badges.append("python_beginner")
        st.balloons()

    level_up()


def ai_assistant_response(message):
    """ИИ-помощник (упрощенная версия)"""
    responses = {
        "привет": "Привет! Я ваш ИИ-помощник по карьере. Чем могу помочь?",
        "карьера": "Проанализировав ваш профиль, я рекомендую развивать навыки в области Data Science.",
        "навыки": "Ваши текущие навыки: Python, SQL. Рекомендую изучить машинное обучение.",
        "план": "Ваш карьерный план: 1. Изучить Python 2. Освоить SQL 3. Изучить ML",
        "квесты": "Сегодня доступны квесты по Python и Agile разработке."
    }

    return responses.get(message.lower(), "Я помогу вам с карьерным развитием. Спросите о навыках, плане или квестах.")


# Заголовок приложения
st.title("🚀 Карьера на автопилоте")
st.markdown("---")

# Боковая панель с профилем
with st.sidebar:
    st.header("👤 Ваш профиль")

    # Аватар и уровень
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🎯")
    with col2:
        st.markdown(f"**Уровень {st.session_state.user_level}**")

    # Прогресс бар
    xp_needed = st.session_state.user_level * 100
    progress = min(st.session_state.user_xp / xp_needed, 1.0)
    st.progress(progress)
    st.markdown(f"Опыт: {st.session_state.user_xp}/{xp_needed}")
    st.markdown(f"Монеты: 🪙 {st.session_state.user_coins}")

    # Бейджи
    st.subheader("🏅 Ваши бейджи")
    for badge_id in st.session_state.badges:
        badge = BADGES[badge_id]
        st.markdown(f"**{badge['name']}**")
        st.caption(badge['description'])

    st.markdown("---")
    st.info("💡 Выполняйте задания для повышения уровня и получения наград!")

# Основная область контента
tab1, tab2, tab3, tab4 = st.tabs(["🎯 Карьерная карта", "📚 Квесты", "🤖 ИИ-помощник", "🏆 Достижения"])

with tab1:
    st.header("Ваша карьерная карта")

    # Выбор карьерного пути
    career_path = st.selectbox("Выберите карьерный путь:", list(CAREER_PATHS.keys()))

    if career_path:
        st.subheader(f"Навыки для {career_path}:")

        # Отображение навыков в виде прогресс-баров
        for skill in CAREER_PATHS[career_path]:
            progress = random.uniform(0.1, 0.8)  # Демо-прогресс
            st.markdown(f"**{skill}**")
            st.progress(progress)

        # Дерево развития (упрощенное)
        st.subheader("🎄 Дерево развития")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("##### 🌱 Начальный уровень")
            st.markdown("- Основы Python")
            st.markdown("- Базы SQL")

        with col2:
            st.markdown("##### 🌿 Средний уровень")
            st.markdown("- Продвинутый Python")
            st.markdown("- Фреймворки ML")

        with col3:
            st.markdown("##### 🎄 Продвинутый уровень")
            st.markdown("- Архитектура данных")
            st.markdown("- Лидерство в проектах")

with tab2:
    st.header("📚 Активные квесты")

    for quest in QUESTS:
        with st.expander(f"🎯 {quest['name']} - 🪙{quest['coins']} - ⭐{quest['xp']} XP"):
            st.write(f"**Навык:** {quest['skill']}")
            if st.button(f"Выполнить", key=f"quest_{quest['id']}"):
                complete_quest(quest["id"])
                st.rerun()

with tab3:
    st.header("🤖 ИИ-помощник по карьере")

    # Чат интерфейс
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant",
             "content": "Привет! Я ваш ИИ-помощник по карьерному развитию. Задайте мне вопрос о ваших навыках, карьерном плане или доступных заданиях."}
        ]

    # Отображение истории чата
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Ввод сообщения
    if prompt := st.chat_input("Задайте вопрос ИИ-помощнику..."):
        # Добавление сообщения пользователя
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Ответ ИИ
        response = ai_assistant_response(prompt)
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

with tab4:
    st.header("🏆 Достижения и статистика")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Статистика")
        st.metric("Общий опыт", f"{st.session_state.user_xp} XP")
        st.metric("Уровень", st.session_state.user_level)
        st.metric("Выполнено заданий", len(st.session_state.badges))
        st.metric("Накоплено монет", f"🪙 {st.session_state.user_coins}")

    with col2:
        st.subheader("🎯 Прогресс навыков")

        skills_data = {
            "Навык": ["Python", "SQL", "ML", "Коммуникация", "Управление"],
            "Прогресс": [65, 40, 25, 70, 35]
        }
        skills_df = pd.DataFrame(skills_data)

        for _, row in skills_df.iterrows():
            st.markdown(f"**{row['Навык']}**")
            st.progress(row['Прогресс'] / 100)

# Футер
st.markdown("---")
st.markdown("### 🚀 Карьера на автопилоте | Холдинг Т1")
st.caption("Ваш персональный помощник в карьерном развитии")
