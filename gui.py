import sys
from pathlib import Path


def main():
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("Для графічного інтерфейсу потрібна бібліотека PyQt6.")
        print("Встановіть її командою:  pip install -r requirements.txt")
        sys.exit(1)

    from app import build_app
    from GUI.viewmodel import GameViewModel, AnswerQueue
    from GUI.window import GameWindow

    data_dir = None
    for arg in sys.argv[1:]:
        if arg.startswith("--data-dir="):
            data_dir = Path(arg.split("=", 1)[1]).expanduser()

    qt_app = QApplication(sys.argv)
    answers = AnswerQueue()
    vm = GameViewModel(build_app(data_dir, reader=answers), answers)
    window = GameWindow(vm)
    window.show()
    sys.exit(qt_app.exec())


if __name__ == "__main__":
    main()
