from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from database import db


class AuthWindow(QWidget):
    user_authenticated = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.current_user = None
        self.is_first_admin = False
        self.init_ui()
        self.check_first_admin()

    def init_ui(self):
        self.setWindowTitle('Мебельный магазин - Вход')
        self.setFixedSize(350, 325)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel('Регистрация/авторизация')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)

        email_label = QLabel('e-mail:')
        email_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Введите ваш email')
        self.email_input.setStyleSheet("font-size: 12pt; padding: 8px;")
        layout.addWidget(self.email_input)

        password_label = QLabel('Пароль:')
        password_label.setStyleSheet("font-size: 12pt;")
        layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("font-size: 12pt; padding: 8px;")
        layout.addWidget(self.password_input)

        self.action_button = QPushButton('Завершить')
        self.action_button.setFixedHeight(45)
        self.action_button.clicked.connect(self.authenticate)
        layout.addWidget(self.action_button)

        self.setLayout(layout)

    def check_first_admin(self):
        query = """
        SELECT s.idСотрудника 
        FROM Сотрудники s
        JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
        WHERE d.Наименование = 'Администратор'
        LIMIT 1
        """

        admins = db.execute_query(query)

        if not admins:
            self.is_first_admin = True
            self.setWindowTitle('Регистрация администратора')
            self.action_button.setText('Зарегистрироваться')
        else:
            self.is_first_admin = False
            self.setWindowTitle('Авторизация')
            self.action_button.setText('Войти')

    def authenticate(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все поля')
            return

        if self.is_first_admin:
            self.register_admin(email, password)
        else:
            self.login_user(email, password)

    def register_admin(self, email: str, password_input: str):
        if '@' not in email and '.' not in email:
            QMessageBox.warning(self, 'Ошибка', 'Введите корректный email')
            return

        if len(password_input) < 6:
            QMessageBox.warning(self, 'Ошибка', 'Пароль должен содержать минимум 6 символов')
            return

        try:
            password_query = """
            INSERT INTO Пароли (email, Пароль) 
            VALUES (%s, %s)
            """
            db.execute_query(password_query, (email, password_input))

            get_password_id_query = "SELECT LAST_INSERT_ID()"
            password_id_result = db.execute_query(get_password_id_query)

            if not password_id_result:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось создать учетные данные')
                return

            password_id = password_id_result[0][0]

            position_query = "SELECT idДолжности FROM Должность WHERE Наименование = 'Администратор'"
            position_result = db.execute_query(position_query)
            position_id = position_result[0][0]

            if not position_id:
                QMessageBox.warning(self, 'Ошибка', 'Должность "Администратор" не найдена')
                return

            email_name = email.split('@')[0]

            from datetime import datetime

            birth_date = datetime.now().date().strftime('%Y-%m-%d')

            create_employee = """
            INSERT INTO Сотрудники 
            (Фамилия, Имя, Отчество, телефон, Дата_рождения, 
             Пароли_idПароли, Должность_idДолжности, График_работы)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            db.execute_query(create_employee, (
                "Администратор",
                "Системный",
                "",
                "0000000000",
                birth_date,
                password_id,
                position_id,
                "5/2"
            ))

            get_employee_id = "SELECT LAST_INSERT_ID()"
            employee_id_result = db.execute_query(get_employee_id)

            if not employee_id_result:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось создать сотрудника')
                return

            employee_id = employee_id_result[0][0]

            get_user = """
            SELECT 
                s.idСотрудника, 
                s.Фамилия, 
                s.Имя, 
                p.email,
                d.Наименование as Должность
            FROM Сотрудники s
            JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
            JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
            WHERE s.idСотрудника = %s
            """

            user_result = db.execute_query(get_user, (employee_id,))

            if not user_result:
                QMessageBox.warning(self, 'Ошибка', 'Не удалось получить данные пользователя')
                return

            user_data = user_result[0]
            self.current_user = {
                'id': user_data[0],
                'last_name': user_data[1],
                'first_name': user_data[2],
                'email': user_data[3],
                'role': user_data[4],
            }
            self.user_authenticated.emit(self.current_user)
            self.close()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка регистрации: {str(e)}\nТип: {type(e).__name__}')

    def login_user(self, email: str, password: str):
        try:
            query = """
            SELECT 
                s.idСотрудника, 
                s.Фамилия, 
                s.Имя, 
                p.email,
                d.Наименование as Должность
            FROM Сотрудники s
            JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
            JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
            WHERE p.email = %s AND p.Пароль = %s
            """

            user = db.execute_query(query, (email, password))

            if user:
                user_data = user[0]
                self.current_user = {
                    'id': user_data[0],
                    'last_name': user_data[1],
                    'first_name': user_data[2],
                    'email': user_data[3],
                    'role': user_data[4],
                }
                self.user_authenticated.emit(self.current_user)
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', 'Неверный email или пароль')

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка при входе: {str(e)}')