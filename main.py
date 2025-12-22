import sys
from PyQt6.QtWidgets import QApplication
from auth_window import AuthWindow
from main_window import MainWindow

def main():
    app = QApplication(sys.argv)

    auth_window = AuthWindow()

    def on_user_authenticated(user_data):
        auth_window.close()
        main_window = MainWindow(user_data)
        main_window.show()

    auth_window.user_authenticated.connect(on_user_authenticated)

    auth_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()