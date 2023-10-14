# junior
Комманда для создания и монтирования образа посредством Docker (запуск при установленном Docker и папки с загружнным репозиторием):
    docker-compose -f docker_compose.yml up

Сервис доступен по адресу:
    http://localhost:7050/docs

Пример запросов (через Swagger FastAPI):
Запрос: количество запрошенных вопросов 0 или отрицательное число:
{
  "questions_num": 0
}

Ответ:
Cod 400, Error: Bad Request, 
{ "detail": "Количество необходимых вопросов для сохранения должно быть больше 0! " }

Запрос: количество запрошенных вопросов больше 0:
{
  "questions_num": 3
}
Ответ:
Cod 200

Response body:
{
  "question_id": 119088,
  "question": "The Sienna",
  "answer": "Toyota",
  "created_at": "2022-12-30T19:53:09.012000Z"
}
