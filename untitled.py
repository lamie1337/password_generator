import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtWidgets import QPlainTextEdit, QPushButton, QDoubleSpinBox, QStatusBar


class AntiPlagiarism(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1000, 1000, 800, 700)
        self.setWindowTitle('Антиплагиат v0.0001')

        self.text1 = QPlainTextEdit(self)
        self.text1.move(10, 100)
        self.text1.resize(360, 500)

        self.text2 = QPlainTextEdit(self)
        self.text2.move(420, 100)
        self.text2.resize(360, 500)

        self.label = QLabel('Текст 1', self)
        self.label.move(10, 80)

        self.label1 = QLabel('Текст 2', self)
        self.label1.move(420, 80)

        self.label2 = QLabel('Порог срабатывания (%)', self)
        self.label2.move(10, 25)

        self.alert_value = QDoubleSpinBox(self)
        self.alert_value.move(300, 15)
        self.alert_value.resize(480, 40)

        self.checkBtn = QPushButton('Сравнить', self)
        self.checkBtn.move(10, 610)
        self.checkBtn.resize(770, 30)
        self.checkBtn.clicked.connect(self.order)

        self.statusBar1 = QStatusBar()
        self.setStatusBar(self.statusBar1)

    def order(self):
        self.nums = []
        for x in range(0, 100):
            self.nums.append(x)
        self.count = 1
        self.count1 = 1
        path = self.text1.toPlainText()
        path1 = self.text2.toPlainText()
        lst = path.split('\n')
        lst1 = path1.split('\n')
        self.unics = []
        self.unicsa = []
        self.unicsb = []
        for i in lst:
            if i not in self.unics:
                self.unics.append(i)
                self.count += 1
            else:
                pass

        for i in lst1:
            if i not in self.unics and i not in lst:
                self.unics.append(i)
                self.count += 1
            else:
                pass

        for i in lst:
            if i in lst1 and i not in self.unicsa:
                self.count1 += 2
                self.unicsa.append(i)

        x = ((int(len(self.unicsa)) / int(len(self.unics))) * 100)
        self.ans = x
        if int(self.alert_value.value()) <= int(((int(len(self.unicsa)) / int(len(self.unics))) * 100)):
            self.statusBar1.showMessage(f'Тексты похожи на '
                                        f'{self.ans:.2f}%'
                                        f', плагиат')
        else:
            self.statusBar1.showMessage(f'Тексты похожи на '
                                        f'{self.ans:.2f}%'
                                        f', не плагиат')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AntiPlagiarism()
    ex.show()
    sys.exit(app.exec())
