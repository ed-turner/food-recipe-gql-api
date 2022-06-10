
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine


from settings import Settings

engine = create_engine(Settings().DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    """
    This is just an async method to get the session

    :return:
    """

    session: Session = SessionLocal()

    try:
        yield session
    except Exception as e:
        session.rollback()

        raise e

    finally:
        session.close()
