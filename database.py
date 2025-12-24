import pymysql


class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='12345',
        )
        self.setup_database()

    def setup_database(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "CREATE DATABASE IF NOT EXISTS furniture_store")
            cursor.execute("USE furniture_store")

            tables = [
                """
                CREATE TABLE IF NOT EXISTS Клиент (
                    idКлиент INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(30) NOT NULL,
                    телефон INT NOT NULL,
                    ФИО VARCHAR(99) NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Должность (
                    idДолжности INT AUTO_INCREMENT PRIMARY KEY,
                    Наименование VARCHAR(45) NOT NULL,
                    Оклад INT 
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Пароли (
                    idПароли INT AUTO_INCREMENT PRIMARY KEY,
                    Пароль VARCHAR(30) NOT NULL,
                    email VARCHAR(30) NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Сотрудники (
                    idСотрудника INT AUTO_INCREMENT PRIMARY KEY,
                    График_работы VARCHAR(20),
                    телефон INT,
                    Дата_рождения DATE,
                    Фамилия VARCHAR(45) NOT NULL,
                    Имя VARCHAR(45) NOT NULL,
                    Отчество VARCHAR(45),
                    Пароли_idПароли INT NOT NULL,
                    Должность_idДолжности INT NOT NULL,
                    FOREIGN KEY (Пароли_idПароли) REFERENCES Пароли(idПароли),
                    FOREIGN KEY (Должность_idДолжности) REFERENCES Должность(idДолжности)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Категория (
                    idКатегории INT AUTO_INCREMENT PRIMARY KEY,
                    Наименование VARCHAR(45) NOT NULL,
                    Надценка INT NOT NULL 
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Материал (
                    idМатериал INT AUTO_INCREMENT PRIMARY KEY,
                    Наименование VARCHAR(45) NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Цвет (
                    idЦвет INT AUTO_INCREMENT PRIMARY KEY,
                    Наименование VARCHAR(45) NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS ДопУслуги (
                    idДопУслуги INT AUTO_INCREMENT PRIMARY KEY,
                    вид VARCHAR(45) NOT NULL,
                    стоимость VARCHAR(45) NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Скидка (
                    idСкидка INT AUTO_INCREMENT PRIMARY KEY,
                    Наименование VARCHAR(45) NOT NULL,
                    Процент INT NOT NULL
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Мебель (
                    idМебель VARCHAR(10) PRIMARY KEY,
                    Наименование VARCHAR(45) NOT NULL,
                    Производитель VARCHAR(45) NOT NULL,
                    Габариты VARCHAR(30) NOT NULL,
                    Вес INT NOT NULL,
                    Количество INT NOT NULL,
                    Цвет_idЦвет INT NOT NULL,
                    Категория_idКатегории INT NOT NULL,
                    Материал_idМатериал INT NOT NULL,
                    FOREIGN KEY (Цвет_idЦвет) REFERENCES Цвет(idЦвет),
                    FOREIGN KEY (Категория_idКатегории) REFERENCES Категория(idКатегории),
                    FOREIGN KEY (Материал_idМатериал) REFERENCES Материал(idМатериал)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Поставки (
                    idПоставки INT AUTO_INCREMENT PRIMARY KEY,
                    Дата DATE NOT NULL,
                    Количество INT NOT NULL,
                    Себестоимость INT NOT NULL,
                    Тип_операции VARCHAR(10) NOT NULL,
                    Мебель_idМебель VARCHAR(10) NOT NULL,
                    FOREIGN KEY (Мебель_idМебель) REFERENCES Мебель(idМебель)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS Заказ (
                    idЗаказ INT AUTO_INCREMENT PRIMARY KEY,
                    Дата DATE NOT NULL,
                    Статус VARCHAR(10) NOT NULL,                    
                    Скидка_idСкидка INT,
                    Клиент_idКлиент INT NOT NULL,
                    Сотрудники_idСотрудника INT NOT NULL,
                    FOREIGN KEY (Скидка_idСкидка) REFERENCES Скидка(idСкидка),
                    FOREIGN KEY (Клиент_idКлиент) REFERENCES Клиент(idКлиент),
                    FOREIGN KEY (Сотрудники_idСотрудника) REFERENCES Сотрудники(idСотрудника)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS ПозицииВзаказе (
                    idПозицииВзаказе INT AUTO_INCREMENT PRIMARY KEY,
                    Количество INT NOT NULL,
                    Мебель_idМебель VARCHAR(10) NOT NULL,
                    Заказ_idЗаказ INT NOT NULL,
                    FOREIGN KEY (Мебель_idМебель) REFERENCES Мебель(idМебель),
                    FOREIGN KEY (Заказ_idЗаказ) REFERENCES Заказ(idЗаказ)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS ДопУслуги_has_Заказ (
                    ДопУслуги_idДопУслуги INT,
                    Заказ_idЗаказ INT,
                    PRIMARY KEY (ДопУслуги_idДопУслуги, Заказ_idЗаказ),
                    FOREIGN KEY (ДопУслуги_idДопУслуги) REFERENCES ДопУслуги(idДопУслуги),
                    FOREIGN KEY (Заказ_idЗаказ) REFERENCES Заказ(idЗаказ)
                )
                """
            ]

            for table_query in tables:
                try:
                    cursor.execute(table_query)
                except Exception as e:
                    print(f"Ошибка при создании таблицы: {e}")

            self.insert_data(cursor)
            self.connection.commit()

    def insert_data(self, cursor):
        cursor.execute("SELECT COUNT(*) FROM Должность")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO Должность (Наименование, Оклад) VALUES "
                           "('Администратор', 80000), "
                           "('Продавец', 35000), "
                           "('Кладовщик', 35000), "
                           "('Бухгалтер', 30000)")

        cursor.execute("SELECT COUNT(*) FROM Категория")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO Категория (Наименование, Надценка) VALUES "
                           "('Диваны', 30), "
                           "('Стулья', 20), "
                           "('Столы', 25), "
                           "('Шкафы', 35), "
                           "('Кровати', 40)")

        cursor.execute("SELECT COUNT(*) FROM Материал")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO Материал (Наименование) VALUES "
                           "('Дерево'), ('Металл'), ('Стекло'), ('Кожа'), ('Ткань'), ('Пластик')")

        # Проверяем таблицу Цвет
        cursor.execute("SELECT COUNT(*) FROM Цвет")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO Цвет (Наименование) VALUES "
                           "('Белый'), ('Черный'), ('Коричневый'), ('Серый'), ('Бежевый'), ('Красный')")

        cursor.execute("SELECT COUNT(*) FROM ДопУслуги")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO ДопУслуги (вид, стоимость) VALUES "
                           "('Доставка', 1500), "
                           "('Сборка', 2000)")

        cursor.execute("SELECT COUNT(*) FROM Скидка")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute("INSERT INTO Скидка (Наименование, Процент) VALUES "
                           "('Празничная', 10), "
                            "('Распродажа', 10), "
                           "('Сотрудникам', 5), "
                           "('Для постоянных клиентов', 15)")

    def execute_query(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute("USE furniture_store")
            cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.lastrowid

    def execute_many(self, query, params_list):
        with self.connection.cursor() as cursor:
            cursor.execute("USE furniture_store")
            cursor.executemany(query, params_list)
            self.connection.commit()
            return cursor.rowcount

    def close(self):
        if self.connection:
            self.connection.close()

db = Database()