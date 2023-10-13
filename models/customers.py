import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, constr, conint
from fastapi import HTTPException, status


ERROR_INPUT_USER = HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Ошибка! Для ввода ФИО требуется использовать только алфавитные символы!'
            )

class AskQuestions(BaseModel):
    questions_num: conint(le = 100)

class Question(BaseModel):
    question_id: int
    question: str
    answer: str
    created_at: datetime.datetime

    model_config = ConfigDict(
                            extra='ignore',
                            )
        
    def __init__(self, **kwargs):
        kwargs['question_id'] = kwargs['id']
        super().__init__(**kwargs) 
    
class QuestionShow(BaseModel):
    question_id: int
    question: str
    answer: str
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes = True)