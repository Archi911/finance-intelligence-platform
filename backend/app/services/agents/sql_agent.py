from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

class SQLAgent:

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    @staticmethod
    def generate_sql(question: str):

        PROMPT_PATH = (
            Path(__file__).resolve().parent.parent
            / "prompts"
            / "text_to_sql_system.txt"
        )

        print("Prompt Path:", PROMPT_PATH)
        print("Exists:", PROMPT_PATH.exists())

        with open(PROMPT_PATH, "r", encoding="utf-8") as f:
            system_prompt = f.read()

        response = SQLAgent.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
        )

        sql = response.choices[0].message.content
        sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql