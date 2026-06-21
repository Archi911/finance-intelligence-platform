from sqlmodel import create_engine, Session

DATABASE_URL = (
    "postgresql://postgres:archi123@localhost:5432/fin-project"
)

engine = create_engine(
    DATABASE_URL,
    echo=True
)


def get_session():
    with Session(engine) as session:
        yield session