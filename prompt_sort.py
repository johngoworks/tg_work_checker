from google import genai
from pydantic import BaseModel
from pprint import pformat
from dotenv import load_dotenv
import os

load_dotenv()


class Vacancy(BaseModel):
    position: str
    salary: str
    short_description: str
    sender: str
    message_link: str
    requirements: str
    conditions: str


client = genai.Client(api_key=os.environ.get("GENAI_API_KEY"))

prompt = """Ты — помощник по поиску и структурированию вакансий из сообщений Telegram.  
На вход получаешь объект такой структуры:
```

{
"keywords": "<строка с ключевыми словами или требованию к вакансии>",
"messages": [
{
"date": "YYYY-MM-DD HH:MM:SS",
"sender": "<Telegram‑username канала или чата‑отправителя (без @)>",
"link": "<ссылка на конкретное сообщение в формате [https://t.me/…/ID](https://t.me/…/ID)>",
"text": "<текст сообщения>"
},
…
]
}

```
Твоя задача:
1. Отбирать только те сообщения из массива `messages`, в поле `text` которых встречаются ключевые слова или тробавния из `keywords` (регистронезависимо) и очищая текст от всяких лишних знаков.
2. Для каждого найденного сообщения извлечь и вернуть в JSON следующие поля:
   - `position` — должность (название вакансии).
   - `salary` — указанный в тексте диапазон или конкретная сумма.
   - `short_description` — первые 1–2 предложения текста, отражающие суть вакансии.
   - `sender` — значение поля `sender` из входного сообщения.
   - `message_link` — значение поля `link` из входного сообщения.
   - `requirements` — раздел «Требования» из текста.
   - `conditions` — раздел «Условия» из текста.
3. Если какого‑то раздела нет — указывать `"не обнаружено"`.
4. Выдать **только** JSON‑массив объектов, без лишнего текста.

**Важно:**  
- Ключевые слова искать только в поле `text`.  
- Не добавлять дополнительных полей.  
- Выдавать только валидный JSON.
- Не использовать markdown или другие форматы.
- Очищать ответ от лишних символов 
-

входные данные:
"""


def start_sort_vacancies(data_to_sort, sort_filter):
    content_to_send = {"keywords": sort_filter, "messages": data_to_sort}
    print(pformat(content_to_send))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt + pformat(content_to_send),
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Vacancy],
        },
    )
    return response.parsed
