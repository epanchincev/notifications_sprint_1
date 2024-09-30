# Проектная работа 9 спринта

Ссылка на проект: 
https://github.com/epanchincev/notifications_sprint_1

## Что сделано в этом спринте
1. Создана инфраструктура для спринта| ./infra;
2. Создано апи для админки с уведомлениями| ./notifications_admin;
3. Создан сервис API реализующий добавление в очередь уведомлений| ./notifications_api;
4. Создан воркер рендеринга шаблонов| ./notification_processor;
5. Создан воркер отправки уведомлений| ./notifiactions_worker.


## Установка
### Клонируй репозиторий и перейди в директорию
```shell
git clone https://github.com/epanchincev/notifications_sprint_1.git
cd notifications_sprint_1
```
### Создай .env файлы
```shell
cp infra/.env.example infra/.env
cp notifications_admin/src/core/.env.example notifications_admin/src/core/.env
cp notifications_api/src/core/.env.example notifications_api/src/core/.env
cp notification_processor/src/core/.env.example notification_processor/src/core/.env
```
### Создай образы и запусти проект
```shell
make up
```

### Авторы
1. [@DBWtv](https://github.com/DBWtv)
2. [@epanchincev](https://github.com/epanchincev)
3. [@jokcik](https://github.com/jokcik)
4. [@tims0n17](http://github.com/tims0n17)

