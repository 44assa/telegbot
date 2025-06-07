import sqlite3

# Функция для создания базы данных
def create_database():
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS faq (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()

create_database()

# Функция для добавления вопросов и ответов
def insert_faq(category, question, answer):
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO faq (category, question, answer) VALUES (?, ?, ?)', (category, question, answer))
    connection.commit()
    connection.close()

# Функция для получения категорий
def get_categories():
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT category FROM faq')
    categories = [row[0] for row in cursor.fetchall()]
    connection.close()
    return categories

# Функция для получения вопросов из базы данных
def get_questions_by_category(category):
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('SELECT question FROM faq WHERE category = ?', (category,))
    questions = [row[0] for row in cursor.fetchall()]
    connection.close()
    return questions

def get_answer(question):
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('SELECT answer FROM faq WHERE question = ?', (question,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else 'Извините, ответ не найден.'
