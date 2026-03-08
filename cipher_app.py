# cipher_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Настройка страницы
st.set_page_config(
    page_title="Криптографический Центр - Шифр Цезаря",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Новая цветовая палитра
COLORS = {
    'dark_blue': '#1a365d',
    'blue': '#2a4a7f',
    'light_blue': '#3b5998',
    'gold': '#d4af37',
    'light_gold': '#f4e4a6',
    'dark_gray': '#2d3748',
    'light_gray': '#e2e8f0',
    'white': '#ffffff'
}

# Фон и стили
def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, {COLORS['dark_blue']} 0%, {COLORS['blue']} 100%);
            background-attachment: fixed;
        }}
        
        /* Основные стили */
        .main .block-container {{
            padding: 2rem 1rem;
        }}
        
        /* Заголовки */
        h1, h2, h3, h4, h5, h6 {{
            color: {COLORS['gold']} !important;
            font-family: 'Georgia', serif;
            margin-bottom: 1rem;
        }}
        
        h1 {{
            border-bottom: 3px solid {COLORS['gold']};
            padding-bottom: 0.5rem;
        }}
        
        /* Текст */
        p, li, td {{
            color: {COLORS['dark_gray']} !important;
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
        }}
        
        /* Карточки */
        .card {{
            background: {COLORS['white']};
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-left: 5px solid {COLORS['gold']};
            transition: transform 0.3s ease;
        }}
        
        .card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}
        
        .card-dark {{
            background: {COLORS['dark_blue']};
            color: {COLORS['white']} !important;
            border-left: 5px solid {COLORS['light_gold']};
        }}
        
        .card-dark p, .card-dark li {{
            color: {COLORS['light_gold']} !important;
        }}
        
        /* Кнопки */
        .stButton button {{
            background: linear-gradient(45deg, {COLORS['gold']}, {COLORS['light_gold']});
            color: {COLORS['dark_blue']} !important;
            font-weight: bold;
            border: none;
            padding: 1rem 2rem;
            border-radius: 10px;
            transition: all 0.3s ease;
            width: 100%;
        }}
        
        .stButton button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
        }}
        
        /* Поля ввода */
        .stTextInput input, .stTextArea textarea {{
            background: {COLORS['light_gray']} !important;
            border: 2px solid {COLORS['gold']};
            border-radius: 8px;
            color: {COLORS['dark_gray']} !important;
        }}
        
        .stSlider div {{
            color: {COLORS['gold']} !important;
        }}
        
        .stRadio div {{
            color: {COLORS['gold']} !important;
        }}
        
        /* Боковая панель */
        .css-1d391kg {{
            background: {COLORS['dark_blue']} !important;
        }}
        
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {{
            color: {COLORS['gold']} !important;
        }}
        
        .css-1d391kg p, .css-1d391kg label {{
            color: {COLORS['light_gold']} !important;
        }}
        
        /* Таблицы */
        .dataframe {{
            background: {COLORS['white']} !important;
            border-radius: 10px;
            overflow: hidden;
        }}
        
        /* Прогресс бар */
        .stProgress > div > div {{
            background: linear-gradient(90deg, {COLORS['gold']}, {COLORS['light_gold']});
        }}
        
        /* Иконки */
        .icon {{
            font-size: 2rem;
            margin-bottom: 1rem;
            color: {COLORS['gold']};
        }}
        
        /* Анимации */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .animate {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        /* Адаптивность */
        @media (max-width: 768px) {{
            .card {{
                padding: 1.5rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# Русский алфавит
RUSSIAN_ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
RUSSIAN_ALPHABET_UPPER = RUSSIAN_ALPHABET.upper()

# Функции шифрования
def caesar_cipher(text, shift, mode='encrypt'):
    result = ""
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if char.lower() in RUSSIAN_ALPHABET:
            is_upper = char.isupper()
            alphabet = RUSSIAN_ALPHABET_UPPER if is_upper else RUSSIAN_ALPHABET
            char_pos = alphabet.index(char)
            new_pos = (char_pos + shift) % len(alphabet)
            result += alphabet[new_pos]
        else:
            result += char
    return result

def frequency_analysis(text):
    clean_text = ''.join([char.lower() for char in text if char.lower() in RUSSIAN_ALPHABET])
    total_letters = len(clean_text)
    
    if total_letters == 0:
        return {}
    
    freq = {letter: 0 for letter in RUSSIAN_ALPHABET}
    for char in clean_text:
        if char in freq:
            freq[char] += 1
    
    for letter in freq:
        freq[letter] = (freq[letter] / total_letters) * 100
    
    return freq

def brute_force_caesar(cipher_text):
    results = []
    for shift in range(1, len(RUSSIAN_ALPHABET)):
        decrypted = caesar_cipher(cipher_text, shift, 'decrypt')
        results.append((shift, decrypted))
    return results

def analyze_text_complexity(text):
    """Анализ сложности текста для взлома"""
    clean_text = ''.join([char.lower() for char in text if char.lower() in RUSSIAN_ALPHABET])
    total_chars = len(text)
    total_letters = len(clean_text)
    
    if total_letters == 0:
        return 0
    
    # Оценка сложности (0-100)
    complexity = min(100, (total_letters / 10) + (len(set(clean_text)) / len(RUSSIAN_ALPHABET)) * 50)
    return round(complexity)

# Боковая панель
with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 1rem; background: {COLORS['blue']}; border-radius: 10px;'>
        <h2>🔐 Крипто Центр</h2>
        <p style='color: {COLORS['light_gold']};'>Мастерская шифрования</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Навигация")
    page = st.radio("Выберите раздел:", 
                   ["Шифратор", "История", "Теория", "Практика", "Справочник"])
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Настройки")
    advanced_mode = st.checkbox("Расширенный режим", False)
    show_stats = st.checkbox("Показывать статистику", True)
    
    st.markdown("---")
    
    st.markdown("### 📊 Статистика сессии")
    if 'encryption_count' not in st.session_state:
        st.session_state.encryption_count = 0
    st.metric("Шифрований сегодня", st.session_state.encryption_count)
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style='color: {COLORS['light_gold']}; text-align: center;'>
        <p>🕒 {datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
        <p>v2.1 | Профессиональная версия</p>
    </div>
    """, unsafe_allow_html=True)

# Главный контент
if page == "Шифратор":
    st.markdown(f"""
    <div class='card'>
        <div style='text-align: center;'>
            <h1>🔐 Шифратор Цезаря</h1>
            <p>Профессиональный инструмент для криптографических операций</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Основной функционал
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### 📝 Исходный текст")
        user_text = st.text_area(
            "Введите текст для обработки:",
            "Привет! Это демонстрация работы шифра Цезаря.",
            height=150,
            help="Поддерживаются русские буквы, цифры и специальные символы"
        )
        
        if user_text:
            complexity = analyze_text_complexity(user_text)
            st.progress(complexity/100, f"Сложность взлома: {complexity}%")
    
    with col2:
        st.markdown("### ⚙️ Параметры")
        
        col_params = st.columns(2)
        with col_params[0]:
            shift = st.slider(
                "🔑 Ключ шифрования:",
                min_value=1,
                max_value=32,
                value=3,
                help="Сдвиг букв в алфавите"
            )
        
        with col_params[1]:
            operation = st.radio(
                "📊 Операция:",
                ["Зашифровать", "Расшифровать", "Авто-взлом"],
                index=0
            )
        
        if operation == "Авто-взлом":
            st.warning("⚠️ Режим взлома может занять время для длинных текстов")
        
        if st.button("🚀 Выполнить операцию", type="primary"):
            st.session_state.encryption_count += 1

    # Обработка
    if user_text and st.session_state.get('encryption_count', 0) > 0:
        if operation == "Авто-взлом":
            with st.spinner("🔓 Выполняется взлом шифра..."):
                results = brute_force_caesar(user_text)
                
                st.markdown("### 🔍 Результаты взлома")
                st.info("Найдите осмысленный текст среди вариантов:")
                
                # Показываем первые 5 наиболее вероятных вариантов
                result_data = []
                for shift_val, text in results[:5]:
                    result_data.append({"Ключ": shift_val, "Текст": text})
                
                df = pd.DataFrame(result_data)
                st.dataframe(df, use_container_width=True, height=200)
                
                # Полная таблица для продвинутых пользователей
                if advanced_mode:
                    with st.expander("📋 Полная таблица взлома (32 варианта)"):
                        full_data = [{"Ключ": s, "Текст": t} for s, t in results]
                        st.dataframe(pd.DataFrame(full_data), height=400)
        
        else:
            mode = 'encrypt' if operation == "Зашифровать" else 'decrypt'
            processed_text = caesar_cipher(user_text, shift, mode)
            
            # Результаты
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.markdown("### 📄 Исходный текст")
                st.text_area("", user_text, height=200, label_visibility="collapsed")
            
            with col_res2:
                st.markdown(f"### 📊 Результат ({operation})")
                st.text_area("", processed_text, height=200, label_visibility="collapsed")
            
            # Статистика
            if show_stats:
                st.markdown("### 📈 Анализ текста")
                col_stats = st.columns(3)
                with col_stats[0]:
                    st.metric("Символов всего", len(user_text))
                with col_stats[1]:
                    st.metric("Букв русского алфавита", 
                             len([c for c in user_text if c.lower() in RUSSIAN_ALPHABET]))
                with col_stats[2]:
                    st.metric("Ключ шифрования", shift)
                
                # Анализ частотности
                freq_before = frequency_analysis(user_text)
                freq_after = frequency_analysis(processed_text)
                
                if freq_before and freq_after:
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
                    
                    ax1.bar(freq_before.keys(), freq_before.values(), color=COLORS['blue'], alpha=0.7)
                    ax1.set_title('Частотность исходного текста')
                    ax1.tick_params(axis='x', rotation=45)
                    
                    ax2.bar(freq_after.keys(), freq_after.values(), color=COLORS['gold'], alpha=0.7)
                    ax2.set_title('Частотность результата')
                    ax2.tick_params(axis='x', rotation=45)
                    
                    plt.tight_layout()
                    st.pyplot(fig)

elif page == "История":
    st.markdown(f"""
    <div class='card'>
        <h1>📜 Историческая справка</h1>
        <p>Шифр Цезаря - один из древнейших и самых известных методов шифрования</p>
    </div>
    """, unsafe_allow_html=True)
    
    # История в карточках
    history_data = [
        {"year": "100-44 до н.э.", "title": "Гай Юлий Цезарь", 
         "content": "Римский полководец использовал шифр со сдвигом на 3 позиции для военной переписки"},
        {"year": "IX век", "title": "Арабские ученые", 
         "content": "Разработали методы частотного анализа для взлома моноалфавитных шифров"},
        {"year": "XV век", "title": "Эпоха Возрождения", 
         "content": "Шифр Цезаря использовался дипломатами и правителями по всей Европе"},
        {"year": "XIX век", "title": "Криптография", 
         "content": "Стала научной дисциплиной, шифр Цезаря изучается как базовый пример"},
        {"year": "XXI век", "title": "Современность", 
         "content": "Используется в образовательных целях и как основа для более сложных алгоритмов"}
    ]
    
    for item in history_data:
        with st.container():
            st.markdown(f"""
            <div class='card'>
                <h3>{item['year']} - {item['title']}</h3>
                <p>{item['content']}</p>
            </div>
            """, unsafe_allow_html=True)

elif page == "Теория":
    st.markdown(f"""
    <div class='card'>
        <h1>📚 Теоретические основы</h1>
        <p>Глубокое погружение в математику и принципы шифрования</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Математика", "Криптоанализ", "Безопасность"])
    
    with tabs[0]:
        st.markdown("""
        ### 🧮 Математическая основа
        
        Шифр Цезаря основан на модульной арифметике:
        
        **Формула шифрования:**
        ```
        E(x) = (x + k) mod n
        ```
        
        **Формула дешифрования:**
        ```
        D(x) = (x - k) mod n
        ```
        
        где:
        - `x` - позиция буквы в алфавите (0-32 для русского)
        - `k` - ключ шифрования (сдвиг)
        - `n` - мощность алфавита (33 для русского)
        """)
    
    with tabs[1]:
        st.markdown("""
        ### 🔍 Методы криптоанализа
        
        1. **Полный перебор (Brute Force)**
           - Всего 32 возможных ключа для русского алфавита
           - Время взлома: несколько миллисекунд
        
        2. **Частотный анализ**
           - Анализ частоты встречаемости букв
           - В русском языке самые частые буквы: О, Е, А, И, Н
        
        3. **Анализ контекста**
           - Поиск осмысленных слов и фраз
           - Учет особенностей языка
        """)
    
    with tabs[2]:
        st.markdown("""
        ### 🛡️ Вопросы безопасности
        
        **Уязвимости:**
        - Малое пространство ключей (всего 32 варианта)
        - Сохранение частотных характеристик
        - Уязвимость к частотному анализу
        
        **Защита:**
        - Использование сложных современных алгоритмов
        - Многоалфавитное шифрование
        - Ключи большой длины
        """)

elif page == "Практика":
    st.markdown(f"""
    <div class='card'>
        <h1>🎯 Практические задания</h1>
        <p>Закрепите знания на практике</p>
    </div>
    """, unsafe_allow_html=True)
    
    exercises = [
        {
            "title": "🔄 Базовое шифрование",
            "task": "Зашифруйте фразу 'Секретное сообщение' с ключом 7",
            "solution": "Шифр: Ырцычёъф тъъхёттръ"
        },
        {
            "title": "🔓 Расшифровка",
            "task": "Расшифруйте 'Йуъжхчшё цуёъчюцхё' с ключом 3",
            "solution": "Исходный текст: Привет сообщение"
        },
        {
            "title": "🔍 Взлом шифра",
            "task": "Взломайте шифр 'Бщцфаэ ъ ртууэ мфьэъи' без знания ключа",
            "solution": "Ключ: 3, Текст: Шифр это просто и интересно"
        }
    ]
    
    for i, ex in enumerate(exercises):
        with st.expander(f"{ex['title']} - {ex['task']}"):
            st.write("**Задание:**", ex['task'])
            if st.button(f"Показать решение #{i+1}", key=f"soln_{i}"):
                st.success(f"**Решение:** {ex['solution']}")

elif page == "Справочник":
    st.markdown(f"""
    <div class='card'>
        <h1>📖 Справочник криптографа</h1>
        <p>Полезная информация и справочные материалы</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Таблица частотности букв
    st.markdown("### 📊 Частотность букв русского языка")
    freq_data = {
        'Буква': list('оеаинтсрвлкмдпуяыьгзбчйхжшюцщэфё'),
        'Частота %': [10.97, 8.45, 7.64, 7.09, 6.78, 6.09, 5.68, 5.53, 4.65, 4.32, 
                     3.49, 3.21, 3.06, 2.98, 2.72, 2.54, 2.36, 2.01, 1.90, 1.81, 
                     1.80, 1.70, 1.66, 1.59, 1.44, 1.21, 1.01, 0.97, 0.94, 0.73, 
                     0.64, 0.48, 0.36]
    }
    freq_df = pd.DataFrame(freq_data)
    st.dataframe(freq_df, use_container_width=True)
    
    # Полезные ссылки
    st.markdown("### 🔗 Дополнительные ресурсы")
    resources = [
        {"name": "Википедия: Шифр Цезаря", "url": "https://ru.wikipedia.org/wiki/Шифр_Цезаря"},
        {"name": "Криптография для начинающих", "url": "https://www.cryptool.org/"},
        {"name": "Онлайн-курсы по криптографии", "url": "https://www.coursera.org/learn/crypto"}
    ]
    
    for res in resources:
        st.markdown(f"- [{res['name']}]({res['url']})")

# Футер
st.markdown("---")
st.markdown(f"""
<div class='card-dark'>
    <div style='text-align: center;'>
        <h3>🔐 Криптографический Центр</h3>
        <p>Профессиональный инструмент для изучения основ криптографии</p>
        <p>📧 support@crypto-center.ru</p>
        <p>© 2024 Все права защищены</p>
    </div>
</div>
""", unsafe_allow_html=True)