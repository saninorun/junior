import sqlalchemy
import datetime

from sqlalchemy import Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    pass

class QuestionBD(Base):
    '''Класс модели для создания и работы с таблицы БД'''

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    question: Mapped[str] = mapped_column(nullable=False, unique=True)
    answer: Mapped[str] = mapped_column(nullable=False, unique=True)
    created_at: Mapped[datetime.datetime] = mapped_column(sqlalchemy.TIMESTAMP(timezone=True), nullable=False)
    

    __table_args__ = (
        Index('number_question', "question_id"),
        )