# 🧩 Установщик модов для Minecraft

Утилита для автоматической установки модов в Minecraft с использованием Google Таблиц.

---

## 🚀 Возможности

- Загрузка модов с **Modrinth** и **CurseForge**
- Поддержка как клиентских, так и серверных модов
- Гибкая настройка через `config.txt`
- Простая интеграция с Google Таблицами

---

## 📋 Подготовка Google Таблицы

Создайте таблицу с модами, содержащую следующие столбцы:

- `client-name` — имя клиентского мода  
- `client-url` — ссылка на клиентский мод (Modrinth или CurseForge)  
- `server-name` — имя серверного мода  
- `server-url` — ссылка на серверный мод  

> Дополнительные столбцы допускаются, но не обязательны.

Ваша таблица должна выглядеть примерно так:

| client-name      | client-url                            | server-name      | server-url                            |
|------------------|---------------------------------------|------------------|---------------------------------------|
| mode1            | https://modrinth.com/mode1            | mode1            | https://modrinth.com/mode1            |
| client-side-mode | https://modrinth.com/client-side-mode | server-side-mode | https://modrinth.com/server-side-mode | 

---

## ⚙️ Настройка

В файле `config.txt` укажите значения переменных окружения:

| Переменная             | Описание                                         |
|------------------------|--------------------------------------------------|
| `SHEET_ID`             | ID вашей Google Таблицы                          |
| `CURSEFORGE_API_KEY`   | API-ключ для доступа к CurseForge                |
| `MINECRAFT_VERSION`    | Версия Minecraft                                 |
| `MINECRAFT_MOD_LOADER` | Загрузчик модов (например, `forge` или `fabric`) |
| `DOWNLOAD_PATH`        | Путь к папке для загрузки модов                  |
| `DOWNLOAD_CLIENT`      | Загружать клиентские моды (`true` / `false`)     |
| `DOWNLOAD_SERVER`      | Загружать серверные моды (`true` / `false`)      |

---

## ▶️ Запуск

1. Убедитесь, что `config.txt` заполнен корректно.
2. Запустите программу.
3. Моды будут загружены в папки:  
   - `DOWNLOAD_PATH/client`  
   - `DOWNLOAD_PATH/server`
4. В случае ошибки повторите запуск — программа обработает недостающие моды повторно.

---

## 🛠️ Сборка проекта

### 🔧 Классический запуск

```shell
py -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
py source/main.py
```

### 📦 Сборка в исполняемый файл (.exe)

```shell
pyinstaller --onefile source/main.py --add-data config.txt:. --name install_mods --icon icon.ico
```
