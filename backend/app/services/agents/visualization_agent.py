from groq import Groq
from dotenv import load_dotenv

import os
import json

load_dotenv()


class VisualizationAgent:

    client = Groq(
        api_key=os.getenv("GROQ_API_KEY")
    )

    @staticmethod
    def suggest_visualization(
        question: str
    ):

        prompt = f"""
You are a data visualization expert.

Question:
{question}

Choose ONLY ONE:

- kpi
- table
- bar_chart
- line_chart
- pie_chart

Rules:

Single metric:
-> kpi

Comparison:
-> bar_chart

Trend over time:
-> line_chart

Category distribution:
-> pie_chart

Raw records:
-> table

Return JSON only.

Example:

{{
    "visualization": "bar_chart"
}}
"""

        response = (
            VisualizationAgent.client
            .chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
        )

        content = (
            response
            .choices[0]
            .message
            .content
        )

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(content)