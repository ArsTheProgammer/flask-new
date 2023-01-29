import sqlite3

create_table = """
CREATE TABLE IF NOT EXISTS quotes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
author TEXT NOT NULL,
text TEXT NOT NULL
);
"""
# Подключение в БД
connection = sqlite3.connect("test.db")

# Создаем cursor, он позволяет делать SQL-запросы
cursor = connection.cursor()

# Выполняем запрос:
cursor.execute(create_table)

# Фиксируем выполнение(транзакцию)
connection.commit()

# Закрыть курсор:
cursor.close()

# Закрыть соединение:
connection.close()


create_quotes = """
INSERT INTO
quotes (author,text)
VALUES
('Rick Cook', 'Программирование сегодня — это гонка разработчиков программ'),
('Waldi Ravens', 'Программирование на С похоже на быстрые танцы на только c мечами в руках'),
('Alan J. Perlis', 'Низкоуровневый язык — это когда требуется внимание к вещам, которые никак не связаны с программами на этом языке.'),
('Thomas C. Gale', 'В хорошем дизайне добавление чего-то стоит дешевле, чем сама эта вещь.');
"""

# Подключение в БД
connection = sqlite3.connect("test.db")

# Создаем cursor, он позволяет делать SQL-запросы
cursor = connection.cursor()

# Выполняем запрос:
cursor.execute(create_quotes)

# Фиксируем выполнение(транзакцию)
connection.commit()

# Закрыть курсор:
cursor.close()

# Закрыть соединение:
connection.close()


select_quotes = "SELECT * from quotes"

# Подключение в БД
connection = sqlite3.connect("test.db")

# Создаем cursor, он позволяет делать SQL-запросы
cursor = connection.cursor()

# Выполняем запрос:
cursor.execute(select_quotes)

# Извлекаем результаты запроса
quotes = cursor.fetchall()
print(f"{quotes=}")

# Закрыть курсор:
cursor.close()

# Закрыть соединение:
connection.close()

