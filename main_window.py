from PyQt6.QtWidgets import (QButtonGroup, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QLineEdit, QPushButton,
                             QTableWidget, QTableWidgetItem,
                             QComboBox, QGroupBox, QMessageBox, QDialog,
                             QHeaderView, QFrame, QDateEdit,
                             QTextEdit, QCheckBox, QGridLayout,
                             QStackedWidget, QScrollArea)
from PyQt6.QtCore import Qt, QDate
from datetime import datetime
from database import db

class FurnitureDialog(QDialog):
    def __init__(self, parent=None, furniture_id=None, action_type=None):
        super().__init__(parent)
        self.furniture_id = furniture_id
        self.action_type = action_type

        title_map = {
            'edit': "Редактирование мебели",
            'supply': "Поставка мебели",
            'write_off': "Списание мебели"
        }

        title = title_map.get(action_type, "Добавление мебели") if not furniture_id else "Редактирование мебели"
        self.setWindowTitle(title)
        self.setFixedSize(500, 500)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        left_column = QVBoxLayout()
        left_column.setSpacing(15)

        right_column = QVBoxLayout()
        right_column.setSpacing(15)

        title_label = QLabel("Параметры мебели")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        name_label = QLabel("Наименование")
        name_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите название мебели")
        left_column.addWidget(self.name_input)

        category_label = QLabel("Категория")
        category_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(category_label)

        self.category_combo = QComboBox()
        self.category_combo.addItem("Выберите категорию")
        self.load_categories()
        left_column.addWidget(self.category_combo)

        material_label = QLabel("Материал")
        material_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(material_label)

        self.material_combo = QComboBox()
        self.material_combo.addItem("Выберите материал")
        self.load_materials()
        left_column.addWidget(self.material_combo)

        producer_label = QLabel("Производитель")
        producer_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(producer_label)

        self.producer_input = QLineEdit()
        self.producer_input.setPlaceholderText("Введите производителя")
        left_column.addWidget(self.producer_input)

        color_label = QLabel("Цвет")
        color_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(color_label)

        self.color_combo = QComboBox()
        self.color_combo.addItem("Выберите цвет")
        self.load_colors()
        right_column.addWidget(self.color_combo)

        quantity_label = QLabel("Количество")
        quantity_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(quantity_label)

        quantity_widget = QWidget()
        quantity_layout = QHBoxLayout()
        self.quantity_input = QLineEdit()
        self.quantity_input.setFixedWidth(80)
        quantity_layout.addWidget(self.quantity_input)
        quantity_layout.addWidget(QLabel("шт"))
        quantity_widget.setLayout(quantity_layout)
        right_column.addWidget(quantity_widget)

        price_label = QLabel("Цена")
        price_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(price_label)

        price_widget = QWidget()
        price_layout = QHBoxLayout()
        self.price_input = QLineEdit()
        self.price_input.setFixedWidth(80)
        price_layout.addWidget(self.price_input)
        price_layout.addWidget(QLabel("руб"))
        price_widget.setLayout(price_layout)
        right_column.addWidget(price_widget)

        q_label = QLabel("  ")
        q_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(q_label)
        qq_label = QLabel("  ")
        qq_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(qq_label)

        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column)

        layout.addLayout(main_layout)

        dimensions_widget = QWidget()
        dimensions_layout = QHBoxLayout()
        dimensions_layout.setSpacing(20)

        length_widget = QWidget()
        length_layout = QVBoxLayout()
        length_label = QLabel("Длина")
        length_label.setStyleSheet("font-weight: bold;")
        length_layout.addWidget(length_label, alignment=Qt.AlignmentFlag.AlignCenter)

        length_input_layout = QHBoxLayout()
        self.length_input = QLineEdit()
        self.length_input.setFixedWidth(50)
        length_input_layout.addWidget(self.length_input)
        length_input_layout.addWidget(QLabel("мм"))
        length_layout.addLayout(length_input_layout)
        length_widget.setLayout(length_layout)
        dimensions_layout.addWidget(length_widget)

        width_widget = QWidget()
        width_layout = QVBoxLayout()
        width_label = QLabel("Ширина")
        width_label.setStyleSheet("font-weight: bold;")
        width_layout.addWidget(width_label, alignment=Qt.AlignmentFlag.AlignCenter)

        width_input_layout = QHBoxLayout()
        self.width_input = QLineEdit()
        self.width_input.setFixedWidth(50)
        width_input_layout.addWidget(self.width_input)
        width_input_layout.addWidget(QLabel("мм"))
        width_layout.addLayout(width_input_layout)
        width_widget.setLayout(width_layout)
        dimensions_layout.addWidget(width_widget)

        height_widget = QWidget()
        height_layout = QVBoxLayout()
        height_label = QLabel("Высота")
        height_label.setStyleSheet("font-weight: bold;")
        height_layout.addWidget(height_label, alignment=Qt.AlignmentFlag.AlignCenter)

        height_input_layout = QHBoxLayout()
        self.height_input = QLineEdit()
        self.height_input.setFixedWidth(50)
        height_input_layout.addWidget(self.height_input)
        height_input_layout.addWidget(QLabel("мм"))
        height_layout.addLayout(height_input_layout)
        height_widget.setLayout(height_layout)
        dimensions_layout.addWidget(height_widget)

        weight_widget = QWidget()
        weight_layout = QVBoxLayout()
        weight_label = QLabel("Вес")
        weight_label.setStyleSheet("font-weight: bold;")
        weight_layout.addWidget(weight_label, alignment=Qt.AlignmentFlag.AlignCenter)

        weight_input_layout = QHBoxLayout()
        self.weight_input = QLineEdit()
        self.weight_input.setFixedWidth(50)
        weight_input_layout.addWidget(self.weight_input)
        weight_input_layout.addWidget(QLabel("кг"))
        weight_layout.addLayout(weight_input_layout)
        weight_widget.setLayout(weight_layout)
        dimensions_layout.addWidget(weight_widget)

        dimensions_widget.setLayout(dimensions_layout)
        layout.addWidget(dimensions_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setFixedWidth(100)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 11pt;
            }
        """)

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.setFixedWidth(100)
        self.btn_save.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 11pt;
            }
        """)

        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_save)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_furniture)
        self.btn_cancel.clicked.connect(self.reject)

        if self.furniture_id:
            self.load_furniture_data()

    def load_categories(self):
        query = "SELECT idКатегории, Наименование FROM Категория ORDER BY Наименование"
        result = db.execute_query(query)
        for row in result:
            self.category_combo.addItem(row[1], row[0])

    def load_materials(self):
        query = "SELECT idМатериал, Наименование FROM Материал ORDER BY Наименование"
        result = db.execute_query(query)
        for row in result:
            self.material_combo.addItem(row[1], row[0])

    def load_colors(self):
        query = "SELECT idЦвет, Наименование FROM Цвет ORDER BY Наименование"
        result = db.execute_query(query)
        for row in result:
            self.color_combo.addItem(row[1], row[0])

    def load_furniture_data(self):
        query = """
                            SELECT 
                                m.idМебель,
                                m.Наименование,
                                m.Категория_idКатегории,
                                m.Материал_idМатериал,
                                m.Производитель,
                                m.Цвет_idЦвет,
                                m.Габариты,
                                m.Вес,
                                m.Количество,
                                COALESCE((
                                    SELECT p.Себестоимость 
                                    FROM Поставки p 
                                    WHERE p.Мебель_idМебель = m.idМебель AND Тип_операции = 'Поставка'
                                    ORDER BY p.Дата DESC 
                                    LIMIT 1
                                ), 0) as последняя_себестоимость
                            FROM Мебель m
                            WHERE m.idМебель = %s
                            """
        result = db.execute_query(query, (self.furniture_id,))

        if result:
            row = result[0]

            self.name_input.setText(row[1] if row[1] else "")

            if row[2]:
                index = self.category_combo.findData(row[2])
                if index >= 0:
                    self.category_combo.setCurrentIndex(index)

            if row[3]:
                index = self.material_combo.findData(row[3])
                if index >= 0:
                    self.material_combo.setCurrentIndex(index)

            if row[5]:
                index = self.color_combo.findData(row[5])
                if index >= 0:
                    self.color_combo.setCurrentIndex(index)

            self.producer_input.setText(row[4] if row[4] else "")

            if row[6]:
                dimensions = row[6].split('x')
                if len(dimensions) >= 3:
                    self.length_input.setText(dimensions[0].strip())
                    self.width_input.setText(dimensions[1].strip())
                    self.height_input.setText(dimensions[2].strip())

            if row[7]:
                self.weight_input.setText(str(row[7]))

            if row[8]:
                self.quantity_input.setText(str(row[8]))

            if row[9]:
                self.price_input.setText(str(row[9]))

    def save_furniture(self):
        try:
            if self.action_type in ['edit', 'supply', 'write_off']:
                if not self.name_input.text().strip():
                    QMessageBox.warning(self,"Ошибка", "Введите наименование мебели!")
                    return

                name = self.name_input.text().strip()

                category_id = self.category_combo.currentData()
                material_id = self.material_combo.currentData()
                color_id = self.color_combo.currentData()

                if not category_id:
                    QMessageBox.warning(self, "Ошибка","Выберите категорию!")
                    return

                if not material_id:
                    QMessageBox.warning(self,"Ошибка", "Выберите материал!")
                    return

                if not color_id:
                    QMessageBox.warning(self, "Ошибка","Выберите цвет!")
                    return

                producer = self.producer_input.text().strip()
                if not producer:
                    QMessageBox.warning(self,"Ошибка", "Введите производителя!")
                    return

                length = self.length_input.text().strip()
                width = self.width_input.text().strip()
                height = self.height_input.text().strip()

                if not (length and width and height):
                    QMessageBox.warning(self, "Ошибка", "Заполните все поля габаритов!")
                    return

                try:
                    length_val = int(length)
                    width_val = int(width)
                    height_val = int(height)

                    if length_val < 0 or width_val < 0 or height_val < 0:
                        QMessageBox.warning(self, "Ошибка", "Габариты должны быть положительными числами!")
                        return

                    dimensions = f"{length_val}x{width_val}x{height_val}"

                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Габариты должны быть числами!")
                    return

                weight_text = self.weight_input.text().strip()
                if not weight_text:
                    QMessageBox.warning(self, "Ошибка", "Введите вес!")
                    self.weight_input.setFocus()
                    return

                try:
                    weight = float(weight_text)
                    if weight <= 0:
                        QMessageBox.warning(self, "Ошибка", "Вес должен быть положительным числом!")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Вес должен быть числом!")
                    return

                quantity_text = self.quantity_input.text().strip()
                if not quantity_text:
                    QMessageBox.warning(self, "Ошибка", "Введите количество!")
                    return

                try:
                    quantity = int(quantity_text)
                    if quantity <= 0:
                        QMessageBox.warning(self, "Ошибка", "Количество должно быть положительным!")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Количество должно быть целым числом!")
                    return

                current_date = datetime.now().date()

            if self.action_type == 'edit':
                price_text = self.price_input.text().strip()
                if not price_text:
                    QMessageBox.warning(self, "Ошибка", "Введите цену")
                    return

                try:
                    price = int(price_text)
                    if price < 0:
                        QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной!")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Цена должна быть числом!")
                    return

                self.edit_furniture(
                    name, category_id, material_id, color_id, producer,
                    dimensions, weight, quantity
                )

            elif self.action_type == 'supply':
                price_text = self.price_input.text().strip()
                if not price_text:
                    QMessageBox.warning(self, "Ошибка", "Введите цену")
                    return

                try:
                    price = int(price_text)
                    if price < 0:
                        QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной!")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Цена должна быть числом!")
                    return

                self.supply_furniture(name, category_id, material_id, color_id, producer,
                                      dimensions, weight, quantity, price, current_date)

            elif self.action_type == 'write_off':
                if self.furniture_id:
                    cost_query = """
                           SELECT Себестоимость 
                           FROM Поставки 
                           WHERE Мебель_idМебель = %s 
                           ORDER BY Дата DESC 
                           LIMIT 1
                           """
                    cost_result = db.execute_query(cost_query, (self.furniture_id,))
                    price = cost_result[0][0] if cost_result and cost_result[0][0] else 0
                else:
                    price_text = self.price_input.text().strip()
                    if price_text:
                        try:
                            price = int(price_text)
                        except ValueError:
                            price = 0
                    else:
                        price = 0


                self.write_off_furniture(name, category_id, material_id, color_id, producer,
                                         dimensions, weight, quantity, price, current_date)

        except Exception as e:
            QMessageBox.critical(self,"Ошибка",  f"Ошибка сохранения: {str(e)}")

    def edit_furniture(self, name, category_id, material_id, color_id, producer, dimensions, weight, quantity):
        try:
            new_price_text = self.price_input.text().strip()
            new_price = None

            if new_price_text:
                try:
                    new_price = float(new_price_text)
                    if new_price < 0:
                        QMessageBox.warning(self, "Ошибка", "Цена не может быть отрицательной!")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Ошибка", "Цена должна быть числом!")
                    return

            update_furniture_query = """
            UPDATE Мебель 
            SET Наименование = %s,
                Категория_idКатегории = %s,
                Материал_idМатериал = %s,
                Цвет_idЦвет = %s,
                Производитель = %s,
                Габариты = %s,
                Вес = %s,
                Количество = %s
            WHERE idМебель = %s
            """

            db.execute_query(update_furniture_query, (
                name, category_id, material_id, color_id,
                producer, dimensions, weight, quantity, self.furniture_id
            ))

            if new_price is not None and self.furniture_id:
                last_supply_query = """
                SELECT idПоставки 
                FROM Поставки 
                WHERE Мебель_idМебель = %s 
                  AND Тип_операции = 'Поставка'  
                ORDER BY Дата DESC, idПоставки DESC 
                LIMIT 1
                """
                last_supply_result = db.execute_query(last_supply_query, (self.furniture_id,))

                if last_supply_result and len(last_supply_result) > 0:
                    last_supply_id = last_supply_result[0][0]

                    update_supply_query = """
                    UPDATE Поставки 
                    SET Себестоимость = %s
                    WHERE idПоставки = %s
                    """
                    db.execute_query(update_supply_query, (new_price, last_supply_id))

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при изменении: {str(e)}")

    def supply_furniture(self, name, category_id, material_id, color_id, producer, dimensions, weight, quantity, price, current_date):
        try:
            find_query = """
            SELECT idМебель, Количество 
            FROM Мебель 
            WHERE Наименование = %s
              AND Категория_idКатегории = %s
              AND Материал_idМатериал = %s
              AND Цвет_idЦвет = %s
              AND Производитель = %s
              AND Габариты = %s 
              AND Вес = %s 
            LIMIT 1
            """

            result = db.execute_query(find_query, (
                name, category_id, material_id, color_id, producer,dimensions, weight))

            if result:
                furniture_id = result[0][0]
                current_quantity = result[0][1] or 0
                new_quantity = current_quantity + quantity

                update_query = "UPDATE Мебель SET Количество = %s WHERE idМебель = %s"
                db.execute_query(update_query, (new_quantity, furniture_id))

            else:
                count_query = "SELECT COUNT(*) FROM Мебель"
                count_result = db.execute_query(count_query)
                next_number = (count_result[0][0] + 1) if count_result else 1
                furniture_id = f"{next_number:06d}"

                insert_query = """
                INSERT INTO Мебель 
                (idМебель, Наименование, Категория_idКатегории, Материал_idМатериал,
                 Цвет_idЦвет, Производитель, Габариты, Вес, Количество)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                db.execute_query(insert_query, (
                    furniture_id, name, category_id, material_id, color_id,
                    producer, dimensions, weight, quantity))

                new_quantity = quantity

            supply_query = """
            INSERT INTO Поставки 
            (Дата, Количество, Себестоимость, Мебель_idМебель, Тип_операции)
            VALUES (%s, %s, %s, %s, %s)
            """

            db.execute_query(supply_query, (
                current_date, quantity, price, furniture_id, "Поставка"
            ))

            self.accept()

        except Exception as e:
            QMessageBox.critical(self,"Ошибка", f"Ошибка при оформлении поставки: {str(e)}")

    def write_off_furniture(self, name, category_id, material_id, color_id, producer, dimensions, weight, quantity,price, current_date):
        try:
            find_query = """
            SELECT idМебель, Количество 
            FROM Мебель 
            WHERE Наименование = %s
              AND Категория_idКатегории = %s
              AND Материал_idМатериал = %s
              AND Цвет_idЦвет = %s
              AND Производитель = %s
              AND Габариты = %s 
              AND Вес = %s 
            LIMIT 1
            """

            result = db.execute_query(find_query, (
                name, category_id, material_id, color_id, producer,
                dimensions, weight
            ))

            if not result:
                QMessageBox.warning(self, "Ошибка", "Такая мебель не найдена в каталоге! Списание невозможно.")
                return

            furniture_id = result[0][0]
            current_quantity = result[0][1] or 0

            if current_quantity < quantity:
                QMessageBox.warning(self, "Ошибка",
                                    f"Недостаточно товара для списания!\n"
                                    f"Текущее количество: {current_quantity} шт.\n"
                                    f"Пытаетесь списать: {quantity} шт.")
                return

            new_quantity = current_quantity - quantity

            update_query = "UPDATE Мебель SET Количество = %s WHERE idМебель = %s"
            db.execute_query(update_query, (new_quantity, furniture_id))

            supply_query = """
            INSERT INTO Поставки 
            (Дата, Количество, Себестоимость, Мебель_idМебель, Тип_операции)
            VALUES (%s, %s, %s, %s, %s)
            """

            db.execute_query(supply_query, (
                current_date, quantity, price, furniture_id, "Списание"
            ))

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при списании: {str(e)}")

class EmployeeDialog(QDialog):
    def __init__(self, parent=None, employee_id=None):
        super().__init__(parent)
        self.employee_id = employee_id
        self.setWindowTitle("Добавление сотрудника" if not employee_id else "Изменение сотрудника")
        self.setFixedSize(500, 500)
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        left_column = QVBoxLayout()
        left_column.setSpacing(15)

        right_column = QVBoxLayout()
        right_column.setSpacing(15)

        title_label = QLabel("Добавление сотрудника" if not self.employee_id else "Изменение сотрудника")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold;")

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)

        surname_label = QLabel("Фамилия")
        surname_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(surname_label)

        self.surname_input = QLineEdit()
        left_column.addWidget(self.surname_input)

        name_label = QLabel("Имя")
        name_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(name_label)

        self.name_input = QLineEdit()
        left_column.addWidget(self.name_input)

        patronymic_label = QLabel("Отчество")
        patronymic_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(patronymic_label)

        self.patronymic_input = QLineEdit()
        left_column.addWidget(self.patronymic_input)

        phone_label = QLabel("Телефон")
        phone_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(phone_label)

        self.phone_input = QLineEdit()
        left_column.addWidget(self.phone_input)

        email_label = QLabel("Email")
        email_label.setStyleSheet("font-weight: bold;")
        left_column.addWidget(email_label)

        self.email_input = QLineEdit()
        left_column.addWidget(self.email_input)

        schedule_label = QLabel("График работы")
        schedule_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(schedule_label)

        self.schedule_input = QLineEdit()
        right_column.addWidget(self.schedule_input)

        birth_date_label = QLabel("Дата рождения")
        birth_date_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(birth_date_label)

        self.birth_date_input = QDateEdit()
        self.birth_date_input.setCalendarPopup(True)
        self.birth_date_input.setDate(QDate(2025, 1, 1))
        right_column.addWidget(self.birth_date_input)

        position_label = QLabel("Должность")
        position_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(position_label)

        self.position_combo = QComboBox()
        self.position_combo.addItem("Выберите должность")
        self.load_positions()
        self.position_combo.currentIndexChanged.connect(self.update_salary_from_position)
        right_column.addWidget(self.position_combo)

        salary_label = QLabel("Оклад")
        salary_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(salary_label)

        salary_widget = QWidget()
        salary_layout = QHBoxLayout()
        self.salary_input = QLineEdit()
        self.salary_input.setFixedWidth(80)
        self.salary_input.setReadOnly(True)
        salary_layout.addWidget(self.salary_input)
        salary_layout.addWidget(QLabel("руб"))
        salary_widget.setLayout(salary_layout)
        right_column.addWidget(salary_widget)

        password_label = QLabel("Пароль")
        password_label.setStyleSheet("font-weight: bold;")
        right_column.addWidget(password_label)

        self.password_input = QLineEdit()
        right_column.addWidget(self.password_input)

        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column)

        layout.addLayout(main_layout)

        button_widget = QWidget()
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.btn_cancel = QPushButton("Отмена")
        self.btn_cancel.setFixedWidth(100)
        self.btn_cancel.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 11pt;
            }
        """)

        self.btn_save = QPushButton("Сохранить")
        self.btn_save.setFixedWidth(100)
        self.btn_save.setStyleSheet("""
            QPushButton {
                padding: 8px;
                font-size: 11pt;
            }
        """)

        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_save)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_employee)
        self.btn_cancel.clicked.connect(self.reject)

        if self.employee_id:
            self.load_employee_data()

    def load_positions(self):
        try:
            query = "SELECT idДолжности, Наименование, Оклад FROM Должность ORDER BY Наименование"
            result = db.execute_query(query)
            for row in result:
                display_text = f"{row[1]}"
                self.position_combo.addItem(display_text, (row[0], row[2]))
        except Exception as e:
            print(f"Ошибка загрузки должностей: {e}")

    def update_salary_from_position(self, index):
        if index > 0:
            data = self.position_combo.currentData()
            if data:
                position_id, salary = data
                self.salary_input.setText(str(salary))
        else:
            self.salary_input.clear()

    def load_employee_data(self):
        try:
            query = """
            SELECT 
                s.Фамилия,
                s.Имя,
                s.Отчество,
                s.Должность_idДолжности,
                s.телефон,
                p.email,
                p.Пароль,  
                s.Дата_рождения,
                s.График_работы,
                d.Оклад
            FROM Сотрудники s
            LEFT JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
            LEFT JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
            WHERE s.idСотрудника = %s
            """
            result = db.execute_query(query, (self.employee_id,))

            if result:
                row = result[0]

                self.surname_input.setText(row[0] if row[0] else "")
                self.name_input.setText(row[1] if row[1] else "")
                self.patronymic_input.setText(row[2] if row[2] else "")

                if row[3]:
                    for i in range(self.position_combo.count()):
                        data = self.position_combo.itemData(i)
                        if data and data[0] == row[3]:
                            self.position_combo.setCurrentIndex(i)
                            break

                self.phone_input.setText(str(row[4]) if row[4] else "")
                self.email_input.setText(row[5] if row[5] else "")

                if row[6]:
                    self.password_input.setText(row[6])

                if row[7]:
                    date = QDate.fromString(str(row[7]), "yyyy-MM-dd")
                    if date.isValid():
                        self.birth_date_input.setDate(date)

                self.schedule_input.setText(row[8] if row[8] else "")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")

    def save_employee(self):
        try:
            if not self.surname_input.text().strip():
                QMessageBox.warning(self, "Ошибка", "Введите фамилию сотрудника!")
                return

            if not self.name_input.text().strip():
                QMessageBox.warning(self, "Ошибка", "Введите имя сотрудника!")
                return

            surname = self.surname_input.text().strip()
            name = self.name_input.text().strip()
            patronymic = self.patronymic_input.text().strip()

            position_data = self.position_combo.currentData()
            if not position_data:
                QMessageBox.warning(self, "Ошибка", "Выберите должность!")
                return

            position_id = position_data[0]
            salary = position_data[1]

            phone = self.phone_input.text().strip()
            if not phone:
                QMessageBox.warning(self, "Ошибка", "Введите телефон!")
                return
            try:
                phone_int = int(phone)
            except ValueError:
                QMessageBox.warning(self, "Ошибка", "Телефон должен содержать только цифры!")
                return

            email = self.email_input.text().strip()
            if not email:
                QMessageBox.warning(self, "Ошибка", "Введите email!")
                return

            if '@' not in email or '.' not in email:
                QMessageBox.warning(self, 'Ошибка', 'Введите корректный email (должен содержать @ и домен)')
                return

            check_email_query = """
                        SELECT COUNT(*) FROM Сотрудники s
                        JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
                        WHERE p.email = %s
                        """
            result = db.execute_query(check_email_query, (email,))

            if result and result[0][0] > 0:
                QMessageBox.warning(self, "Ошибка",
                                    "Этот email уже используется другим сотрудником!\n"
                                    "Пожалуйста, введите другой email.")
                return

            birth_date = self.birth_date_input.date().toString("yyyy-MM-dd")

            schedule = self.schedule_input.text().strip()
            if not schedule:
                QMessageBox.warning(self, "Ошибка", "Введите график работы!")
                return

            password = self.password_input.text().strip()
            if not password:
                QMessageBox.warning(self, "Ошибка","Введите пароль!")
                return
            if len(password) < 6:
                QMessageBox.warning(self,"Ошибка", "Пароль должен быть не менее 6 символов!")
                return

            if self.employee_id:
                check_password_query = """
                        SELECT Пароли_idПароли FROM Сотрудники WHERE idСотрудника = %s
                        """
                result = db.execute_query(check_password_query, (self.employee_id,), fetch=True)

                password_id = result[0][0] if result and result[0][0] else None

                if password_id:
                    password_update_query = """
                            UPDATE Пароли 
                            SET email = %s, Пароль = %s
                            WHERE idПароли = %s
                            """
                    db.execute_query(password_update_query, (email, password, password_id))


                query = """
                            UPDATE Сотрудники 
                            SET Фамилия = %s,
                                Имя = %s,
                                Отчество = %s,
                                Должность_idДолжности = %s,
                                телефон = %s,
                                Дата_рождения = %s,
                                График_работы = %s,
                                Пароли_idПароли = %s
                            WHERE idСотрудника = %s
                        """

                db.execute_query(query, (
                    surname, name, patronymic, position_id, phone_int,
                    birth_date, schedule, password_id, self.employee_id
                ))

            else:
                password_insert_query = """
                        INSERT INTO Пароли (Пароль, email) 
                        VALUES (%s, %s)
                        """
                db.execute_query(password_insert_query, (password,email ))
                get_last_id_query = "SELECT LAST_INSERT_ID()"
                result = db.execute_query(get_last_id_query)
                password_id = result

                query = """
                            INSERT INTO Сотрудники 
                            (Фамилия, Имя, Отчество, Должность_idДолжности, телефон, 
                             Дата_рождения, График_работы, Пароли_idПароли)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """

                db.execute_query(query, (
                    surname, name, patronymic, position_id, phone_int,
                    birth_date, schedule, password_id))

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.selected_employee_id = None
        self.catalog_data_cash = []
        self.cart_data = []
        self.all_catalog_data = []
        self.current_catalog_filters = {}
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Информационная система мебельного магазина')
        self.setGeometry(100, 100, 1400, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        nav_panel = QFrame()
        nav_panel.setFixedWidth(200)
        nav_panel.setStyleSheet("background-color: #f0f0f0; border-right: 1px solid #ccc;")
        nav_layout = QVBoxLayout()

        self.btn_catalog = self.create_nav_button("Каталог", True)
        self.btn_supplies = self.create_nav_button("Поставки", False)
        self.btn_orders = self.create_nav_button("Заказы", False)
        self.btn_clients = self.create_nav_button("Клиенты", False)
        self.btn_cash = self.create_nav_button("Касса", False)
        self.btn_employees = self.create_nav_button("Сотрудники", False)
        self.btn_reports = self.create_nav_button("Отчёты", False)

        nav_layout.addWidget(self.btn_catalog)
        nav_layout.addWidget(self.btn_supplies)
        nav_layout.addWidget(self.btn_orders)
        nav_layout.addWidget(self.btn_clients)
        nav_layout.addWidget(self.btn_cash)
        nav_layout.addWidget(self.btn_employees)
        nav_layout.addWidget(self.btn_reports)

        nav_layout.addStretch()
        nav_panel.setLayout(nav_layout)
        main_layout.addWidget(nav_panel)

        self.work_area = QStackedWidget()
        main_layout.addWidget(self.work_area)

        self.create_catalog_page()
        self.create_supplies_page()
        self.create_orders_page()
        self.create_clients_page()
        self.create_cash_page()
        self.create_employees_page()
        self.create_reports_page()

        self.check_user_access()
        central_widget.setLayout(main_layout)

        self.btn_catalog.clicked.connect(lambda: self.show_page(0))
        self.btn_supplies.clicked.connect(lambda: self.show_page(1))
        self.btn_orders.clicked.connect(lambda: self.show_page(2))
        self.btn_clients.clicked.connect(lambda: self.show_page(3))
        self.btn_cash.clicked.connect(lambda: self.show_page(4))
        self.btn_employees.clicked.connect(lambda: self.show_page(5))
        self.btn_reports.clicked.connect(lambda: self.show_page(6))

    def create_nav_button(self, text, is_active=False):
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        if is_active:
            btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2c3e50;
                        color: white;
                        border: none;
                        text-align: left;
                        padding-left: 20px;
                        font-size: 12pt;
                        font-weight: bold;
                    }
                """)
        else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #333;
                        border: none;
                        text-align: left;
                        padding-left: 20px;
                        font-size: 12pt;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
        return btn

    def check_user_access(self):
        role = self.user_data.get('role', 'employee')

        if role == 'Администратор':
            self.show_page(0)
            return

        if role == 'Кладовщик':
            self.btn_catalog.setVisible(False)
            self.btn_orders.setVisible(False)
            self.btn_clients.setVisible(False)
            self.btn_cash.setVisible(False)
            self.btn_employees.setVisible(False)
            self.btn_reports.setVisible(False)
            self.show_page(1)
            return

        if role == 'Продавец':
            self.btn_catalog.setVisible(False)
            self.btn_supplies.setVisible(False)
            self.btn_orders.setVisible(False)
            self.btn_clients.setVisible(False)
            self.btn_employees.setVisible(False)
            self.btn_reports.setVisible(False)
            self.show_page(4)
            return

        if role == 'Бухгалтер':
            self.btn_catalog.setVisible(False)
            self.btn_supplies.setVisible(False)
            self.btn_orders.setVisible(False)
            self.btn_clients.setVisible(False)
            self.btn_employees.setVisible(False)
            self.btn_cash.setVisible(False)
            self.show_page(6)
            return

    def show_page(self, index):
        if index < 0 or index >= self.work_area.count():
            index = 0

        self.work_area.setCurrentIndex(index)
        buttons = [self.btn_catalog, self.btn_supplies, self.btn_orders,
                   self.btn_clients, self.btn_cash, self.btn_employees, self.btn_reports]
        for i, btn in enumerate(buttons):
            if i == index:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #2c3e50;
                        color: white;
                        border: none;
                        text-align: left;
                        padding-left: 20px;
                        font-size: 12pt;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #333;
                        border: none;
                        text-align: left;
                        padding-left: 20px;
                        font-size: 12pt;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                    }
                """)
    #Каталог
    def create_catalog_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        top_panel = QHBoxLayout()

        search_label = QLabel("Поиск:")
        search_label.setFixedWidth(50)
        top_panel.addWidget(search_label)

        self.catalog_search = QLineEdit()
        self.catalog_search.setFixedHeight(30)
        self.catalog_search.setFixedWidth(950)
        top_panel.addWidget(self.catalog_search)

        self.btn_search_catalog = QPushButton("Поиск")
        self.btn_search_catalog.setFixedHeight(30)
        top_panel.addWidget(self.btn_search_catalog)

        self.btn_modify_furniture = QPushButton("Изменить")
        self.btn_modify_furniture.setFixedWidth(100)
        self.btn_modify_furniture.setFixedHeight(30)
        self.btn_modify_furniture.setEnabled(False)
        top_panel.addWidget(self.btn_modify_furniture)

        top_panel.addStretch()

        layout.addLayout(top_panel)

        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(1)

        column_widths = [120, 225, 120, 120, 150, 100, 125, 80, 100, 100]

        for i in range(10):
            header_widget = QWidget()
            header_widget.setFixedWidth(column_widths[i])
            header_widget_layout = QVBoxLayout(header_widget)
            header_widget_layout.setContentsMargins(1, 1, 1, 1)
            header_widget_layout.setSpacing(0)

            if i == 0:
                label = QLabel("Артикул")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 1:
                label = QLabel("Наименование")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)


            elif i == 2:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Категория")
                combo.currentTextChanged.connect(self.filter_catalog_by_category)
                combo.setStyleSheet("""
                        QComboBox {
                            font-weight: bold;
                            padding: 4px;
                            background-color: #f0f0f0;
                            border: 1px solid #d0d0d0;
                        }
                    """)
                self.category_filter_combo_catalog_page_main = combo
                header_widget_layout.addWidget(combo)
            elif i == 3:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Материал")
                combo.currentTextChanged.connect(self.filter_catalog_by_material)
                combo.setStyleSheet("""
                        QComboBox {
                            font-weight: bold;
                            padding: 4px;
                            background-color: #f0f0f0;
                            border: 1px solid #d0d0d0;
                        }
                    """)
                self.material_filter_combo_catalog_page = combo
                header_widget_layout.addWidget(combo)
            elif i == 4:
                label = QLabel("Производитель")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)


            elif i == 5:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Цвет")
                combo.currentTextChanged.connect(self.filter_catalog_by_color)
                combo.setStyleSheet("""
                        QComboBox {
                            font-weight: bold;
                            padding: 4px;
                            background-color: #f0f0f0;
                            border: 1px solid #d0d0d0;
                        }
                    """)
                self.color_filter_combo_catalog_page = combo
                header_widget_layout.addWidget(combo)

            elif i == 6:
                label = QLabel("Габариты")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 7:
                label = QLabel("Вес")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 8:
                label = QLabel("Количество")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 9:
                label = QLabel("Цена")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            header_layout.addWidget(header_widget)

        self.catalog_table = QTableWidget()
        self.catalog_table.setColumnCount(10)

        for i, width in enumerate(column_widths):
            self.catalog_table.setColumnWidth(i, width)

        self.catalog_table.horizontalHeader().setVisible(False)
        self.catalog_table.verticalHeader().setVisible(False)

        self.catalog_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.catalog_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.catalog_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.catalog_table.setAlternatingRowColors(True)

        layout.addWidget(header_container)
        layout.addWidget(self.catalog_table)

        page.setLayout(layout)
        self.work_area.addWidget(page)

        self.load_catalog_data()

        self.btn_search_catalog.clicked.connect(self.search_catalog)
        self.btn_modify_furniture.clicked.connect(lambda: self.modify_furniture('edit'))
        self.catalog_table.itemSelectionChanged.connect(self.update_modify_button_state)

        return page
    #Фильтры каталога
    def load_catalog_filter_data(self):
        categories_query = "SELECT DISTINCT Наименование FROM Категория ORDER BY Наименование"
        categories = db.execute_query(categories_query)

        materials_query = "SELECT DISTINCT Наименование FROM Материал ORDER BY Наименование"
        materials = db.execute_query(materials_query)

        colors_query = "SELECT DISTINCT Наименование FROM Цвет ORDER BY Наименование"
        colors = db.execute_query(colors_query)

        if hasattr(self, 'category_filter_combo_catalog_page_main'):
            self.category_filter_combo_catalog_page_main.clear()
            self.category_filter_combo_catalog_page_main.addItem("Категория")
            for category in categories:
                if category[0]:
                    self.category_filter_combo_catalog_page_main.addItem(category[0])

        if hasattr(self, 'material_filter_combo_catalog_page'):
            self.material_filter_combo_catalog_page.clear()
            self.material_filter_combo_catalog_page.addItem("Материал")
            for material in materials:
                if material[0]:
                    self.material_filter_combo_catalog_page.addItem(material[0])

        if hasattr(self, 'color_filter_combo_catalog_page'):
            self.color_filter_combo_catalog_page.clear()
            self.color_filter_combo_catalog_page.addItem("Цвет")
            for color in colors:
                if color[0]:
                    self.color_filter_combo_catalog_page.addItem(color[0])

        if hasattr(self, 'category_filter_combo_catalog'):
            self.category_filter_combo_catalog.clear()
            self.category_filter_combo_catalog.addItem("Все категории")
            for category in categories:
                if category[0]:
                    self.category_filter_combo_catalog.addItem(category[0])

        if hasattr(self, 'material_filter_combo_catalog'):
            self.material_filter_combo_catalog.clear()
            self.material_filter_combo_catalog.addItem("Материал")
            for material in materials:
                if material[0]:
                    self.material_filter_combo_catalog.addItem(material[0])

        if hasattr(self, 'color_filter_combo_catalog'):
            self.color_filter_combo_catalog.clear()
            self.color_filter_combo_catalog.addItem("Цвет")
            for color in colors:
                if color[0]:
                    self.color_filter_combo_catalog.addItem(color[0])

    def filter_catalog_by_category(self):
        if hasattr(self, 'category_filter_combo_catalog_page_main'):
            selected_category = self.category_filter_combo_catalog_page_main.currentText()
        else:
            return

        if not hasattr(self, 'all_catalog_data') or not self.all_catalog_data:
            return

        if selected_category == "Категория":
            for row in range(self.catalog_table.rowCount()):
                self.catalog_table.setRowHidden(row, False)
            return

        for row in range(self.catalog_table.rowCount()):
            if row < len(self.all_catalog_data):
                category_in_data = self.all_catalog_data[row][2]
                if category_in_data == selected_category:
                    self.catalog_table.setRowHidden(row, False)
                else:
                    self.catalog_table.setRowHidden(row, True)

    def filter_catalog_by_material(self):
        if hasattr(self, 'material_filter_combo_catalog_page'):
            selected_material = self.material_filter_combo_catalog_page.currentText()
        else:
            return

        if not hasattr(self, 'all_catalog_data') or not self.all_catalog_data:
            return

        if selected_material == "Материал":
            for row in range(self.catalog_table.rowCount()):
                self.catalog_table.setRowHidden(row, False)
            return

        for row in range(self.catalog_table.rowCount()):
            if row < len(self.all_catalog_data):
                material_in_data = self.all_catalog_data[row][3]
                if material_in_data == selected_material:
                    self.catalog_table.setRowHidden(row, False)
                else:
                    self.catalog_table.setRowHidden(row, True)

    def filter_catalog_by_color(self):
        if hasattr(self, 'color_filter_combo_catalog_page'):
            selected_color = self.color_filter_combo_catalog_page.currentText()
        else:
            return

        if not hasattr(self, 'all_catalog_data') or not self.all_catalog_data:
            return

        if selected_color == "Цвет":
            for row in range(self.catalog_table.rowCount()):
                self.catalog_table.setRowHidden(row, False)
            return

        for row in range(self.catalog_table.rowCount()):
            if row < len(self.all_catalog_data):
                color_in_data = self.all_catalog_data[row][5]
                if color_in_data == selected_color:
                    self.catalog_table.setRowHidden(row, False)
                else:
                    self.catalog_table.setRowHidden(row, True)

    def update_modify_button_state(self):
        selected_rows = self.catalog_table.selectionModel().selectedRows()
        if selected_rows:
            self.btn_modify_furniture.setEnabled(True)
        else:
            self.btn_modify_furniture.setEnabled(False)
    #Поставки
    def create_supplies_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        top_panel = QHBoxLayout()

        search_label = QLabel("Поиск:")
        search_label.setFixedWidth(50)
        top_panel.addWidget(search_label)

        self.supplies_search = QLineEdit()
        self.supplies_search.setFixedHeight(30)
        self.supplies_search.setFixedWidth(850)
        top_panel.addWidget(self.supplies_search)

        self.btn_search_supplies = QPushButton("Поиск")
        self.btn_search_supplies.setFixedWidth(80)
        self.btn_search_supplies.setFixedHeight(30)
        top_panel.addWidget(self.btn_search_supplies)

        self.btn_add_supply = QPushButton("Поставка")
        self.btn_add_supply.setFixedWidth(100)
        self.btn_add_supply.setFixedHeight(30)
        top_panel.addWidget(self.btn_add_supply)

        self.btn_write_off = QPushButton("Списать")
        self.btn_write_off.setFixedWidth(100)
        self.btn_write_off.setFixedHeight(30)
        top_panel.addWidget(self.btn_write_off)

        top_panel.addStretch()
        layout.addLayout(top_panel)

        header_container = QWidget()
        header_layout = QHBoxLayout(header_container)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(1)

        column_widths = [120, 200, 150, 250, 250, 120, 150]

        for i in range(7):
            header_widget = QWidget()
            header_widget.setFixedWidth(column_widths[i])
            header_widget_layout = QVBoxLayout(header_widget)
            header_widget_layout.setContentsMargins(1, 1, 1, 1)
            header_widget_layout.setSpacing(0)

            if i == 0:
                label = QLabel("N операции")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 1:
                label = QLabel("Дата")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 2:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Тип операции")
                combo.addItem("Поставка")
                combo.addItem("Списание")
                combo.currentTextChanged.connect(self.filter_supplies_by_type)
                combo.setStyleSheet("""
                    QComboBox {
                        font-weight: bold;
                        padding: 4px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                self.operation_type_filter_combo = combo
                header_widget_layout.addWidget(combo)

            elif i == 3:
                label = QLabel("Наименование")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 4:
                label = QLabel("Производитель")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 5:
                label = QLabel("Количество")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 6:
                label = QLabel("Себестоимость")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            header_layout.addWidget(header_widget)

        self.supplies_table = QTableWidget()
        self.supplies_table.setColumnCount(7)

        for i, width in enumerate(column_widths):
            self.supplies_table.setColumnWidth(i, width)

        self.supplies_table.horizontalHeader().setVisible(False)
        self.supplies_table.verticalHeader().setVisible(False)

        self.supplies_table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        self.supplies_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.supplies_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)

        self.supplies_table.setAlternatingRowColors(True)

        layout.addWidget(header_container)
        layout.addWidget(self.supplies_table)

        page.setLayout(layout)
        self.work_area.addWidget(page)

        self.btn_search_supplies.clicked.connect(self.search_supplies_data)
        self.btn_add_supply.clicked.connect(lambda: self.modify_furniture('supply'))
        self.btn_write_off.clicked.connect(lambda: self.modify_furniture('write_off'))

        self.load_supplies_data()

        return page

    def filter_supplies_by_type(self):
        selected_type = self.operation_type_filter_combo.currentText()

        if not hasattr(self, 'all_supplies_data') or not self.all_supplies_data:
            return

        if selected_type == "Тип операции":
            for row in range(self.supplies_table.rowCount()):
                self.supplies_table.setRowHidden(row, False)
            return

        for row in range(self.supplies_table.rowCount()):
            if row < len(self.all_supplies_data):
                operation_type = self.all_supplies_data[row][2]
                if operation_type == selected_type:
                    self.supplies_table.setRowHidden(row, False)
                else:
                    self.supplies_table.setRowHidden(row, True)
    #Сотрудники
    def create_employees_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        top_panel = QHBoxLayout()

        search_label = QLabel("Поиск:")
        search_label.setFixedWidth(50)
        top_panel.addWidget(search_label)

        self.employees_search = QLineEdit()
        self.employees_search.setFixedHeight(30)
        self.employees_search.setFixedWidth(800)
        top_panel.addWidget(self.employees_search)

        self.btn_search_employees = QPushButton("Поиск")
        self.btn_search_employees.setFixedWidth(80)
        self.btn_search_employees.setFixedHeight(30)
        top_panel.addWidget(self.btn_search_employees)

        self.btn_add_employee = QPushButton("Создать")
        self.btn_add_employee.setFixedWidth(100)
        self.btn_add_employee.setFixedHeight(30)
        top_panel.addWidget(self.btn_add_employee)

        self.btn_modify_employee = QPushButton("Изменить")
        self.btn_modify_employee.setFixedWidth(100)
        self.btn_modify_employee.setFixedHeight(30)
        self.btn_modify_employee.setEnabled(False)

        top_panel.addWidget(self.btn_modify_employee)

        top_panel.addStretch()
        layout.addLayout(top_panel)

        self.employees_scroll = QScrollArea()
        self.employees_scroll.setWidgetResizable(True)
        self.employees_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f5f5;
            }
            QScrollBar:vertical {
                width: 12px;
                background-color: #f0f0f0;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)

        self.employees_cards_container = QWidget()
        self.employees_cards_container.setStyleSheet("background-color: #f5f5f5;")
        self.employees_cards_layout = QGridLayout(self.employees_cards_container)
        self.employees_cards_layout.setSpacing(15)
        self.employees_cards_layout.setContentsMargins(20, 20, 20, 20)
        self.employees_cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.employees_scroll.setWidget(self.employees_cards_container)
        layout.addWidget(self.employees_scroll)

        page.setLayout(layout)
        self.work_area.addWidget(page)

        self.btn_search_employees.clicked.connect(self.search_employees)
        self.btn_add_employee.clicked.connect(self.add_employee)
        self.btn_modify_employee.clicked.connect(self.modify_employee)

        self.load_employees_cards()

    def create_employee_card(self, employee):
        card = QFrame()
        card.setMinimumSize(500, 170)
        card.setMaximumWidth(600)
        card.setMaximumHeight(200)

        card.employee_id = employee.get("id")
        card.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QLabel {
                border: none;
                background-color: transparent;
            }
        """)

        card.mousePressEvent = lambda event: self.select_employee_card(card, employee.get("id"))

        main_layout = QVBoxLayout(card)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        info_widget = QWidget()
        info_layout = QGridLayout(info_widget)
        info_layout.setVerticalSpacing(8)
        info_layout.setHorizontalSpacing(20)

        row = 0

        info_layout.addWidget(QLabel("Фамилия:"), row, 0)
        info_layout.addWidget(QLabel(str(employee.get("surname", ""))), row, 1)
        row += 1

        info_layout.addWidget(QLabel("Имя:"), row, 0)
        info_layout.addWidget(QLabel(str(employee.get("name", ""))), row, 1)
        row += 1

        info_layout.addWidget(QLabel("Отчество:"), row, 0)
        info_layout.addWidget(QLabel(str(employee.get("patronymic", ""))), row, 1)
        row += 1

        info_layout.addWidget(QLabel("Телефон:"), row, 0)
        phone = employee.get("phone", "")
        info_layout.addWidget(QLabel(str(phone) if phone else "Не указан"), row, 1)
        row += 1

        info_layout.addWidget(QLabel("Email:"), row, 0)
        email = employee.get("email", "")
        info_layout.addWidget(QLabel(str(email) if email else "Не указан"), row, 1)
        row += 1

        info_layout.addWidget(QLabel("График работы:"), row, 0)
        schedule = employee.get("schedule", "")
        info_layout.addWidget(QLabel(str(schedule) if schedule else "Не указан"), row, 1)
        row += 1

        row = 0

        info_layout.addWidget(QLabel("Оклад:"), row, 2)
        salary = employee.get("salary", "")
        info_layout.addWidget(QLabel(salary), row, 3)
        row += 1

        info_layout.addWidget(QLabel("Дата рождения:"), row, 2)
        birth_date = employee.get("birth_date", "")
        info_layout.addWidget(QLabel(str(birth_date) if birth_date else "Не указана"), row, 3)
        row += 1

        info_layout.addWidget(QLabel("Должность:"), row, 2)
        position = employee.get("position", "")
        info_layout.addWidget(QLabel(str(position) if position else "Не указана"), row, 3)
        row += 1

        info_layout.addWidget(QLabel("Пароль:"), row, 2)
        password = employee.get("password", "")
        info_layout.addWidget(QLabel(str(password) if password else "Не указан"), row, 3)
        row += 1

        main_layout.addWidget(info_widget)
        main_layout.addStretch()
        return card

    def select_employee_card(self, card, employee_id):
        if self.selected_employee_id:
            self.clear_employee_selection()

        card.setStyleSheet("""
            QFrame {
                border: 2px solid black;;
                border-radius: 4px;
                background-color: white;
            }
            QLabel {
                border: none;
                background-color: transparent;
            }
        """)

        self.selected_employee_id = employee_id
        self.btn_modify_employee.setEnabled(True)

    def clear_employee_selection(self):
        for i in range(self.employees_cards_layout.count()):
            item = self.employees_cards_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget and hasattr(widget, 'employee_id'):
                    widget.setStyleSheet("""
                            QFrame {
                                border: 1px solid #ccc;
                                border-radius: 4px;
                                background-color: white;
                            }
                            QLabel {
                                border: none;
                                background-color: transparent;
                            }
                        """)

        self.selected_employee_id = None
        self.btn_modify_employee.setEnabled(False)
    #Касса
    def create_cash_page(self):
        page = QWidget()
        main_layout = QVBoxLayout()

        catalog_group = QWidget()
        catalog_layout = QVBoxLayout(catalog_group)
        catalog_layout.setSpacing(10)

        catalog_controls_row = QHBoxLayout()

        catalog_label = QLabel("Поиск по каталогу:")
        catalog_label.setFixedWidth(120)
        catalog_controls_row.addWidget(catalog_label)

        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(5)

        self.catalog_search_cash = QLineEdit()
        self.catalog_search_cash.setFixedWidth(650)
        search_layout.addWidget(self.catalog_search_cash)

        self.btn_search_catalog_cash = QPushButton("Поиск")
        self.btn_search_catalog_cash.setFixedWidth(80)
        search_layout.addWidget(self.btn_search_catalog_cash)
        catalog_controls_row.addWidget(search_widget)

        self.category_filter_combo_catalog = QComboBox()
        self.category_filter_combo_catalog.addItem("Все категории")
        self.category_filter_combo_catalog.setFixedWidth(150)
        catalog_controls_row.addWidget(self.category_filter_combo_catalog)

        self.btn_add_to_cart = QPushButton("Добавить в кассу")
        self.btn_add_to_cart.setFixedWidth(150)

        catalog_controls_row.addWidget(self.btn_add_to_cart)

        catalog_controls_row.addStretch()
        catalog_layout.addLayout(catalog_controls_row)

        header_container_top = QWidget()
        header_layout_top = QHBoxLayout(header_container_top)
        header_layout_top.setContentsMargins(0, 0, 0, 0)
        header_layout_top.setSpacing(1)

        column_widths_top = [235, 135, 230, 150, 150, 100, 120, 100]

        for i in range(8):
            header_widget = QWidget()
            header_widget.setFixedWidth(column_widths_top[i])
            header_widget_layout = QVBoxLayout(header_widget)
            header_widget_layout.setContentsMargins(1, 1, 1, 1)
            header_widget_layout.setSpacing(0)

            if i == 0:
                label = QLabel("Наименование")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 1:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Материал")
                combo.setStyleSheet("""
                    QComboBox {
                        font-weight: bold;
                        padding: 4px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                self.material_filter_combo_catalog = combo
                header_widget_layout.addWidget(combo)

            elif i == 2:
                label = QLabel("Производитель")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 3:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Цвет")
                combo.setStyleSheet("""
                    QComboBox {
                        font-weight: bold;
                        padding: 4px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                self.color_filter_combo_catalog = combo
                header_widget_layout.addWidget(combo)

            elif i == 4:
                label = QLabel("Габариты, мм")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 5:
                label = QLabel("Вес. кг")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 6:
                label = QLabel("В наличии, шт")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 7:
                label = QLabel("Цена, руб")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            header_layout_top.addWidget(header_widget)

        self.catalog_table_cash = QTableWidget()
        self.catalog_table_cash.setColumnCount(8)

        for i, width in enumerate(column_widths_top):
            self.catalog_table_cash.setColumnWidth(i, width)

        self.catalog_table_cash.horizontalHeader().setVisible(False)
        self.catalog_table_cash.verticalHeader().setVisible(False)
        self.catalog_table_cash.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.catalog_table_cash.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.catalog_table_cash.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.catalog_table_cash.setAlternatingRowColors(True)

        catalog_layout.addWidget(header_container_top)
        catalog_layout.addWidget(self.catalog_table_cash)
        main_layout.addWidget(catalog_group)

        client_info_group = QWidget()
        client_info_layout = QVBoxLayout(client_info_group)

        client_row = QHBoxLayout()

        name_label = QLabel("Заказ для:")
        name_label.setFixedWidth(80)
        client_row.addWidget(name_label)

        self.client_name_input = QLineEdit()
        client_row.addWidget(self.client_name_input)

        phone_label = QLabel("Тел.")
        phone_label.setFixedWidth(30)
        client_row.addWidget(phone_label)

        self.client_phone_input = QLineEdit()
        client_row.addWidget(self.client_phone_input)

        email_label = QLabel("e-mail:")
        email_label.setFixedWidth(50)
        client_row.addWidget(email_label)

        self.client_email_input = QLineEdit()
        client_row.addWidget(self.client_email_input)

        client_row.addStretch()

        client_info_layout.addLayout(client_row)
        main_layout.addWidget(client_info_group)

        cart_group = QWidget()
        cart_layout = QVBoxLayout(cart_group)
        cart_layout.setSpacing(10)

        cart_controls_row = QHBoxLayout()

        cart_label = QLabel("Поиск по кассе:")
        cart_label.setFixedWidth(120)
        cart_controls_row.addWidget(cart_label)

        cart_search_widget = QWidget()
        cart_search_layout = QHBoxLayout(cart_search_widget)
        cart_search_layout.setContentsMargins(0, 0, 0, 0)
        cart_search_layout.setSpacing(5)

        self.cart_search_input = QLineEdit()
        self.cart_search_input.setFixedWidth(650)
        cart_search_layout.addWidget(self.cart_search_input)

        self.btn_search_cart = QPushButton("Поиск")
        self.btn_search_cart.setFixedWidth(80)

        cart_search_layout.addWidget(self.btn_search_cart)
        cart_controls_row.addWidget(cart_search_widget)

        self.category_filter_combo_cart = QComboBox()
        self.category_filter_combo_cart.addItem("Все категории")
        self.category_filter_combo_cart.setFixedWidth(150)
        cart_controls_row.addWidget(self.category_filter_combo_cart)

        self.btn_remove_from_cart = QPushButton("Убрать из кассы")
        self.btn_remove_from_cart.setFixedWidth(150)

        cart_controls_row.addWidget(self.btn_remove_from_cart)

        cart_controls_row.addStretch()
        cart_layout.addLayout(cart_controls_row)

        header_container_bottom = QWidget()
        header_layout_bottom = QHBoxLayout(header_container_bottom)
        header_layout_bottom.setContentsMargins(0, 0, 0, 0)
        header_layout_bottom.setSpacing(1)

        column_widths_bottom = [235, 135, 230, 150, 150, 100, 120, 100]

        for i in range(8):
            header_widget = QWidget()
            header_widget.setFixedWidth(column_widths_bottom[i])
            header_widget_layout = QVBoxLayout(header_widget)
            header_widget_layout.setContentsMargins(1, 1, 1, 1)
            header_widget_layout.setSpacing(0)

            if i == 0:
                label = QLabel("Наименование")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 1:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Материал")
                combo.setStyleSheet("""
                    QComboBox {
                        font-weight: bold;
                        padding: 4px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                self.material_filter_combo_cart = combo
                header_widget_layout.addWidget(combo)

            elif i == 2:
                label = QLabel("Производитель")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 3:
                combo = QComboBox()
                combo.setFixedHeight(30)
                combo.addItem("Цвет")
                combo.setStyleSheet("""
                    QComboBox {
                        font-weight: bold;
                        padding: 4px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                self.color_filter_combo_cart = combo
                header_widget_layout.addWidget(combo)

            elif i == 4:
                label = QLabel("Габариты, мм")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 5:
                label = QLabel("Вес. кг")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 6:
                label = QLabel("Количество")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            elif i == 7:
                label = QLabel("Цена, руб")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("""
                    QLabel {
                        font-weight: bold;
                        padding: 8px;
                        background-color: #f0f0f0;
                        border: 1px solid #d0d0d0;
                    }
                """)
                header_widget_layout.addWidget(label)

            header_layout_bottom.addWidget(header_widget)

        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(8)

        for i, width in enumerate(column_widths_bottom):
            self.cart_table.setColumnWidth(i, width)

        self.cart_table.horizontalHeader().setVisible(False)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cart_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.cart_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.cart_table.setAlternatingRowColors(True)

        cart_layout.addWidget(header_container_bottom)
        cart_layout.addWidget(self.cart_table)
        main_layout.addWidget(cart_group)

        summary_panel = QHBoxLayout()
        summary_panel.setContentsMargins(0, 20, 0, 0)

        checkboxes_panel = QVBoxLayout()
        checkboxes_panel.setSpacing(10)

        self.additional_services = []
        query = "SELECT вид, стоимость FROM ДопУслуги"
        result = db.execute_query(query)
        self.additional_services = [(row[0], float(row[1])) for row in result]

        self.service_checkboxes = {}
        for service_name, service_price in self.additional_services:
            checkbox = QCheckBox(service_name)
            checkbox.service_name = service_name
            checkbox.service_price = service_price
            checkbox.stateChanged.connect(self.update_order_summary)
            checkboxes_panel.addWidget(checkbox)
            self.service_checkboxes[service_name] = checkbox

        summary_panel.addLayout(checkboxes_panel)

        sums_panel = QHBoxLayout()
        sums_panel.setSpacing(30)

        sum_widget = QWidget()
        sum_layout = QHBoxLayout(sum_widget)
        sum_layout.setSpacing(5)
        sum_label = QLabel("Сумма:")
        sum_layout.addWidget(sum_label)

        self.sum_value_label = QLabel("0 руб")
        self.sum_value_label.setStyleSheet("font-size: 12pt;")
        sum_layout.addWidget(self.sum_value_label)
        sums_panel.addWidget(sum_widget)

        discount_widget = QWidget()
        discount_layout = QHBoxLayout(discount_widget)
        discount_layout.setSpacing(5)

        discount_label = QLabel("Скидка:")
        discount_layout.addWidget(discount_label)

        self.discounts_combo = QComboBox()
        self.discounts_combo.addItem("Без скидки", 0)

        query = "SELECT Наименование, Процент FROM Скидка"
        result = db.execute_query(query)
        for row in result:
            self.discounts_combo.addItem(f"{row[0]} ({row[1]}%)", float(row[1]))

        self.discounts_combo.setFixedWidth(150)
        self.discounts_combo.currentIndexChanged.connect(self.update_order_summary)
        discount_layout.addWidget(self.discounts_combo)

        sums_panel.addWidget(discount_widget)

        total_widget = QWidget()
        total_layout = QHBoxLayout(total_widget)
        total_layout.setSpacing(5)

        total_label = QLabel("Сумма со скидкой:")
        total_layout.addWidget(total_label)

        self.total_with_discount_value_label = QLabel("0 руб")
        total_layout.addWidget(self.total_with_discount_value_label)
        sums_panel.addWidget(total_widget)

        summary_panel.addLayout(sums_panel)
        summary_panel.addStretch()

        self.btn_confirm_order = QPushButton("Подтвердить")
        self.btn_confirm_order.setFixedWidth(250)
        self.btn_confirm_order.setFixedHeight(50)

        summary_panel.addWidget(self.btn_confirm_order)

        main_layout.addLayout(summary_panel)
        page.setLayout(main_layout)
        self.work_area.addWidget(page)

        self.load_cash_filters_data()
        self.load_catalog_data_cash()
        self.cart_data = []

        self.btn_add_to_cart.clicked.connect(self.add_item_to_cart)
        self.btn_remove_from_cart.clicked.connect(self.remove_item_from_cart)
        self.btn_confirm_order.clicked.connect(self.confirm_order)

        self.btn_search_catalog_cash.clicked.connect(self.search_cash_page)
        self.btn_search_cart.clicked.connect(self.search_cart_cash)

        self.category_filter_combo_catalog.currentTextChanged.connect(self.filter_category_cash)
        self.category_filter_combo_cart.currentTextChanged.connect(self.filter_category_cart)

        return page

    def update_order_summary(self):
        base_total = 0
        for cart_item in self.cart_data:
            base_total += float(cart_item['price']) * cart_item['quantity']

        services_total = 0
        for service_name, checkbox in self.service_checkboxes.items():
            if checkbox.isChecked():
                services_total += checkbox.service_price

        discount_percent = self.discounts_combo.currentData() or 0
        discount_amount = (base_total * discount_percent) / 100

        total_after_discount = base_total - discount_amount

        total_with_services = total_after_discount + services_total

        self.sum_value_label.setText(f"{base_total + services_total:.2f} руб")
        self.total_with_discount_value_label.setText(f"{total_with_services:.2f} руб")

    def add_item_to_cart(self):
        current_row = self.catalog_table_cash.currentRow()

        if current_row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите товар из каталога!")
            return

        item_data = self.catalog_data_cash[current_row]

        available_quantity = int(item_data['quantity'])
        if available_quantity <= 0:
            QMessageBox.warning(self, "Внимание", "Товара нет в наличии!")
            return

        cart_item_index = -1
        for i, cart_item in enumerate(self.cart_data):
            if cart_item['furniture_id'] == item_data['furniture_id']:
                cart_item_index = i
                break

        if cart_item_index >= 0:
            self.cart_data[cart_item_index]['quantity'] += 1

            quantity_item = self.cart_table.item(cart_item_index, 6)
            new_quantity = int(quantity_item.text()) + 1
            quantity_item.setText(str(new_quantity))
        else:
            cart_item = {
                'name': item_data['name'],
                'material': item_data['material'],
                'producer': item_data['producer'],
                'color': item_data['color'],
                'dimensions': item_data['dimensions'],
                'weight': item_data['weight'],
                'quantity': 1,
                'price': item_data['price'],
                'category': item_data['category'],
                'furniture_id': item_data['furniture_id'],
                'catalog_row': current_row
            }
            self.cart_data.append(cart_item)

            row_position = self.cart_table.rowCount()
            self.cart_table.insertRow(row_position)

            for col_idx, key in enumerate(['name', 'material', 'producer', 'color',
                                           'dimensions', 'weight']):
                item = QTableWidgetItem(str(cart_item[key]))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.cart_table.setItem(row_position, col_idx, item)

            quantity_item = QTableWidgetItem("1")
            quantity_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cart_table.setItem(row_position, 6, quantity_item)

            price_item = QTableWidgetItem(str(cart_item['price']))
            price_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.cart_table.setItem(row_position, 7, price_item)

        new_quantity = available_quantity - 1
        item_data['quantity'] = new_quantity

        quantity_item_catalog = self.catalog_table_cash.item(current_row, 6)
        quantity_item_catalog.setText(str(new_quantity))

        if new_quantity == 0:
            self.catalog_table_cash.setRowHidden(current_row, True)

        self.update_order_summary()

    def remove_item_from_cart(self):
        current_row = self.cart_table.currentRow()

        if current_row < 0:
            QMessageBox.warning(self, "Внимание", "Выберите товар из корзины!")
            return

        if current_row >= len(self.cart_data):
            return

        cart_item = self.cart_data[current_row]

        if cart_item['quantity'] > 1:
            cart_item['quantity'] -= 1
            quantity_item = self.cart_table.item(current_row, 6)
            new_quantity = int(quantity_item.text()) - 1
            quantity_item.setText(str(new_quantity))
        else:
            self.cart_data.pop(current_row)
            self.cart_table.removeRow(current_row)

        catalog_row = cart_item.get('catalog_row')

        for idx, item_data in enumerate(self.catalog_data_cash):
            if item_data['furniture_id'] == cart_item['furniture_id']:
                new_catalog_quantity = item_data['quantity'] + 1
                item_data['quantity'] = new_catalog_quantity

                quantity_item_catalog = self.catalog_table_cash.item(idx, 6)
                if quantity_item_catalog:
                    quantity_item_catalog.setText(str(new_catalog_quantity))

                if self.catalog_table_cash.isRowHidden(idx):
                    self.catalog_table_cash.setRowHidden(idx, False)

                break

        self.update_order_summary()

    def confirm_order(self):
        client_name = self.client_name_input.text().strip()
        client_phone = self.client_phone_input.text().strip()
        client_email = self.client_email_input.text().strip()

        if not client_name:
            QMessageBox.warning(self, "Ошибка", "Введите ФИО клиента!")
            return

        if not client_phone:
            QMessageBox.warning(self, "Ошибка", "Введите телефон клиента!")
            return

        if not client_email or '@' not in client_email:
            QMessageBox.warning(self, "Ошибка", "Введите корректный email!")
            return

        if not self.cart_data:
            QMessageBox.warning(self, "Ошибка", "Корзина пуста!")
            return

        try:
            client_query = """
            SELECT idКлиент FROM Клиент 
            WHERE email = %s 
            LIMIT 1
            """
            client_result = db.execute_query(client_query, (client_email,))

            if client_result and client_result[0][0]:
                client_id = client_result[0][0]
            else:
                name_parts = client_name.split()
                surname = name_parts[0] if len(name_parts) > 0 else ""
                name = name_parts[1] if len(name_parts) > 1 else ""
                patronymic = name_parts[2] if len(name_parts) > 2 else ""

                full_name = f"{surname} {name}"
                if patronymic:
                    full_name += f" {patronymic}"

                client_insert_query = """
                INSERT INTO Клиент (email, телефон, ФИО) 
                VALUES (%s, %s, %s)
                """
                db.execute_query(client_insert_query, (client_email, client_phone, full_name))

                get_client_id_query = "SELECT LAST_INSERT_ID()"
                client_id_result = db.execute_query(get_client_id_query)
                client_id = client_id_result[0][0]

            discount_percent = self.discounts_combo.currentData()
            discount_id = None
            if discount_percent and discount_percent > 0:
                discount_query = "SELECT idСкидка FROM Скидка WHERE Процент = %s LIMIT 1"
                discount_result = db.execute_query(discount_query, (discount_percent,))
                if discount_result and discount_result[0][0]:
                    discount_id = discount_result[0][0]

            # 3. Создаем заказ
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_employee_id = self.user_data.get('id', 1)

            order_query = """
            INSERT INTO Заказ (Дата, Статус, Клиент_idКлиент, Сотрудники_idСотрудника, Скидка_idСкидка)
            VALUES (%s, 'Размещён', %s, %s, %s)
            """
            db.execute_query(order_query, (current_date, client_id, current_employee_id, discount_id))

            get_order_id_query = "SELECT LAST_INSERT_ID()"
            order_id_result = db.execute_query(get_order_id_query)
            order_id = order_id_result[0][0]

            for service_name, checkbox in self.service_checkboxes.items():
                if checkbox.isChecked():
                    service_query = "SELECT idДопУслуги FROM ДопУслуги WHERE вид = %s"
                    service_result = db.execute_query(service_query, (service_name,))

                    if service_result and service_result[0][0]:
                        service_id = service_result[0][0]
                        service_link_query = """
                        INSERT INTO ДопУслуги_has_Заказ (ДопУслуги_idДопУслуги, Заказ_idЗаказ)
                        VALUES (%s, %s)
                        """
                        db.execute_query(service_link_query, (service_id, order_id))

            for cart_item in self.cart_data:
                furniture_id = cart_item['furniture_id']
                quantity = cart_item['quantity']

                check_stock_query = """
                SELECT Количество FROM Мебель WHERE idМебель = %s
                """
                stock_result = db.execute_query(check_stock_query, (furniture_id,))

                if not stock_result or stock_result[0][0] < quantity:
                    raise Exception(
                        f"Недостаточно товара {cart_item['name']} на складе! Доступно: {stock_result[0][0] if stock_result else 0}, нужно: {quantity}")

                order_item_query = """
                INSERT INTO ПозицииВзаказе (Заказ_idЗаказ, Мебель_idМебель, Количество)
                VALUES (%s, %s, %s)
                """
                db.execute_query(order_item_query, (order_id, furniture_id, quantity))

                update_stock_query = """
                UPDATE Мебель 
                SET Количество = Количество - %s
                WHERE idМебель = %s
                """
                db.execute_query(update_stock_query, (quantity, furniture_id))

            total_amount = sum(item['quantity'] * item['price'] for item in self.cart_data)

            self.clear_cart()
            self.load_catalog_data_cash()
            self.load_catalog_data()

            if hasattr(self, 'orders_table'):
                self.load_orders_data()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить заказ: {str(e)}")

    def clear_cart(self):
        self.cart_data = []
        self.cart_table.setRowCount(0)

        self.client_name_input.clear()
        self.client_phone_input.clear()
        self.client_email_input.clear()

        for service_name, checkbox in self.service_checkboxes.items():
            checkbox.setChecked(False)

        self.discounts_combo.setCurrentIndex(0)

        self.update_order_summary()

        self.load_catalog_data_cash()

    #Фильтры каталога кассы
    def filter_category_cash(self):
        selected_category = self.category_filter_combo_catalog.currentText()

        if selected_category == "Все категории":
            for row in range(self.catalog_table_cash.rowCount()):
                self.catalog_table_cash.setRowHidden(row, False)
            return

        for row in range(self.catalog_table_cash.rowCount()):
            if row < len(self.catalog_data_cash):
                item_data = self.catalog_data_cash[row]
                item_category = item_data.get('category', '')
                self.catalog_table_cash.setRowHidden(row, item_category != selected_category)
            else:
                self.catalog_table_cash.setRowHidden(row, True)

    def filter_material_cash(self):
        selected_material = self.material_filter_combo_catalog.currentText()

        if selected_material == "Материал":
            for row in range(self.catalog_table_cash.rowCount()):
                self.catalog_table_cash.setRowHidden(row, False)
            return

        for row in range(self.catalog_table_cash.rowCount()):
            if row < len(self.catalog_data_cash):
                item_data = self.catalog_data_cash[row]
                item_material = item_data.get('material', '')
                self.catalog_table_cash.setRowHidden(row, item_material != selected_material)
            else:
                self.catalog_table_cash.setRowHidden(row, True)

    def filter_color_cash(self):
        selected_color = self.color_filter_combo_catalog.currentText()

        if selected_color == "Цвет":
            for row in range(self.catalog_table_cash.rowCount()):
                self.catalog_table_cash.setRowHidden(row, False)
            return

        for row in range(self.catalog_table_cash.rowCount()):
            if row < len(self.catalog_data_cash):
                item_data = self.catalog_data_cash[row]
                item_color = item_data.get('color', '')
                self.catalog_table_cash.setRowHidden(row, item_color != selected_color)
            else:
                self.catalog_table_cash.setRowHidden(row, True)
    #Фильтры корзины
    def filter_category_cart(self):
        selected_category = self.category_filter_combo_cart.currentText()

        if selected_category == "Все категории":
            for row in range(self.cart_table.rowCount()):
                self.cart_table.setRowHidden(row, False)
            return

        for row in range(self.cart_table.rowCount()):
            if row < len(self.cart_data):
                item_category = self.cart_data[row].get('category', '')
                self.cart_table.setRowHidden(row, item_category != selected_category)
            else:
                self.cart_table.setRowHidden(row, True)

    def filter_material_cart(self):
        selected_material = self.material_filter_combo_cart.currentText()

        if selected_material == "Материал":
            for row in range(self.cart_table.rowCount()):
                self.cart_table.setRowHidden(row, False)
            return

        for row in range(self.cart_table.rowCount()):
            if row < len(self.cart_data):
                item_material = self.cart_data[row].get('material', '')
                self.cart_table.setRowHidden(row, item_material != selected_material)
            else:
                material_item = self.cart_table.item(row, 1)
                if material_item:
                    self.cart_table.setRowHidden(row, material_item.text() != selected_material)
                else:
                    self.cart_table.setRowHidden(row, True)

    def filter_color_cart(self):
        selected_color = self.color_filter_combo_cart.currentText()

        if selected_color == "Цвет":
            for row in range(self.cart_table.rowCount()):
                self.cart_table.setRowHidden(row, False)
            return

        for row in range(self.cart_table.rowCount()):
            if row < len(self.cart_data):
                item_color = self.cart_data[row].get('color', '')
                self.cart_table.setRowHidden(row, item_color != selected_color)
            else:
                color_item = self.cart_table.item(row, 3)
                if color_item:
                    self.cart_table.setRowHidden(row, color_item.text() != selected_color)
                else:
                    self.cart_table.setRowHidden(row, True)
    #Заказы
    def create_orders_page(self):
        page = QWidget()
        main_layout = QVBoxLayout()

        top_panel = QWidget()
        top_layout = QHBoxLayout(top_panel)

        search_label = QLabel("Поиск")
        search_label.setFixedWidth(50)
        top_layout.addWidget(search_label)

        self.orders_search_input = QLineEdit()
        self.orders_search_input.setFixedWidth(1050)
        top_layout.addWidget(self.orders_search_input)

        self.btn_search_orders = QPushButton("Найти")
        self.btn_search_orders.setFixedWidth(80)
        top_layout.addWidget(self.btn_search_orders)

        main_layout.addWidget(top_panel)

        table_container = QWidget()
        table_layout = QVBoxLayout(table_container)

        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(9)
        self.orders_table.verticalHeader().setVisible(False)
        self.orders_table.setHorizontalHeaderLabels([
            "№заказа", "Клиент", "Мебель", "Количество,шт",
            "Дата", "Доп. услуги", "Статус", "Стоимость,руб", "Сотрудник"
        ])

        column_widths = [80, 175, 175, 100, 120, 134, 150, 120, 175]
        for i, width in enumerate(column_widths):
            self.orders_table.setColumnWidth(i, width)

        self.orders_table.setAlternatingRowColors(True)
        self.orders_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.orders_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        header = self.orders_table.horizontalHeader()

        for i in range(self.orders_table.columnCount()):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.Fixed)

        header.setStretchLastSection(False)
        header.setSectionsMovable(False)

        table_layout.addWidget(self.orders_table)
        main_layout.addWidget(table_container)

        status_panel = QWidget()
        status_layout = QHBoxLayout(status_panel)

        status_label = QLabel("Изменение статуса заказа:")
        status_label.setFixedWidth(150)
        status_layout.addWidget(status_label)

        self.status_placed_checkbox = QCheckBox("Размещён")
        self.status_in_process_checkbox = QCheckBox("В процессе")
        self.status_completed_checkbox = QCheckBox("Выполнен")

        self.status_button_group = QButtonGroup()
        self.status_button_group.setExclusive(True)
        self.status_button_group.addButton(self.status_placed_checkbox)
        self.status_button_group.addButton(self.status_in_process_checkbox)
        self.status_button_group.addButton(self.status_completed_checkbox)

        self.status_placed_checkbox.setEnabled(False)
        self.status_in_process_checkbox.setEnabled(False)
        self.status_completed_checkbox.setEnabled(False)

        status_layout.addWidget(self.status_placed_checkbox)
        status_layout.addWidget(self.status_in_process_checkbox)
        status_layout.addWidget(self.status_completed_checkbox)

        status_layout.addStretch()
        main_layout.addWidget(status_panel)

        page.setLayout(main_layout)
        self.work_area.addWidget(page)

        self.load_orders_data()

        self.btn_search_orders.clicked.connect(self.search_orders_page)
        self.orders_table.itemSelectionChanged.connect(self.on_order_selected)
        self.status_placed_checkbox.stateChanged.connect(lambda: self.update_order_status("Размещён"))
        self.status_in_process_checkbox.stateChanged.connect(lambda: self.update_order_status("В процессе"))
        self.status_completed_checkbox.stateChanged.connect(lambda: self.update_order_status("Выполнен"))

        return page

    def on_order_selected(self):
        selected_rows = self.orders_table.selectionModel().selectedRows()

        if not selected_rows:
            self.status_placed_checkbox.setEnabled(False)
            self.status_in_process_checkbox.setEnabled(False)
            self.status_completed_checkbox.setEnabled(False)

            self.status_button_group.setExclusive(False)
            self.status_placed_checkbox.setChecked(False)
            self.status_in_process_checkbox.setChecked(False)
            self.status_completed_checkbox.setChecked(False)
            self.status_button_group.setExclusive(True)
            return

        self.status_placed_checkbox.setEnabled(True)
        self.status_in_process_checkbox.setEnabled(True)
        self.status_completed_checkbox.setEnabled(True)

        row = selected_rows[0].row()
        status_item = self.orders_table.item(row, 6)

        if status_item:
            current_status = status_item.text()

            self.status_placed_checkbox.blockSignals(True)
            self.status_in_process_checkbox.blockSignals(True)
            self.status_completed_checkbox.blockSignals(True)

            if current_status == "Размещён":
                self.status_placed_checkbox.setChecked(True)
            elif current_status == "В процессе":
                self.status_in_process_checkbox.setChecked(True)
            elif current_status == "Выполнен":
                self.status_completed_checkbox.setChecked(True)

            self.status_placed_checkbox.blockSignals(False)
            self.status_in_process_checkbox.blockSignals(False)
            self.status_completed_checkbox.blockSignals(False)

    def update_order_status(self, new_status):
        selected_rows = self.orders_table.selectionModel().selectedRows()

        if not selected_rows:
            return

        row = selected_rows[0].row()
        order_id_item = self.orders_table.item(row, 0)

        if not order_id_item:
            return

        order_id = order_id_item.text()

        update_query = "UPDATE Заказ SET Статус = %s WHERE idЗаказ = %s"
        db.execute_query(update_query, (new_status, order_id))

        status_item = self.orders_table.item(row, 6)
        if status_item:
            status_item.setText(new_status)
    #Клиенты
    def create_clients_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        top_panel = QHBoxLayout()

        search_label = QLabel("Поиск:")
        search_label.setFixedWidth(50)
        top_panel.addWidget(search_label)

        self.clients_search = QLineEdit()
        self.clients_search.setFixedHeight(30)
        self.clients_search.setFixedWidth(900)
        top_panel.addWidget(self.clients_search)

        self.btn_search_clients = QPushButton("Поиск")
        self.btn_search_clients.setFixedWidth(80)
        self.btn_search_clients.setFixedHeight(30)
        top_panel.addWidget(self.btn_search_clients)

        top_panel.addStretch()
        layout.addLayout(top_panel)

        self.clients_scroll = QScrollArea()
        self.clients_scroll.setWidgetResizable(True)
        self.clients_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #f5f5f5;
            }
            QScrollBar:vertical {
                width: 12px;
                background-color: #f0f0f0;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)

        self.clients_cards_container = QWidget()
        self.clients_cards_container.setStyleSheet("background-color: #f5f5f5;")
        self.clients_cards_layout = QGridLayout(self.clients_cards_container)
        self.clients_cards_layout.setSpacing(15)
        self.clients_cards_layout.setContentsMargins(20, 20, 20, 20)
        self.clients_cards_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.clients_scroll.setWidget(self.clients_cards_container)
        layout.addWidget(self.clients_scroll)

        page.setLayout(layout)
        self.work_area.addWidget(page)

        self.btn_search_clients.clicked.connect(self.search_clients_page)
        self.load_clients_cards()

        return page

    def create_client_card(self, client):
        card = QFrame()
        card.setMinimumSize(500, 170)
        card.setMaximumWidth(600)
        card.setMaximumHeight(200)

        card.client_id = client.get("id")
        card.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
            }
            QLabel {
                border: none;
                background-color: transparent;
            }
        """)

        main_layout = QVBoxLayout(card)
        main_layout.setContentsMargins(15, 10, 15, 10)
        main_layout.setSpacing(8)

        name_line = QHBoxLayout()

        name_label = QLabel(str(client.get("name", "")))
        name_line.addWidget(name_label)

        contact_info = QLabel(f"({client.get('email', '')}, {client.get('phone', '')})")
        name_line.addWidget(contact_info)

        name_line.addStretch()
        main_layout.addLayout(name_line)

        orders_text = client.get("orders_info")
        orders_label = QLabel(orders_text)
        orders_label.setWordWrap(True)
        main_layout.addWidget(orders_label)

        main_layout.addStretch()

        if client.get("seller_info"):
            bottom_line = QHBoxLayout()

            seller_label = QLabel(f"Продавец: {client.get('seller_info', '')}")
            bottom_line.addWidget(seller_label)

            bottom_line.addStretch()
            main_layout.addLayout(bottom_line)

        return card
    #Отчёты
    def create_reports_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        buttons_panel = QHBoxLayout()
        buttons_panel.setSpacing(10)

        self.report_buttons = []
        report_configs = [
            ("Продажи за период", "sales_period"),
            ("Продажи по работникам", "sales_employees"),
            ("Доходы и расходы", "income_expenses"),
            ("Средний чек", "avg_check"),
            ("Анализ продаж", "sales_analysis"),
            ("Анализ рентабельности", "profitability_analysis")
        ]

        for btn_text, report_type in report_configs:
            btn = QPushButton(btn_text)
            btn.setFixedHeight(40)
            btn.setMinimumWidth(150)

            btn.clicked.connect(lambda checked, rt=report_type: self.generate_report_by_type(rt))

            buttons_panel.addWidget(btn)
            self.report_buttons.append(btn)

        buttons_panel.addStretch()
        layout.addLayout(buttons_panel)

        report_display = QGroupBox()

        report_display_layout = QVBoxLayout()

        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)

        report_display_layout.addWidget(self.report_text)
        report_display.setLayout(report_display_layout)
        layout.addWidget(report_display)

        page.setLayout(layout)
        self.work_area.addWidget(page)

        return page

    def generate_report_by_type(self, report_type):
        date_to = QDate.currentDate().toString("yyyy-MM-dd")
        date_from = QDate.currentDate().addMonths(-1).toString("yyyy-MM-dd")

        try:
            report_data = ""

            if report_type == "sales_period":
                report_data = self.generate_sales_period_report(date_from, date_to)
            elif report_type == "sales_employees":
                report_data = self.generate_sales_by_employee_report(date_from, date_to)
            elif report_type == "income_expenses":
                report_data = self.generate_income_expenses_report(date_from, date_to)
            elif report_type == "avg_check":
                report_data = self.generate_average_check_report(date_from, date_to)
            elif report_type == "sales_analysis":
                report_data = self.generate_sales_analysis_report(date_from, date_to)
            elif report_type == "profitability_analysis":
                report_data = self.generate_profitability_analysis_report(date_from, date_to)

            self.report_text.setPlainText(report_data)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось оформить отчёт: {str(e)}")

    def generate_profitability_analysis_report(self, date_from, date_to):
        try:
            report = "АНАЛИЗ РЕНТАБЕЛЬНОСТИ\n"
            report += f"Период: {date_from} - {date_to}\n"
            report += "=" * 80 + "\n\n"

            report += "ОСНОВНЫЕ ПОКАЗАТЕЛИ РЕНТАБЕЛЬНОСТИ:\n"
            report += "-" * 50 + "\n"

            main_query = """
            SELECT 
                ROUND(SUM(p.Количество * (
                    SELECT COALESCE(p2.Себестоимость, 0) 
                    FROM Поставки p2 
                    WHERE p2.Мебель_idМебель = m.idМебель 
                    AND p2.Тип_операции = 'Поставка' 
                    ORDER BY p2.Дата DESC 
                    LIMIT 1
                ) * (1 + COALESCE(c.Надценка, 0) / 100)), 2) as total_revenue,
                ROUND(SUM(p.Количество * (
                    SELECT COALESCE(p2.Себестоимость, 0) 
                    FROM Поставки p2 
                    WHERE p2.Мебель_idМебель = m.idМебель 
                    AND p2.Тип_операции = 'Поставка' 
                    ORDER BY p2.Дата DESC 
                    LIMIT 1
                )), 2) as total_cost
            FROM Заказ z
            JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
            JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
            LEFT JOIN Категория c ON m.Категория_idКатегории = c.idКатегории
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            AND z.Статус IN ('Размещён', 'В процессе', 'Выполнен')
            """

            main_result = db.execute_query(main_query, (date_from, date_to))

            if main_result and main_result[0]:
                total_revenue = main_result[0][0] if main_result[0][0] else 0.0
                total_cost = main_result[0][1] if main_result[0][1] else 0.0

                if total_cost > 0:
                    profit = total_revenue - total_cost
                    profitability = (profit / total_cost) * 100
                    markup = ((total_revenue - total_cost) / total_cost) * 100

                    report += f"  Выручка: {total_revenue:.2f} руб\n"
                    report += f"  Себестоимость: {total_cost:.2f} руб\n"
                    report += f"  Прибыль: {profit:.2f} руб\n"
                    report += f"  Рентабельность: {profitability:.2f}%\n"
                    report += f"  Наценка: {markup:.2f}%\n"
                else:
                    report += "  Нет данных о продажах за выбранный период\n"
            else:
                report += "  Нет данных о продажах за выбранный период\n"

            report += "\n\n"

            report += "РЕНТАБЕЛЬНОСТЬ ПО КАТЕГОРИЯМ:\n"
            report += "-" * 70 + "\n"
            report += f"{'Категория':<25} {'Выручка':<12} {'Себест.':<12} {'Рентаб.':<12} {'Наценка':<12}\n"
            report += "-" * 70 + "\n"

            category_query = """
            SELECT 
                c.Наименование as category,
                ROUND(SUM(p.Количество * (
                    SELECT COALESCE(p2.Себестоимость, 0) 
                    FROM Поставки p2 
                    WHERE p2.Мебель_idМебель = m.idМебель 
                    AND p2.Тип_операции = 'Поставка' 
                    ORDER BY p2.Дата DESC 
                    LIMIT 1
                ) * (1 + c.Надценка / 100)), 2) as revenue,
                ROUND(SUM(p.Количество * (
                    SELECT COALESCE(p2.Себестоимость, 0) 
                    FROM Поставки p2 
                    WHERE p2.Мебель_idМебель = m.idМебель 
                    AND p2.Тип_операции = 'Поставка' 
                    ORDER BY p2.Дата DESC 
                    LIMIT 1
                )), 2) as cost,
                SUM(p.Количество) as total_items
            FROM Категория c
            LEFT JOIN Мебель m ON c.idКатегории = m.Категория_idКатегории
            LEFT JOIN ПозицииВзаказе p ON m.idМебель = p.Мебель_idМебель
            LEFT JOIN Заказ z ON p.Заказ_idЗаказ = z.idЗаказ
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            GROUP BY c.idКатегории
            HAVING total_items > 0
            ORDER BY revenue DESC
            """

            category_result = db.execute_query(category_query, (date_from, date_to))

            if category_result:
                for row in category_result:
                    category = row[0] if row[0] else "Без категории"
                    revenue = row[1] if row[1] else 0.0
                    cost = row[2] if row[2] else 0.0

                    if cost > 0:
                        profit_category = revenue - cost
                        profitability_category = (profit_category / cost) * 100
                        markup_category = ((revenue - cost) / cost) * 100

                        report += f"{category:<25} {revenue:<12.2f} {cost:<12.2f} {profitability_category:<12.2f}% {markup_category:<12.2f}%\n"
                    else:
                        report += f"{category:<25} {revenue:<12.2f} {cost:<12.2f} {'-':<12} {'-':<12}\n"
            else:
                report += "  Нет данных\n"

            report += "\n\n"

            report += "3. ТОП-5 САМЫХ РЕНТАБЕЛЬНЫХ ТОВАРОВ:\n"
            report += "-" * 70 + "\n"

            top_profit_query = """
            SELECT 
                m.Наименование as product_name,
                c.Наименование as category,
                SUM(p.Количество) as total_sold,
                ROUND(SUM(p.Количество * (
                    SELECT COALESCE(p2.Себестоимость, 0) 
                    FROM Поставки p2 
                    WHERE p2.Мебель_idМебель = m.idМебель 
                    AND p2.Тип_операции = 'Поставка' 
                    ORDER BY p2.Дата DESC 
                    LIMIT 1
                ) * (1 + COALESCE(c.Надценка, 0) / 100)), 2) as revenue,
                ROUND(SUM(p.Количество * (
                    SELECT COALESCE(p2.Себестоимость, 0) 
                    FROM Поставки p2 
                    WHERE p2.Мебель_idМебель = m.idМебель 
                    AND p2.Тип_операции = 'Поставка' 
                    ORDER BY p2.Дата DESC 
                    LIMIT 1
                )), 2) as cost
            FROM Мебель m
            LEFT JOIN Категория c ON m.Категория_idКатегории = c.idКатегории
            LEFT JOIN ПозицииВзаказе p ON m.idМебель = p.Мебель_idМебель
            LEFT JOIN Заказ z ON p.Заказ_idЗаказ = z.idЗаказ
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            GROUP BY m.idМебель, m.Наименование, c.Наименование
            HAVING total_sold > 0 AND cost > 0
            ORDER BY (revenue - cost) / cost DESC
            LIMIT 5
            """

            top_profit_result = db.execute_query(top_profit_query, (date_from, date_to))

            if top_profit_result:
                for i, row in enumerate(top_profit_result, 1):
                    product = row[0] if row[0] else "Неизвестный товар"
                    category = row[1] if row[1] else "Без категории"
                    sold = row[2] if row[2] else 0
                    revenue = row[3] if row[3] else 0.0
                    cost = row[4] if row[4] else 0.0

                    if cost > 0:
                        profit_item = revenue - cost
                        profitability_item = (profit_item / cost) * 100

                        if len(product) > 25:
                            product = product[:22] + "..."

                        report += f"  {i}. {product:<25} ({category})\n"
                        report += f"     Продано: {sold} шт, Прибыль: {profit_item:.2f} руб, Рентабельность: {profitability_item:.2f}%\n"
            else:
                report += "  Нет данных\n"

            report += "\n\n"

            report += "АНАЛИЗ ЭФФЕКТИВНОСТИ:\n"
            report += "-" * 40 + "\n"

            if main_result and main_result[0] and total_cost > 0:
                profitability = ((total_revenue - total_cost) / total_cost) * 100

                if profitability > 50:
                    report += "  Оценка: ОТЛИЧНАЯ рентабельность (>50%)\n"
                elif profitability > 30:
                    report += "  Оценка: ХОРОШАЯ рентабельность (30-50%)\n"
                elif profitability > 15:
                    report += "  Оценка: СРЕДНЯЯ рентабельность (15-30%)\n"
                elif profitability > 0:
                    report += "  Оценка: НИЗКАЯ рентабельность (0-15%)\n"
                else:
                    report += "  Оценка: УБЫТОЧНО\n"

                avg_profit_per_item = (total_revenue - total_cost) / total_cost * 100 if total_cost > 0 else 0
                report += f"\n  Средняя рентабельность на товар: {avg_profit_per_item:.2f}%\n"

            return report

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить отчёт: {str(e)}")

    def generate_sales_period_report(self, date_from, date_to):
        try:
            query = """
            SELECT 
                DATE(z.Дата) as date,
                COUNT(DISTINCT z.idЗаказ) as order_count,
                SUM(p.Количество) as total_items,
                ROUND(SUM(p.Количество * 1000), 2) as total_revenue  -- Упрощенный расчет
            FROM Заказ z
            JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            GROUP BY DATE(z.Дата)
            ORDER BY date
            """

            result = db.execute_query(query, (date_from, date_to))

            report = "ОТЧЕТ: ПРОДАЖИ ЗА ПЕРИОД\n"
            report += f"Период: {date_from} - {date_to}\n"
            report += "=" * 60 + "\n\n"
            report += f"{'Дата':<12} {'Заказов':<10} {'Товаров':<10} {'Выручка (руб)':<15}\n"
            report += "-" * 60 + "\n"

            total_orders = 0
            total_items = 0
            total_revenue = 0.0

            for row in result:
                date_obj = row[0]
                if date_obj:
                    date_str = date_obj.strftime("%Y-%m-%d") if hasattr(date_obj, 'strftime') else str(date_obj)
                else:
                    date_str = "Нет даты"

                orders = int(row[1]) if row[1] else 0
                items = int(row[2]) if row[2] else 0
                revenue = float(row[3]) if row[3] else 0.0

                report += f"{date_str:<12} {orders:<10} {items:<10} {revenue:<15.2f}\n"

                total_orders += orders
                total_items += items
                total_revenue += revenue

            report += "-" * 60 + "\n"
            report += f"{'ИТОГО':<12} {total_orders:<10} {total_items:<10} {total_revenue:<15.2f}\n"

            return report

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить отчёт: {str(e)}")

    def generate_sales_by_employee_report(self, date_from, date_to):
        try:
            query = """
            SELECT 
                CONCAT(s.Фамилия, ' ', s.Имя) as employee_name,
                d.Наименование as position,
                COUNT(DISTINCT z.idЗаказ) as order_count,
                SUM(p.Количество) as total_items,
                ROUND(SUM(
                    p.Количество * 
                    COALESCE(c.Надценка, 10) / 100 *  -- Простая наценка 10%% если нет данных
                    1000  -- Базовая цена 1000 руб за единицу для упрощения
                ), 2) as total_revenue
            FROM Сотрудники s
            JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
            LEFT JOIN Заказ z ON s.idСотрудника = z.Сотрудники_idСотрудника
            LEFT JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
            LEFT JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
            LEFT JOIN Категория c ON m.Категория_idКатегории = c.idКатегории
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            GROUP BY s.idСотрудника, s.Фамилия, s.Имя, d.Наименование
            ORDER BY total_revenue DESC
            """

            result = db.execute_query(query, (date_from, date_to))

            report = "ОТЧЕТ: ПРОДАЖИ ПО СОТРУДНИКАМ\n"
            report += f"Период: {date_from} - {date_to}\n"
            report += "=" * 80 + "\n\n"
            report += f"{'Сотрудник':<25} {'Должность':<15} {'Заказов':<10} {'Товаров':<10} {'Выручка (руб)':<15}\n"
            report += "-" * 80 + "\n"

            total_orders = 0
            total_items = 0
            total_revenue = 0.0

            for row in result:
                employee = row[0] if row[0] else "Не назначен"
                position = row[1] if row[1] else "Не указана"
                orders = int(row[2]) if row[2] else 0
                items = int(row[3]) if row[3] else 0
                revenue = float(row[4]) if row[4] else 0.0

                report += f"{employee:<25} {position:<15} {orders:<10} {items:<10} {revenue:<15.2f}\n"

                total_orders += orders
                total_items += items
                total_revenue += revenue

            report += "-" * 80 + "\n"
            report += f"{'ИТОГО':<41} {total_orders:<10} {total_items:<10} {total_revenue:<15.2f}\n"

            if total_revenue > 0:
                avg_per_employee = total_revenue / len(result) if result else 0
                report += f"\nСредняя выручка на сотрудника: {avg_per_employee:.2f} руб\n"

            return report

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить отчёт: {str(e)}")

    def generate_income_expenses_report(self, date_from, date_to):
        try:
            report = "ДОХОДЫ И РАСХОДЫ\n"
            report += f"Период: {date_from} - {date_to}\n"
            report += "=" * 60 + "\n\n"

            income_query = """
            SELECT 
                ROUND(SUM(p.Количество * 1000), 2) as total_income  # Базовая цена 1000 руб
            FROM Заказ z
            JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            AND z.Статус IN ('Размещён', 'В процессе', 'Выполнен')
            """

            income_result = db.execute_query(income_query, (date_from, date_to))
            total_income = float(income_result[0][0]) if income_result and income_result[0][0] else 0.0

            expenses_query = """
            SELECT 
                ROUND(SUM(p.Количество * p.Себестоимость), 2) as total_expenses
            FROM Поставки p
            WHERE DATE(p.Дата) BETWEEN %s AND %s
            AND p.Тип_операции = 'Поставка'
            """

            expenses_result = db.execute_query(expenses_query, (date_from, date_to))
            total_expenses = float(expenses_result[0][0]) if expenses_result and expenses_result[0][0] else 0.0

            salary_query = """
            SELECT 
                ROUND(SUM(d.Оклад), 2) as total_salary
            FROM Сотрудники s
            JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
            """

            salary_result = db.execute_query(salary_query)
            total_salary = float(salary_result[0][0]) if salary_result and salary_result[0][0] else 0.0

            report += "ДОХОДЫ:\n"
            report += f"  Выручка от продаж: {total_income:.2f} руб\n\n"

            report += "РАСХОДЫ:\n"
            report += f"  Закупка товаров: {total_expenses:.2f} руб\n"
            report += f"  Зарплаты сотрудников (ежемесячно): {total_salary:.2f} руб\n\n"

            total_expenses_all = total_expenses + total_salary
            report += f"  Всего расходов: {total_expenses_all:.2f} руб\n\n"

            # Финансовый результат
            financial_result = total_income - total_expenses_all
            report += "ФИНАНСОВЫЙ РЕЗУЛЬТАТ:\n"
            report += f"  Прибыль/Убыток: {financial_result:.2f} руб\n"

            if financial_result > 0:
                report += "  Результат: ПРИБЫЛЬ\n"
            elif financial_result < 0:
                report += "  Результат: УБЫТОК\n"
            else:
                report += "  Результат: БЕЗУБЫТОЧНО\n"

            return report

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить отчёт: {str(e)}")

    def generate_average_check_report(self, date_from, date_to):
        try:
            query = """
            SELECT 
                DATE(z.Дата) as date,
                COUNT(DISTINCT z.idЗаказ) as order_count,
                ROUND(SUM(p.Количество * 1000), 2) as total_revenue,
                ROUND(SUM(p.Количество * 1000) / COUNT(DISTINCT z.idЗаказ), 2) as avg_check
            FROM Заказ z
            JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            GROUP BY DATE(z.Дата)
            ORDER BY date
            """

            result = db.execute_query(query, (date_from, date_to))

            report = "СРЕДНИЙ ЧЕК\n"
            report += f"Период: {date_from} - {date_to}\n"
            report += "=" * 70 + "\n\n"
            report += f"{'Дата':<12} {'Заказов':<10} {'Выручка (руб)':<15} {'Средний чек (руб)':<15}\n"
            report += "-" * 70 + "\n"

            total_orders = 0
            total_revenue = 0.0

            for row in result:
                date_obj = row[0]
                if date_obj:
                    date_str = date_obj.strftime("%Y-%m-%d") if hasattr(date_obj, 'strftime') else str(date_obj)
                else:
                    date_str = "Нет даты"

                orders = int(row[1]) if row[1] else 0

                # Преобразуем Decimal в float
                revenue = float(row[2]) if row[2] else 0.0
                avg_check = float(row[3]) if row[3] else 0.0

                report += f"{date_str:<12} {orders:<10} {revenue:<15.2f} {avg_check:<15.2f}\n"

                total_orders += orders
                total_revenue += revenue

            overall_avg = total_revenue / total_orders if total_orders > 0 else 0

            report += "-" * 70 + "\n"
            report += f"{'ИТОГО':<12} {total_orders:<10} {total_revenue:<15.2f} {overall_avg:<15.2f}\n\n"

            report += "АНАЛИЗ СРЕДНЕГО ЧЕКА:\n"
            report += "-" * 40 + "\n"

            if result:
                valid_values = []
                for row in result:
                    if row[3] is not None:
                        valid_values.append(float(row[3]))

                if valid_values:
                    max_avg = max(valid_values)
                    min_avg = min(valid_values)

                    report += f"  Максимальный средний чек: {max_avg:.2f} руб\n"
                    report += f"  Минимальный средний чек: {min_avg:.2f} руб\n"
                    report += f"  Общий средний чек: {overall_avg:.2f} руб\n"

                    if overall_avg > 0 and len(result) >= 2:
                        first_row = result[0]
                        last_row = result[-1]

                        if first_row[3] and float(first_row[3]) > 0:
                            first_avg = float(first_row[3])
                            last_avg = float(last_row[3]) if last_row[3] else 0
                            change_percent = ((last_avg - first_avg) / first_avg) * 100
                            report += f"  Изменение за период: {change_percent:+.1f}%\n"

            return report

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить отчёт: {str(e)}")

    def generate_sales_analysis_report(self, date_from, date_to):
        try:
            report = "АНАЛИЗ ПРОДАЖ\n"
            report += f"Период: {date_from} - {date_to}\n"
            report += "=" * 60 + "\n\n"

            report += "ПРОДАЖИ ПО КАТЕГОРИЯМ:\n"
            report += "-" * 40 + "\n"

            category_query = """
            SELECT 
                c.Наименование as category,
                SUM(p.Количество) as total_items,
                ROUND(SUM(p.Количество * 1000), 2) as revenue  # Базовая цена 1000 руб
            FROM Категория c
            LEFT JOIN Мебель m ON c.idКатегории = m.Категория_idКатегории
            LEFT JOIN ПозицииВзаказе p ON m.idМебель = p.Мебель_idМебель
            LEFT JOIN Заказ z ON p.Заказ_idЗаказ = z.idЗаказ
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            GROUP BY c.idКатегории
            ORDER BY revenue DESC
            """

            category_result = db.execute_query(category_query, (date_from, date_to))

            if category_result:
                for row in category_result:
                    category = row[0] if row[0] else "Без категории"
                    items = row[1] if row[1] else 0
                    revenue = row[2] if row[2] else 0.0

                    report += f"  {category:<20}: {items:>5} шт, {revenue:>10.2f} руб\n"
            else:
                report += "  Нет данных\n"

            report += "\n\n"

            report += "ТОП-10 ТОВАРОВ ПО ПРОДАЖАМ:\n"
            report += "-" * 40 + "\n"

            top_products_query = """
            SELECT 
                m.Наименование as product_name,
                SUM(p.Количество) as total_sold,
                ROUND(SUM(p.Количество * 1000), 2) as revenue  # Базовая цена 1000 руб
            FROM Мебель m
            LEFT JOIN ПозицииВзаказе p ON m.idМебель = p.Мебель_idМебель
            LEFT JOIN Заказ z ON p.Заказ_idЗаказ = z.idЗаказ
            WHERE DATE(z.Дата) BETWEEN %s AND %s
            GROUP BY m.idМебель
            ORDER BY total_sold DESC
            LIMIT 10
            """

            top_result = db.execute_query(top_products_query, (date_from, date_to))

            if top_result:
                for i, row in enumerate(top_result, 1):
                    product = row[0] if row[0] else "Неизвестный товар"
                    sold = row[1] if row[1] else 0
                    revenue = row[2] if row[2] else 0.0

                    # Обрезаем слишком длинные названия
                    if len(product) > 30:
                        product = product[:27] + "..."

                    report += f"  {i:2}. {product:<30}: {sold:>5} шт, {revenue:>10.2f} руб\n"
            else:
                report += "  Нет данных\n"

            return report

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить отчёт: {str(e)}")

    # Методы загрузки данных
    def load_catalog_data(self):
        query = """
                    SELECT 
                        m.idМебель,
                        m.Наименование,
                        c.Наименование,
                        mat.Наименование,
                        m.Производитель,
                        col.Наименование,
                        m.Габариты,
                        m.Вес,
                        m.Количество,
                        COALESCE(ROUND(
                            (SELECT p.Себестоимость 
                            FROM Поставки p 
                            WHERE p.Мебель_idМебель = m.idМебель AND Тип_операции = 'Поставка'
                            ORDER BY p.Дата DESC 
                            LIMIT 1) * (1 + COALESCE(c.Надценка, 0) / 100), 2), 0) as price
                    FROM Мебель m
                    LEFT JOIN Категория c ON m.Категория_idКатегории = c.idКатегории
                    LEFT JOIN Материал mat ON m.Материал_idМатериал = mat.idМатериал
                    LEFT JOIN Цвет col ON m.Цвет_idЦвет = col.idЦвет
                    ORDER BY m.idМебель
                    """

        furniture_data = db.execute_query(query)
        self.all_catalog_data = furniture_data

        self.catalog_table.setRowCount(len(furniture_data))

        for row_idx, row_data in enumerate(furniture_data):
            for col_idx, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data) if cell_data is not None else "")
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                if col_idx in [7, 8, 9]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                elif col_idx in [0, 1, 4, 6]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.catalog_table.setItem(row_idx, col_idx, item)

        self.load_catalog_filter_data()

    def load_supplies_data(self):
        query = """
                    SELECT 
                        p.idПоставки,
                        p.Дата,
                        p.Тип_операции,
                        m.Наименование,
                        m.Производитель,
                        p.Количество,
                        p.Себестоимость
                    FROM Поставки p
                    JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
                    ORDER BY p.idПоставки 
                    LIMIT 100
                    """
        result = db.execute_query(query)

        self.all_supplies_data = result

        self.supplies_table.setRowCount(len(result))
        for row_idx, row in enumerate(result):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                if col_idx in [0, 5, 6]:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

                self.supplies_table.setItem(row_idx, col_idx, item)

    def load_employees_cards(self):
        self.clear_employee_selection()

        for i in reversed(range(self.employees_cards_layout.count())):
            widget = self.employees_cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        try:
            query = """
            SELECT 
                s.Фамилия,
                s.Имя,
                s.Отчество,
                d.Наименование as Должность,
                s.телефон,
                p.email as Должность,
                DATE_FORMAT(s.Дата_рождения, '%%d.%%m.%%Y') as Дата_рождения,
                d.Оклад as Оклад,
                s.График_работы,
                s.idСотрудника
            FROM Сотрудники s
            JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
            LEFT JOIN Пароли p ON s.Пароли_idПароли = p.idПароли  
            ORDER BY s.idСотрудника
            """
            employees = db.execute_query(query)

            if not employees:
                no_data_label = QLabel("Сотрудники не найдены")
                no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_data_label.setStyleSheet("font-size: 16px; color: #888; padding: 50px;")
                self.employees_cards_layout.addWidget(no_data_label, 0, 0, 1, 2)
                return

            for i, employee in enumerate(employees):
                card = self.create_employee_card({
                    "surname": employee[0],
                    "name": employee[1],
                    "patronymic": employee[2],
                    "position": employee[3],
                    "phone": employee[4],
                    "email": employee[5] if employee[5] else "Не указан",
                    "birth_date": employee[6],
                    "salary": employee[7] if employee[7] else 0,
                    "schedule": employee[8] if employee[8] else "Не указан",
                    "id": employee[9]
                })

                row = i // 2
                col = i % 2
                self.employees_cards_layout.addWidget(card, row, col)

        except Exception as e:
            QMessageBox.critical(self,"Ошибка",  f"Не удалось загрузить сотрудников: {str(e)}")

    def load_cash_filters_data(self):
        category_query = "SELECT DISTINCT Наименование FROM Категория ORDER BY Наименование"
        categories = db.execute_query(category_query)

        material_query = "SELECT DISTINCT Наименование FROM Материал ORDER BY Наименование"
        materials = db.execute_query(material_query)

        color_query = "SELECT DISTINCT Наименование FROM Цвет ORDER BY Наименование"
        colors = db.execute_query(color_query)

        self.category_filter_combo_catalog.clear()
        self.category_filter_combo_catalog.addItem("Все категории")
        for category in categories:
            if category[0]:
                self.category_filter_combo_catalog.addItem(category[0])

        self.material_filter_combo_catalog.clear()
        self.material_filter_combo_catalog.addItem("Материал")
        for material in materials:
            if material[0]:
                self.material_filter_combo_catalog.addItem(material[0])

        self.color_filter_combo_catalog.clear()
        self.color_filter_combo_catalog.addItem("Цвет")
        for color in colors:
            if color[0]:
                self.color_filter_combo_catalog.addItem(color[0])

        self.category_filter_combo_cart.clear()
        self.category_filter_combo_cart.addItem("Все категории")
        for category in categories:
            if category[0]:
                self.category_filter_combo_cart.addItem(category[0])

        self.material_filter_combo_cart.clear()
        self.material_filter_combo_cart.addItem("Материал")
        for material in materials:
            if material[0]:
                self.material_filter_combo_cart.addItem(material[0])

        self.color_filter_combo_cart.clear()
        self.color_filter_combo_cart.addItem("Цвет")
        for color in colors:
            if color[0]:
                self.color_filter_combo_cart.addItem(color[0])

    def load_categories_for_filters(self):
        query = "SELECT DISTINCT Наименование FROM Категория ORDER BY Наименование"
        result = db.execute_query(query)

        self.category_filter_combo_catalog.clear()
        self.category_filter_combo_cart.clear()

        self.category_filter_combo_catalog.addItem("Все категории")
        self.category_filter_combo_cart.addItem("Все категории")

        for row in result:
            category_name = row[0]
            self.category_filter_combo_catalog.addItem(category_name)
            self.category_filter_combo_cart.addItem(category_name)

    def load_catalog_data_cash(self):
        query = """
                    SELECT 
                        m.Наименование,
                        mat.Наименование ,
                        m.Производитель,
                        col.Наименование,
                        m.Габариты,
                        m.Вес,
                        m.Количество,
                        COALESCE(ROUND(
                            (SELECT p.Себестоимость 
                            FROM Поставки p 
                            WHERE p.Мебель_idМебель = m.idМебель AND Тип_операции = 'Поставка'
                            ORDER BY p.Дата DESC 
                            LIMIT 1) * (1 + COALESCE(c.Надценка, 0) / 100), 2), 0) as price,
                        c.Наименование,
                        m.idМебель as furniture_id
                    FROM Мебель m
                    LEFT JOIN Категория c ON m.Категория_idКатегории = c.idКатегории
                    LEFT JOIN Материал mat ON m.Материал_idМатериал = mat.idМатериал
                    LEFT JOIN Цвет col ON m.Цвет_idЦвет = col.idЦвет
                    WHERE m.Количество > 0
                    ORDER BY m.Наименование
                    LIMIT 100
                    """
        result = db.execute_query(query)

        self.catalog_data_cash = []

        self.catalog_table_cash.setRowCount(len(result))
        for row_idx, row in enumerate(result):
            row_data = {
                'name': row[0],
                'material': row[1],
                'producer': row[2],
                'color': row[3],
                'dimensions': row[4],
                'weight': row[5],
                'quantity': row[6],
                'price': row[7],
                'category': row[8],
                'furniture_id': row[9],
                'catalog_row': row_idx
            }
            self.catalog_data_cash.append(row_data)

            for col_idx, value in enumerate(row[:8]):
                item = QTableWidgetItem(str(value) if value else "")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.catalog_table_cash.setItem(row_idx, col_idx, item)

    def load_orders_data(self):
        try:
            query = """
            SELECT 
                z.idЗаказ,
                k.ФИО as client_name,
                GROUP_CONCAT(DISTINCT m.Наименование SEPARATOR ', ') as furniture_items,
                COALESCE(SUM(p.Количество), 0) as total_quantity,
                z.Дата,
                GROUP_CONCAT(DISTINCT du.вид SEPARATOR ', ') as additional_services,
                z.Статус,
                COALESCE(
                    SUM(p.Количество * 
                        (SELECT COALESCE(p2.Себестоимость, 0) 
                         FROM Поставки p2 
                         WHERE p2.Мебель_idМебель = m.idМебель 
                           AND p2.Тип_операции = 'Поставка' 
                         ORDER BY p2.Дата DESC 
                         LIMIT 1) * 
                        (1 + COALESCE((
                            SELECT Надценка 
                            FROM Категория cat 
                            WHERE cat.idКатегории = m.Категория_idКатегории
                        ), 0) / 100)
                    ), 0
                ) as total_cost,
                par.email
            FROM Заказ z
            JOIN Клиент k ON z.Клиент_idКлиент = k.idКлиент
            LEFT JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
            LEFT JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
            LEFT JOIN ДопУслуги_has_Заказ dhz ON z.idЗаказ = dhz.Заказ_idЗаказ
            LEFT JOIN ДопУслуги du ON dhz.ДопУслуги_idДопУслуги = du.idДопУслуги
            LEFT JOIN Сотрудники s ON z.Сотрудники_idСотрудника = s.idСотрудника
            LEFT JOIN Пароли par ON s.Пароли_idПароли = par.idПароли  -- Соединяем с таблицей паролей для email
            GROUP BY z.idЗаказ, k.ФИО, z.Дата, z.Статус, par.email
            ORDER BY z.idЗаказ 
            LIMIT 50
            """

            result = db.execute_query(query)

            self.orders_table.setRowCount(len(result))

            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value) if value else "")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    if col_idx == 4 and value:
                        try:
                            date_obj = datetime.strptime(str(value), "%Y-%m-%d %H:%M:%S")
                            item.setText(date_obj.strftime("%d.%m.%Y %H:%M"))
                        except:
                            pass

                    if col_idx == 7 and value:
                        item.setText(f"{float(value):.2f} руб")

                    if col_idx == 8 and value and len(str(value)) > 20:
                        item.setText(str(value)[:20] + "...")

                    self.orders_table.setItem(row_idx, col_idx, item)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка",f"Не удалось оформить отчёт: {str(e)}")


    def load_clients_cards(self):
        for i in reversed(range(self.clients_cards_layout.count())):
            widget = self.clients_cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        try:
            query = """
            SELECT 
                k.idКлиент,
                k.ФИО,
                k.email,
                k.телефон
            FROM Клиент k
            ORDER BY k.ФИО
            LIMIT 20
            """

            clients = db.execute_query(query)

            if not clients:
                no_data_label = QLabel("Клиенты не найдены")
                no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.clients_cards_layout.addWidget(no_data_label, 0, 0, 1, 2)
                return

            for i, client in enumerate(clients):
                last_order_query = """
                SELECT 
                    z.idЗаказ,
                    m.Наименование,
                    z.Статус,
                    z.Дата
                FROM Заказ z
                LEFT JOIN ПозицииВзаказе pz ON z.idЗаказ = pz.Заказ_idЗаказ
                LEFT JOIN Мебель m ON pz.Мебель_idМебель = m.idМебель
                WHERE z.Клиент_idКлиент = %s
                GROUP BY z.idЗаказ, m.Наименование, z.Статус, z.Дата
                ORDER BY z.Дата DESC
                LIMIT 3
                """
                orders = db.execute_query(last_order_query, (client[0],))

                seller_query = """
                SELECT 
                    CONCAT(s.Фамилия, ' ', s.Имя, ' ', COALESCE(s.Отчество, '')) as seller_name,
                    p.email as seller_email
                FROM Заказ z
                LEFT JOIN Сотрудники s ON z.Сотрудники_idСотрудника = s.idСотрудника
                LEFT JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
                WHERE z.Клиент_idКлиент = %s
                ORDER BY z.Дата DESC
                LIMIT 1
                """
                seller_result = db.execute_query(seller_query, (client[0],))

                orders_info = ""
                seller_info = ""

                if orders:
                    order_lines = []
                    seen_orders = set()

                    for order in orders:
                        order_id = order[0]
                        if order_id and order_id not in seen_orders:
                            seen_orders.add(order_id)
                            status_display = "в процессе" if order[2] == "В процессе" else order[2].lower()
                            order_lines.append(f"-Заказ N {order_id} - {status_display}")

                    orders_info = "\n".join(order_lines)

                if seller_result and seller_result[0]:
                    seller_data = seller_result[0]
                    if seller_data[0] and seller_data[1]:
                        seller_info = f"{seller_data[0]} ({seller_data[1]})"
                    elif seller_data[0]:
                        seller_info = seller_data[0]
                    elif seller_data[1]:
                        seller_info = f"Продавец ({seller_data[1]})"


                card = self.create_client_card({
                    "id": client[0],
                    "name": client[1] if client[1] else "Не указано",
                    "email": client[2] if client[2] else "Не указан",
                    "phone": client[3] if client[3] else "Не указан",
                    "orders_info": orders_info,
                    "seller_info": seller_info
                })

                row = i // 2
                col = i % 2
                self.clients_cards_layout.addWidget(card, row, col)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить клиентов: {str(e)}")

    def load_clients_data(self):
        try:
            query = """
            SELECT 
                ФИО,
                email,
                телефон,
                COALESCE((SELECT COUNT(*) FROM Заказ WHERE Клиент_idКлиент = Клиент.idКлиент), 0) as order_count,
                DATE_FORMAT(COALESCE((SELECT MAX(Дата) FROM Заказ WHERE Клиент_idКлиент = Клиент.idКлиент), NOW()), '%%d.%%m.%%Y') as last_order
            FROM Клиент
            ORDER BY ФИО
            LIMIT 50
            """
            result = db.execute_query(query)

            self.clients_table.setRowCount(len(result))
            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value) if value else "")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.clients_table.setItem(row_idx, col_idx, item)

        except Exception as e:
            print(f"Ошибка загрузки клиентов: {e}")

    def load_clients_orders_data(self):
        try:
            query = """
            SELECT 
                k.ФИО,
                k.email,
                k.телефон,
                z.idЗаказ,
                DATE_FORMAT(z.Дата, '%%d.%%m.%%Y %%H:%%i') as order_date,
                COALESCE((SELECT SUM( p.Количество) 
                 FROM ПозицииВзаказе p 
                 JOIN Мебель m ON p.Мебель_idМебель = m.idМебель 
                 WHERE p.Заказ_idЗаказ = z.idЗаказ), 0) as total
            FROM Клиент k
            INNER JOIN Заказ z ON k.idКлиент = z.Клиент_idКлиент
            ORDER BY z.Дата DESC
            LIMIT 50
            """
            result = db.execute_query(query)

            self.clients_orders_table.setRowCount(len(result))
            for row_idx, row in enumerate(result):
                for col_idx, value in enumerate(row):
                    item = QTableWidgetItem(str(value) if value else "")
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.clients_orders_table.setItem(row_idx, col_idx, item)

        except Exception as e:
            print(f"Ошибка загрузки данных клиентов: {e}")

    # Методы поиска
    def search_catalog(self):
        search_text = self.catalog_search.text().strip()

        if not search_text:
            self.load_catalog_data()
            return

        if not hasattr(self, 'all_catalog_data') or not self.all_catalog_data:
            return

        for row in range(self.catalog_table.rowCount()):
            show_row = False

            for col in [0, 1, 4]:
                if col < self.catalog_table.columnCount():
                    item = self.catalog_table.item(row, col)
                    if item:
                        cell_text = item.text()
                        if col == 0:
                            if cell_text == search_text:
                                show_row = True
                                break
                        elif col in [1, 4]:
                            if cell_text.lower() == search_text.lower():
                                show_row = True
                                break

            self.catalog_table.setRowHidden(row, not show_row)

    def search_supplies_data(self):
        search_text = self.supplies_search.text().strip()

        if not search_text:
            for row in range(self.supplies_table.rowCount()):
                self.supplies_table.setRowHidden(row, False)
            return

        for row in range(self.supplies_table.rowCount()):
            show_row = False

            item = self.supplies_table.item(row, 0)
            if item and item.text() == search_text:
                show_row = True
            else:
                for col in [1, 3, 4]:
                    if col < self.supplies_table.columnCount():
                        item = self.supplies_table.item(row, col)
                        if item and item.text().lower() == search_text.lower():
                            show_row = True
                            break

            self.supplies_table.setRowHidden(row, not show_row)

    def search_employees(self):
        search_text = self.employees_search.text().strip()

        if not search_text:
            self.load_employees_cards()
            return

        for i in reversed(range(self.employees_cards_layout.count())):
            widget = self.employees_cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        try:
            query = """
            SELECT 
                s.Фамилия,
                s.Имя,
                s.Отчество,
                d.Наименование as Должность,
                s.телефон,
                p.email,
                DATE_FORMAT(s.Дата_рождения, '%%d.%%m.%%Y') as Дата_рождения,
                d.Оклад,
                s.График_работы,
                s.idСотрудника
            FROM Сотрудники s
            JOIN Должность d ON s.Должность_idДолжности = d.idДолжности
            LEFT JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
            WHERE s.Фамилия LIKE %s 
               OR s.Имя LIKE %s 
               OR s.Отчество LIKE %s 
               OR d.Наименование LIKE %s
               OR p.email LIKE %s
            ORDER BY s.Фамилия, s.Имя
            """

            search_pattern = f"%{search_text}%"
            employees = db.execute_query(query, (search_pattern, search_pattern, search_pattern,
                                                 search_pattern, search_pattern))

            if not employees:
                no_data_label = QLabel("Сотрудники не найдены")
                no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_data_label.setStyleSheet("font-size: 16px; color: #888; padding: 50px;")
                self.employees_cards_layout.addWidget(no_data_label, 0, 0, 1, 2)
                return

            for i, employee in enumerate(employees):
                card = self.create_employee_card({
                    "surname": employee[0],
                    "name": employee[1],
                    "patronymic": employee[2],
                    "position": employee[3],
                    "phone": employee[4],
                    "email": employee[5] if employee[5] else "Не указан",
                    "birth_date": employee[6],
                    "salary": employee[7] if employee[7] else 0,
                    "schedule": employee[8] if employee[8] else "Не указан",
                    "id": employee[9]
                })

                row = i // 2
                col = i % 2
                self.employees_cards_layout.addWidget(card, row, col)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка поиска: {str(e)}")

    def search_cash_page(self):
        search_text = self.catalog_search_cash.text().strip()

        if not search_text:
            for row in range(self.catalog_table_cash.rowCount()):
                self.catalog_table_cash.setRowHidden(row, False)
            return

        for row in range(self.catalog_table_cash.rowCount()):
            show_row = False

            for col in [0, 2]:
                if col < self.catalog_table_cash.columnCount():
                    item = self.catalog_table_cash.item(row, col)
                    if item and item.text().lower() == search_text.lower():
                        show_row = True
                        break

            self.catalog_table_cash.setRowHidden(row, not show_row)

    def search_cart_cash(self):
        search_text = self.cart_search_input.text().strip()

        if not search_text:
            for row in range(self.cart_table.rowCount()):
                self.cart_table.setRowHidden(row, False)
            return

        for row in range(self.cart_table.rowCount()):
            show_row = False

            for col in [0, 2]:
                if col < self.cart_table.columnCount():
                    item = self.cart_table.item(row, col)
                    if item and item.text().lower() == search_text.lower():
                        show_row = True
                        break

            self.cart_table.setRowHidden(row, not show_row)

    def search_orders_page(self):
        search_text = self.orders_search_input.text().strip().lower()

        if not search_text:
            for row in range(self.orders_table.rowCount()):
                self.orders_table.setRowHidden(row, False)

            self.orders_table.clearSelection()

            self.status_placed_checkbox.setEnabled(False)
            self.status_in_process_checkbox.setEnabled(False)
            self.status_completed_checkbox.setEnabled(False)

            self.status_button_group.setExclusive(False)
            self.status_placed_checkbox.setChecked(False)
            self.status_in_process_checkbox.setChecked(False)
            self.status_completed_checkbox.setChecked(False)
            self.status_button_group.setExclusive(True)

            return

        for row in range(self.orders_table.rowCount()):
            self.orders_table.setRowHidden(row, True)

        search_columns = [0, 1, 8]

        search_words = search_text.split()

        for row in range(self.orders_table.rowCount()):
            should_show = False

            for col in search_columns:
                item = self.orders_table.item(row, col)
                if item:
                    cell_text = item.text().lower()

                    all_words_match = True
                    for word in search_words:
                        if word not in cell_text.split():
                            all_words_match = False
                            break

                    if all_words_match:
                        should_show = True
                        break

            if should_show:
                self.orders_table.setRowHidden(row, False)

        self.orders_table.clearSelection()

        self.status_placed_checkbox.setEnabled(False)
        self.status_in_process_checkbox.setEnabled(False)
        self.status_completed_checkbox.setEnabled(False)

        self.status_button_group.setExclusive(False)
        self.status_placed_checkbox.setChecked(False)
        self.status_in_process_checkbox.setChecked(False)
        self.status_completed_checkbox.setChecked(False)
        self.status_button_group.setExclusive(True)

    def search_clients_page(self):
        search_text = self.clients_search.text().strip()

        if not search_text:
            self.load_clients_cards()
            return

        for i in reversed(range(self.clients_cards_layout.count())):
            widget = self.clients_cards_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        try:
            query = """
            SELECT DISTINCT
                k.idКлиент,
                k.ФИО,
                k.email,
                k.телефон
            FROM Клиент k
            LEFT JOIN Заказ z ON k.idКлиент = z.Клиент_idКлиент
            LEFT JOIN Сотрудники s ON z.Сотрудники_idСотрудника = s.idСотрудника
            LEFT JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
            WHERE k.ФИО LIKE %s 
               OR k.email LIKE %s 
               OR p.email LIKE %s
            ORDER BY k.ФИО
            LIMIT 20
            """

            search_pattern = f"%{search_text}%"
            clients = db.execute_query(query, (search_pattern, search_pattern, search_pattern))

            if not clients:
                no_data_label = QLabel("Клиенты не найдены")
                no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.clients_cards_layout.addWidget(no_data_label, 0, 0, 1, 2)
                return

            for i, client in enumerate(clients):
                last_order_query = """
                SELECT 
                    z.idЗаказ,
                    z.Статус
                FROM Заказ z
                WHERE z.Клиент_idКлиент = %s
                ORDER BY z.Дата DESC
                LIMIT 3
                """
                orders = db.execute_query(last_order_query, (client[0],))

                seller_query = """
                SELECT 
                    CONCAT(s.Фамилия, ' ', s.Имя, ' ', COALESCE(s.Отчество, '')) as seller_name,
                    p.email as seller_email
                FROM Заказ z
                LEFT JOIN Сотрудники s ON z.Сотрудники_idСотрудника = s.idСотрудника
                LEFT JOIN Пароли p ON s.Пароли_idПароли = p.idПароли
                WHERE z.Клиент_idКлиент = %s
                ORDER BY z.Дата DESC
                LIMIT 1
                """
                seller_result = db.execute_query(seller_query, (client[0],))

                orders_info = ""
                seller_info = ""

                if orders:
                    order_lines = []
                    seen_orders = set()

                    for order in orders:
                        order_id = order[0]
                        if order_id and order_id not in seen_orders:
                            seen_orders.add(order_id)
                            status_display = "в процессе" if order[1] == "В процессе" else order[1].lower()
                            order_lines.append(f"-Заказ N {order_id} - {status_display}")

                    orders_info = "\n".join(order_lines)

                if seller_result and seller_result[0]:
                    seller_data = seller_result[0]
                    if seller_data[0] and seller_data[1]:
                        seller_info = f"{seller_data[0]} ({seller_data[1]})"
                    elif seller_data[0]:
                        seller_info = seller_data[0]
                    elif seller_data[1]:
                        seller_info = f"Продавец ({seller_data[1]})"
                else:
                    orders_info = "Нет заказов" if not orders_info else orders_info

                card = self.create_client_card({
                    "id": client[0],
                    "name": client[1] if client[1] else "Не указано",
                    "email": client[2] if client[2] else "Не указан",
                    "phone": client[3] if client[3] else "Не указан",
                    "orders_info": orders_info,
                    "seller_info": seller_info
                })

                row = i // 2
                col = i % 2
                self.clients_cards_layout.addWidget(card, row, col)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка поиска: {str(e)}")

    def search_cash_items(self):
        search_text = self.cash_search_input.text().lower().strip()
        selected_category = self.category_filter_combo_cash.currentText()

        if not search_text and selected_category == "Все категории":
            for row in range(self.cash_table.rowCount()):
                self.cash_table.setRowHidden(row, False)
            return

        for row in range(self.cash_table.rowCount()):
            should_show = True

            if selected_category != "Все категории":
                if hasattr(self, 'cart_data') and self.cart_data:
                    item_category = None
                    for cart_item in self.cart_data:
                        if cart_item['row'] == row:
                            item_category = cart_item.get('category')
                            break

                    if item_category != selected_category:
                        should_show = False
                else:
                    item_name = self.cash_table.item(row, 0).text().lower()
                    if selected_category.lower() not in item_name:
                        should_show = False

            if search_text and should_show:
                should_show = False
                for col in range(self.cash_table.columnCount()):
                    item = self.cash_table.item(row, col)
                    if item and search_text in item.text().lower():
                        should_show = True
                        break

            self.cash_table.setRowHidden(row, not should_show)

    # Методы генерации отчетов
    def generate_report(self):
        report_type = self.report_type_combo.currentText()
        date_from = self.report_date_from.date().toString("yyyy-MM-dd")
        date_to = self.report_date_to.date().toString("yyyy-MM-dd")

        try:
            report_text = f"Отчет: {report_type}\n"
            report_text += f"Период: {date_from} - {date_to}\n"
            report_text += "=" * 50 + "\n\n"

            if report_type == "Отчёт по продажам":
                query = """
                SELECT 
                    DATE(z.Дата) as date,
                    COUNT(*) as order_count,
                    SUM(p.Количество) as total_items,
                    SUM(p.Количество) as total_revenue
                FROM Заказ z
                JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
                JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
                WHERE DATE(z.Дата) BETWEEN %s AND %s
                GROUP BY DATE(z.Дата)
                ORDER BY date
                """
                result = db.execute_query(query, (date_from, date_to))

                report_text += "Дата          | Заказы | Товары | Выручка\n"
                report_text += "-" * 45 + "\n"

                for row in result:
                    report_text += f"{row[0]} | {row[1]:6d} | {row[2]:6d} | {row[3]:10.2f} руб\n"

            elif report_type == "Отчёт по выручке":
                query = """
                SELECT 
                    m.Наименование,
                    SUM(p.Количество) as sold_quantity,
                    SUM( p.Количество) as revenue
                FROM ПозицииВзаказе p
                JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
                JOIN Заказ z ON p.Заказ_idЗаказ = z.idЗаказ
                WHERE DATE(z.Дата) BETWEEN %s AND %s
                GROUP BY m.idМебель
                ORDER BY revenue DESC
                LIMIT 20
                """
                result = db.execute_query(query, (date_from, date_to))

                report_text += "Товар                          | Продано | Выручка\n"
                report_text += "-" * 50 + "\n"

                total_revenue = 0
                for row in result:
                    name = row[0][:30] + "..." if len(row[0]) > 30 else row[0]
                    report_text += f"{name:30s} | {row[1]:7d} | {row[2]:10.2f} руб\n"
                    total_revenue += row[2]

                report_text += f"\nОбщая выручка: {total_revenue:.2f} руб\n"

            elif report_type == "Отчёт по среднему чеку":
                query = """
                SELECT 
                    COUNT(*) as order_count,
                    SUM(p.Количество) as total_revenue,
                    AVG( p.Количество) as avg_check
                FROM Заказ z
                JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
                JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
                WHERE DATE(z.Дата) BETWEEN %s AND %s
                """
                result = db.execute_query(query, (date_from, date_to))

                if result and result[0]:
                    row = result[0]
                    report_text += f"Количество заказов: {row[0]}\n"
                    report_text += f"Общая выручка: {row[1]:.2f} руб\n"
                    report_text += f"Средний чек: {row[2]:.2f} руб\n"

            self.report_text.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self,"Ошибка",  f"Не удалось сформировать отчёт: {str(e)}")

    def generate_cash_report(self):
        report_type = self.cash_report_combo.currentText()

        try:
            if report_type == "Продажи за сегодня":
                query = """
                SELECT 
                    COUNT(*) as orders_today,
                    SUM(p.Количество) as items_today,
                    SUM(p.Количество) as revenue_today
                FROM Заказ z
                JOIN ПозицииВзаказе p ON z.idЗаказ = p.Заказ_idЗаказ
                JOIN Мебель m ON p.Мебель_idМебель = m.idМебель
                WHERE DATE(z.Дата) = CURDATE()
                """
                result = db.execute_query(query)

                if result and result[0]:
                    row = result[0]
                    report_text = "Продажи за сегодня:\n\n"
                    report_text += f"Заказов: {row[0]}\n"
                    report_text += f"Товаров продано: {row[1]}\n"
                    report_text += f"Выручка: {row[2]:.2f} руб\n"
                    self.cash_report_text.setText(report_text)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сформировать отчёт: {str(e)}")

    def modify_furniture(self,action_type):
        furniture_id = None

        if action_type == 'edit':
            current_row = self.catalog_table.currentRow()

            if current_row >= 0:
                furniture_id_item = self.catalog_table.item(current_row, 0)
                if furniture_id_item:
                    furniture_id = furniture_id_item.text()

        dialog = FurnitureDialog(self, furniture_id, action_type)

        if dialog.exec():
            self.load_catalog_data()
            self.load_catalog_data_cash()
            if action_type in ['supply', 'write_off']:
                self.load_supplies_data()

    def add_employee(self):
        dialog = EmployeeDialog(self)
        if dialog.exec():
            self.load_employees_cards()

    def modify_employee(self):
        dialog = EmployeeDialog(self, self.selected_employee_id)
        if dialog.exec():
            self.load_employees_cards()
            self.clear_employee_selection()