from fastapi import APIRouter, Depends
from models.customers import AskQuestions, QuestionShow
from services.customersservices import CustomerService

customer_operation_router = APIRouter(prefix='/customer', tags=['Customer'])

@customer_operation_router.post('/question', response_model=QuestionShow|None)
async def question(
    body: AskQuestions, 
    service: CustomerService = Depends(),
) -> QuestionShow|None:
    responze = await service.askQuestions(body)
    return QuestionShow(**responze[0].model_dump()) if responze else None