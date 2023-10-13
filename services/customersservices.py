import httpx
import sqlalchemy
from fastapi import Depends, HTTPException, status
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from models.customers import AskQuestions, QuestionShow, Question
from dbtable.dbmodel import QuestionBD
from core.database import get_session


class CustomerService:
    
    def __init__(self, session: AsyncSession = Depends(get_session)):
        self.session = session

    async def _getQuestionsFromUrl(self, *, num: int) -> list[Question]:
        """
        Функция для получения ответа от удаленного API (получения вопросов для викторины)

        """

        try:
            async with httpx.AsyncClient() as client:
                request_questions = await client.get(f'https://jservice.io/api/random?count={num}')
            return request_questions.json()
        except HTTPException:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Что-то не так с удаленным сервером! "
                    )
    
    async def _getQuestionsIdsFromDb(self, *, min_question_id: int, max_question_id: int,) -> set[int]:
        """
        Функция делает запросы к БД для получения уже сохраненных вопросов.
        Возвращает список с номерами уже сохраненых вопросов либо None.
        
        """
        
        query = select(  
            QuestionBD.question_id,                                     
            ).where(
                    and_(QuestionBD.question_id >= min_question_id,
                         QuestionBD.question_id <= max_question_id,
                        )
                    ).order_by(
                            QuestionBD.question_id.desc()
                            )
        try:
            async with self.session.begin():
                rezult = await self.session.execute(query)
                rezult = rezult.scalars().all()
                if not rezult:
                    return None
        except sqlalchemy.exc.OperationalError:
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Ошибка связи с базой данных! "
                    )
        except sqlalchemy.exc.DBAPIError:
             raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Ошибка добавления в базу данных! "
                    )
        return rezult
    
    async def _QuestionsAddDb(self, questions_for_add: list[Question]) -> int:
        """
        Функция записывающая вопросы в БД.
        
        """
        questions = []
        for item in questions_for_add:
            questions.append(QuestionBD(**item.model_dump()))
            try:
                async with self.session.begin():
                    self.session.add_all(questions)
            except sqlalchemy.exc.DBAPIError:
                return None
        return None

    async def askQuestions(self, questions_num: AskQuestions) -> Question|None:
        """
        Функция записывает НОВЫЕ вопросы в базу данных после проверки на их наличие в БД. 
        
        """
        if  questions_num.questions_num <= 0 :
            raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Количество необходимых вопросов для сохранения должно быть больше 0! "
                    )
        number_question = questions_num.questions_num
        questions = []
        
        # Цикл проверки вопросов на их уникальность для записив нашу БД 
        while number_question:
            questions_from_url = await self._getQuestionsFromUrl(num = number_question)
            if not questions_from_url:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Что-то не так с удаленным сервером! "
                    )
            
            id_question = set()
            for item in questions_from_url:
                id_question.add(item['id'])
            
            questions_from_db = await self._getQuestionsIdsFromDb(
                                                                  min_question_id = min(id_question), 
                                                                  max_question_id = max(id_question),
                                                                  )

            if questions_from_db: 
                new_reqwest = id_question.difference(set(questions_from_db))
            else:
                new_reqwest = id_question
            
            if new_reqwest:
                questions.extend(
                                [questions_from_url[i] for i in range(len(questions_from_url)) \
                                if questions_from_url[i]['id'] in new_reqwest]
                                )
            number_question = number_question - len(new_reqwest)
        
        # Создание списка после сериализации данных и запись в БД
        questions_add_db = []
        for i in questions_from_url:
            questions_add_db.append(Question(**i))
        await self._QuestionsAddDb(questions_for_add = questions_add_db)

        return questions_add_db[:-2:-1] if questions_add_db else None
 