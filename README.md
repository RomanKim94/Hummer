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
    "phone_number": "8-9**-***-**-**" (номер телефона пользователя)
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
    "phone_number": "8-9**-***-**-**", (номер телефона пользователя)
    "reg_code": "****" (полученный 4-значный код)  
}  
```
Ответ сервера: отправка `refresh` и `access` токенов  
Формат ответа: 
```
{
    "refresh": "*", (refresh token)
    "access": "*" (access token)
}
```
## Реферальная система  
### Получение информации о пользователе  
Метод: `GET`  
Адрес отправки запроса: ![https://testingdatingapi.pythonanywhere.com/user/<phone_number>/](https://testingdatingapi.pythonanywhere.com/user/<phone_number>/)  
Вместо <phone_number> требуется указать номер телефона интересуемого пользователя.  
Также возможно указать вместо <phone_number> слово "me". В таком случае, ответ будет содержать информацию о текущем пользователе.
Формат ответа:
```
{
    "phone_number": "*", (номер телефона пользователя)
    "invite_code": "*", (инвайт-код пользователя)
    "invited_users": [], (список пользователей, использующих инвайт-код данного пользователя)
    "strange_code": null или "*" (null или введенный инвайт-код)
}
```
### Указание чужого инвайт-кода  
Ввод инвайт-кода доступен только после авторизации пользователя
Метод: `POST`  
Адрес отправки запроса: ![https://testingdatingapi.pythonanywhere.com/invite/set_code/](https://testingdatingapi.pythonanywhere.com/invite/set_code/)
Формат ввода данных:
```
{  
    "code": "*",
}  
```
Формат ответа, при успешном применении кода:  
```
{
    'result': 'Инвайт-код успешно применен'
}
```

