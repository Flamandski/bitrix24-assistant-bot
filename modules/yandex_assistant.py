import requests
from config import YANDEX_IAM_TOKEN, YANDEX_FOLDER_ID
from modules.database import SessionLocal, BitrixDoc

class YandexAssistantManager:
    def __init__(self):
        self.iam_token = YANDEX_IAM_TOKEN
        self.folder_id = YANDEX_FOLDER_ID
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        
        if not self.iam_token:
            raise Exception("❌ YANDEX_IAM_TOKEN не указан в .env!")
        if not self.folder_id:
            raise Exception("❌ YANDEX_FOLDER_ID не указан в .env!")
            
        print("✅ YandexGPT инициализирован (прямой режим)")

    def _get_headers(self):
        return {
            "Authorization": f"Bearer {self.iam_token}",
            "x-folder-id": self.folder_id,
            "Content-Type": "application/json"
        }

    def _search_in_database(self, query: str) -> str:
        """Ищет релевантную документацию в БД по ключевым словам"""
        db = SessionLocal()
        try:
            keywords = query.lower().split()
            docs = db.query(BitrixDoc).all()
            
            relevant_docs = []
            for doc in docs:
                doc_text = (doc.title + " " + doc.content).lower()
                if any(keyword in doc_text for keyword in keywords if len(keyword) > 3):
                    relevant_docs.append(doc)
            
            if relevant_docs:
                context = "\n\n---\n\n".join([
                    f"### {doc.title}\nURL: {doc.url}\n\n{doc.content[:1000]}..."
                    for doc in relevant_docs[:3]
                ])
                return context
            else:
                return "Документация не найдена в базе данных."
        finally:
            db.close()

    def send_message(self, session_id, text_query):
        """Отправляет запрос в YandexGPT с контекстом из БД"""
        
        print(f"🔍 Ищу документацию по запросу: {text_query}")
        context = self._search_in_database(text_query)
        
        system_prompt = """Ты — эксперт по API Bitrix24. Отвечай на вопросы разработчиков, 
опираясь на предоставленную документацию. Будь точным, кратким и полезным. 
Если не знаешь ответа или документации недостаточно — честно скажи об этом.
Всегда указывай ссылку на источник, если он есть в документации."""

        user_message = f"""Контекст из документации Bitrix24:

{context}

---

Вопрос пользователя: {text_query}

Ответь на вопрос, используя только информацию из документации выше."""

        payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,  
                "maxTokens": "2000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": system_prompt
                },
                {
                    "role": "user",
                    "text": user_message
                }
            ]
        }
        
        print(f"🤖 Отправляю запрос в YandexGPT...")
        response = requests.post(
            self.api_url,
            json=payload,
            headers=self._get_headers(),
            timeout=60.0
        )
        
        if response.status_code == 200:
            data = response.json()
            try:
                answer = data["result"]["alternatives"][0]["message"]["text"]
                print(f"✅ Получен ответ от YandexGPT ({len(answer)} символов)")
                return answer
            except (KeyError, IndexError) as e:
                print(f"❌ Ошибка парсинга ответа: {e}")
                print(f"   Полный ответ: {data}")
                return "Не удалось получить ответ от YandexGPT."
        else:
            print(f"❌ YandexGPT API Error: {response.status_code}")
            print(f"   Ответ: {response.text[:500]}")
            return "Произошла ошибка при обращении к YandexGPT."