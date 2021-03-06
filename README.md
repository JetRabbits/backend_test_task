# Тестовое задание
Должность back-end разработчика компании JetRabbits

[Документация Swagger](http://0.0.0.0/rest/v1/ui)

## Микро-сервис
1. Сервис служит для создания иерархии узлов
2. Узлы делятся по типам: директория, директория для публикации, файл, массив байт (видео streaming)
3. Один узел может быть связан с одним ресурсом: файл, массив байт (видео streaming)
4. Ресурсы в данном проекте образуют файловую систему на сервере: иерархия директорий под которыми располагаются файлы
5. Суть задачи: организовать CRUD операции, включая операции поиска и проверку прав на чтение и запись узлов

## Спецификация

`http://0.0.0.0/rest/v1/openapi.json`

## Ресурсы

### Узлы (рабочее API)

| HTTP | Ресурс | Тип | Аргументы | Описание |
|---|---|---|---|---|
| GET | [/rest/v1/nodes](http://0.0.0.0/rest/v1/nodes) | json | {JWT-token} | Получение всех узлов |
| GET | [/rest/v1/nodes/{id}/download](http://0.0.0.0/rest/v1/nodes/{id}/download) | json | - | Скачивание ресурса по ID узла |
| POST | [/rest/v1/nodes](http://0.0.0.0/rest/v1/nodes) | json | {JWT-token} | Создание или изменение всех узлов |
| POST | [/rest/v1/nodes/{id}/upload](http://0.0.0.0/rest/v1/nodes/{id}/upload) | json | {JWT-token} | Загрузка ресурса по ID узла |

### Узлы (разработать API)

| HTTP | Ресурс | Тип | Аргументы | Описание |
|---|---|---|---|---|
| GET | [/rest/v1/nodes/{id}](http://0.0.0.0/rest/v1/nodes/{id}) | json | {JWT-token} | Получение узла по ID |
| POST | [/rest/v1/nodes/search](http://0.0.0.0/rest/v1/nodes/search) | json | {JWT-token} | Поиск узлов включая сортировку и paging |
| DELETE | [/rest/v1/nodes/{id}](http://0.0.0.0/rest/v1/nodes/{id}) | json | {JWT-token} | Удаление узла по ID |

## FAQ

### Что такое JWT-token?

JSON Web Token (JWT) — это открытый стандарт (RFC 7519) для создания токенов доступа, основанный на формате JSON. Как правило, используется для передачи данных для аутентификации в клиент-серверных приложениях. Токены создаются сервером, подписываются секретным ключом и передаются клиенту, который в дальнейшем использует данный токен для подтверждения своей личности. Выдаётся перед началом тестового задания и действует 24 часа с момента генерации.