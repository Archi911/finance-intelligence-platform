from fastapi import APIRouter
from pydantic import BaseModel
from backend.app.services.agents.sql_agent import SQLAgent
from backend.app.services.agents.insight_agent import InsightAgent
from backend.app.services.agents.visualization_agent import VisualizationAgent
from backend.app.services.sql_guard import SQLGuard
from backend.app.services.sql_engine import SQLEngine

router = APIRouter()


class QuestionRequest(BaseModel):
    question: str





@router.post("/analytics")
def analytics(request: QuestionRequest):

    sql = SQLAgent.generate_sql(
    request.question
)

    if not SQLGuard.is_safe(sql):
        return {
            "error": "Unsafe query blocked"
        }

    result = SQLEngine.execute(sql)

    result = [
        list(row)
        for row in result
    ]

    insight = InsightAgent.generate_insight(
        request.question,
        sql,
        result
    )

    return {
    **insight,
    "sql": sql,
    "data": result
}