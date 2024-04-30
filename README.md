# Исполнение тестового задания для Python разработчика
#### В связи с затруднением запуска проекта на хостинге с использованием БД Postgres, была использована БД SQLite.  
#### PostgreSQL используется при запуске проекта локально
#### Деплой проекта на хостинге ![PythonAnyWhere](https://testingdatingapi.pythonanywhere.com/)
## Авторизация по номеру телефона:
#### Первый этап: отправка номера телефона
Метод: `POST`  
Адрес отправки запроса: ![https://testingdatingapi.pythonanywhere.com/user/send_reg_code/](https://testingdatingapi.pythonanywhere.com/user/send_reg_code/)  
Формат ввода данных:
```
{
    "phone_number": "8-9**-***-**-**"
}
```  
Ответ сервера: отправка 4-значного кода (вместо отправки sms, выдача кода реализована в формате ответа сервера).  
Формат ответа: 
```
{
    "reg_code": "****"
}
```  
#### Второй этап: отправка номера телефона с кодом
Метод: `POST`  
Адрес отправки запроса: ![https://testingdatingapi.pythonanywhere.com/user/send_access_token/](https://testingdatingapi.pythonanywhere.com/user/send_access_token/)  
Формат ввода данных:
```
{  
    "phone_number": "8-9**-***-**-**",  
    "reg_code": "****"  
}  
```
Ответ сервера: отправка `refresh` и `access` токенов  
Формат ответа: 
```
{
    "refresh": "*",
    "access": "*"
}
```
В дальнейшем, токены будут необходимы для получения доступа к остальному функционалу сервиса.  
## Реферальная система  
### Получение личного инвайт-кода
Личный инвайт-код пользователя выдается при первом просмотре профиля данного пользователя.  
Метод: `GET`  
Адрес отправки запроса: ![https://testingdatingapi.pythonanywhere.com/user/ID](https://testingdatingapi.pythonanywhere.com/user/1)  
Формат ответа:
```
{
    "phone_number": "*",
    "invite_code": "*",
    "invited_users": [],
    "strange_code": null
}
```
### Указание чужого 
