import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgres/mydb"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


@contextmanager
def session():
    sess = sessionmaker(
        expire_on_commit=False, autocommit=False, autoflush=False, bind=engine
    )()
    try:
        yield sess
        sess.commit()
    except Exception as exc:
        logger.error(f"Encountered {exc}, rolling back...")
        sess.rollback()
        raise
    finally:
        sess.close()
