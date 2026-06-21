from groq import Groq
from dotenv import load_dotenv

import os
import json

load_dotenv()


class InsightAgent:

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    @staticmethod
    def generate_insight(
        question: str,
        sql: str,
        result
    ):

        prompt = f"""
You are a senior financial analyst.

Question:
{question}

Generated SQL:
{sql}

Database Result:
{result}

Your task:

1. Answer the user's question clearly.
2. Provide important business insights if visible.
3. Highlight anomalies or risks if any.
4. Suggest the best visualization.

Only provide insights directly supported by the data.

If the result set is too small to infer trends,
patterns, anomalies, consistency, growth,
or variance, explicitly state:

"Insufficient data available for deeper analysis."

Never invent financial insights.

Allowed visualizations:

- kpi
- table
- bar_chart
- line_chart
- pie_chart

Return JSON only.

Example:

{{
    "answer":
    "Total GST amount is ₹9,360.",

    "insights":
    [
        "GST values appear consistent.",
        "No unusual variance detected."
    ],

    "visualization":
    "kpi"
}}
"""

        response = InsightAgent.client.chat.completions.create(
            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()

        return json.loads(content)