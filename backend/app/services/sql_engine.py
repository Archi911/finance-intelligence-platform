from sqlmodel import Session
from sqlalchemy import text
from backend.app.database.connection import engine


class SQLEngine:

    @staticmethod
    def execute(sql_query: str):

        with Session(engine) as session:
            result = session.exec(
                text(sql_query)
            )
            return result.all()