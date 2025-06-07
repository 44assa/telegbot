from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from db import create_database, insert_faq

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Главная страница админ-панели
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    faqs = get_all_faqs()
    return templates.TemplateResponse("index.html", {"request": request, "faqs": faqs})


# Получение всех вопросов и ответов из базы данных
def get_all_faqs():
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM faq')
    faqs = cursor.fetchall()
    connection.close()
    return [{"id": row[0], "category": row[1], "question": row[2], "answer": row[3]} for row in faqs]


# Добавление нового вопроса и ответа
@app.post("/add/")
async def add_faq(category: str = Form(...), question: str = Form(...), answer: str = Form(...)):
    insert_faq(category, question, answer)
    return {"message": "Вопрос успешно добавлен"}

# Удаление вопроса по ID
@app.post("/delete/{faq_id}")
async def delete_faq(faq_id: int):
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM faq WHERE id = ?', (faq_id,))
    connection.commit()
    connection.close()
    return {"message": "Вопрос успешно удален"}


# Обновление вопроса и ответа по ID
@app.post("/update/{faq_id}")
async def update_faq(faq_id: int, category: str = Form(...), question: str = Form(...), answer: str = Form(...)):
    connection = sqlite3.connect('faq.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE faq SET category=?, question=?, answer=? WHERE id=?',
                   (category, question, answer, faq_id))
    connection.commit()
    connection.close()
    return {"message": "Вопрос успешно обновлен"}
