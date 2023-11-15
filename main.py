import os
import sys
import random
import sqlite3 as sl
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QPixmap
from PyQt5.QtWidgets import QWidget, QTableView, QApplication, QMessageBox, QDialog
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog, QPushButton, QDoubleSpinBox, QPlainTextEdit,\
    QCheckBox, QRadioButton, QGridLayout, QButtonGroup, QVBoxLayout, QWidget, QSpinBox, QInputDialog, QStatusBar

class welcome_modal(QtWidgets.QWidget):
    def __init__(self):
        super(welcome_modal, self).__init__()
        self.WINDOW2()
    def WINDOW2(self):
        self.setGeometry(400, 300, 270, 140)
        self.setWindowTitle('Здравствуйте')

        self.passbutton = QPushButton(self)
        self.passbutton.setText('Продолжить')
        self.passbutton.move(10, 60)
        self.passbutton.resize(250, 40)
        self.passbutton.clicked.connect(self.passdef)

        self.inputname_label = QLabel(self)
        self.inputname_label.setText('Введите ваше имя:')
        self.inputname_label.move(10, 10)
        self.inputname = QPlainTextEdit(self)
        self.inputname.move(10, 25)
        self.inputname.resize(100, 30)

        self.themes_label = QLabel(self)
        self.themes_label.setText('Выберите тему:')
        self.themes_label.move(120, 10)
        self.theme_label_white = QLabel(self)
        self.theme_label_white.setText('Светлая')
        self.theme_label_white.move(120, 45)
        self.theme_label_black = QLabel(self)
        self.theme_label_black.setText('Серая')
        self.theme_label_black.move(170, 45)
        self.theme_label_green = QLabel(self)
        self.theme_label_green.setText('Зеленая')
        self.theme_label_green.move(220, 45)
        self.theme_white = QRadioButton(self)
        self.theme_white.move(120, 30)
        self.theme_white.setChecked(True)
        self.theme_black = QRadioButton(self)
        self.theme_black.move(170, 30)
        self.theme_green = QRadioButton(self)
        self.theme_green.move(220, 30)
        self.theme_box = QButtonGroup(self)
        self.theme_box.addButton(self.theme_white)
        self.theme_box.addButton(self.theme_black)
        self.theme_box.addButton(self.theme_green)
        self.theme_array = [self.theme_white, self.theme_black, self.theme_green]

    def passdef(self):
        con = sl.connect("settings.sqlite")
        cur = con.cursor()
        if self.inputname.toPlainText() != '':
            text = self.inputname.toPlainText()
            cur.execute("""UPDATE settings_table SET text = ? WHERE id = 2""", (text, ))
            for i in self.theme_array:
                if self.theme_white.isChecked():
                    cur.execute("""UPDATE settings_table SET theme = 'white' WHERE id = 3""")
                    break
                elif self.theme_black.isChecked():
                    cur.execute("""UPDATE settings_table SET theme = 'black' WHERE id = 3""")
                    break
                elif self.theme_green.isChecked():
                    cur.execute("""UPDATE settings_table SET theme = 'green' WHERE id = 3""")
                    break
            con.commit()
            con.close()
            QWidget.close(self)
        else:
            self.showerror()

    def showerror(self):
        infoBox = QMessageBox()
        infoBox.setText("Ошибка")
        infoBox.setInformativeText("Не выбрано ни одного параметра!")
        infoBox.setWindowTitle("Внимание")
        infoBox.setStandardButtons(QMessageBox.Ok)
        infoBox.setIcon(QMessageBox.Critical)
        infoBox.setWindowIcon(QtGui.QIcon('icon.png'))
        infoBox.exec_()


    def closeEvent(self, e):
        result = QtWidgets.QMessageBox.question(self, "Продолжить|Закрыть?",
           "Вы действительно хотите продолжить|закрыть?",
           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
           QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            e.accept()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()

class Modal(QtWidgets.QWidget): #КЛАСС МОДАЛЬНОГО ОКНА
    def __init__(self):
        super(Modal, self).__init__()
        self.WINDOW()
    def WINDOW(self):
        self.setGeometry(300, 300, 500, 440)
        self.setWindowTitle('Настройки')

        self.savebtn = QPushButton(self)
        self.savebtn.setText('Сохранить')
        self.savebtn.resize(125, 30)
        self.savebtn.move(335, 380)
        self.savebtn.clicked.connect(self.savesettings)

        self.label = QLabel(self)
        self.label.setText('Выберите тему')
        self.label.move(20, 5)

        label1 = QLabel(self)
        pixmap = QPixmap('Screenshot_1.png')
        label1.setPixmap(pixmap)
        label1.move(20, 20)

        label2 = QLabel(self)
        pixmap = QPixmap('Screenshot_2.png')
        label2.setPixmap(pixmap)
        label2.move(20, 120)

        label3 = QLabel(self)
        pixmap = QPixmap('Screenshot_3.png')
        label3.setPixmap(pixmap)
        label3.move(20, 220)

        self.label1_btn = QRadioButton(self)
        self.label1_btn.move(210, 20)
        self.label2_btn = QRadioButton(self)
        self.label2_btn.move(210, 120)
        self.label3_btn = QRadioButton(self)
        self.label3_btn.move(210, 220)

        self.labals_box = QButtonGroup(self)
        self.labals_box.addButton(self.label1_btn)
        self.labals_box.addButton(self.label2_btn)
        self.labals_box.addButton(self.label3_btn)
        self.labals_box_grid = [self.label1_btn, self.label2_btn, self.label3_btn]

        con = sl.connect("settings.sqlite")
        cur = con.cursor()
        res = cur.execute('''SELECT theme FROM settings_table WHERE id = 3''').fetchone()
        if res[0] == 'white':
            self.label2_btn.setChecked(True)
        elif res[0] == 'black':
            self.label1_btn.setChecked(True)
        else:
            self.label3_btn.setChecked(True)
        res = cur.execute('''SELECT text FROM settings_table WHERE id = 2''').fetchone()
        self.unamelabel = QLabel(self)
        self.unamelabel.setText(f'Ваше текущее имя:{res[0]}')
        self.unamelabel.move(300, 10)

        self.changename_btn = QPushButton(self)
        self.changename_btn.setText('Изменить')
        self.changename_btn.move(350, 25)
        self.changename_btn.clicked.connect(self.changenameshowDialog)
        con.commit()
        con.close()

    def changenameshowDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Введите новое имя:')
        if ok:
            name = str(text)
            con = sl.connect("settings.sqlite")
            cur = con.cursor()
            cur.execute('''UPDATE settings_table SET text = ? WHERE id = 2''', (name,))
            con.commit()
            con.close()


    def savesettings(self):
        con = sl.connect("settings.sqlite")
        cur = con.cursor()
        if self.label2_btn.isChecked():
            cur.execute('''UPDATE settings_table SET theme = 'white' WHERE id = 3''')
        elif self.label1_btn.isChecked():
            cur.execute('''UPDATE settings_table SET theme = 'black' WHERE id = 3''')
        else:
            cur.execute('''UPDATE settings_table SET theme = 'green' WHERE id = 3''')
        con.commit()
        con.close()
        self.showsavesettings()

    def showsavesettings(self):
        infoBox = QMessageBox()
        infoBox.setText("Сохранение")
        infoBox.setInformativeText("Изменения вступят в силу после перезапуска")
        infoBox.setWindowTitle("Внимание")
        infoBox.setStandardButtons(QMessageBox.Ok)
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setWindowIcon(QtGui.QIcon('icon.png'))
        infoBox.exec_()

class MyPillow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Главное окно
        self.setGeometry(400, 400, 1200, 600)
        con = sl.connect("settings.sqlite")
        cur = con.cursor()
        res = cur.execute('''SELECT text FROM settings_table WHERE id = 2''').fetchone()
        self.setWindowTitle(f'Generator - {res[0]}')
        theme = cur.execute('''SELECT theme FROM settings_table WHERE id = 3''').fetchone()
        if theme[0] == 'black':
            oImage = QImage("gray.jpg")
            sImage = oImage.scaled(QSize(1200, 600))
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(sImage))
            self.setPalette(palette)
        elif theme[0] == 'green':
            oImage = QImage("green.jpg")
            sImage = oImage.scaled(QSize(1200, 600))
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(sImage))
            self.setPalette(palette)
        else:
            pass
        con.commit()
        con.close()

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        #Кнопка генерации пароля(ей)
        self.button_pass = QPushButton(self)
        self.button_pass.setText('Генерировать')
        self.button_pass.move(50, 470)
        self.button_pass.resize(600, 50)
        self.button_pass.clicked.connect(self.generate)

        #Кнопка очистки вывода паролей
        self.button_clear = QPushButton(self)
        self.button_clear.setText('Очистить')
        self.button_clear.move(50, 530)
        self.button_clear.resize(335, 30)
        self.button_clear.clicked.connect(self.cleartext)

        #Вывод пароля
        self.answer = QPlainTextEdit(self)
        self.answer.resize(600, 400)
        self.answer.move(50, 50)

        #Вывод названия окна вывода текста
        self.name_answer = QLabel(self)
        self.name_answer.setText('Пароли:')
        self.name_answer.resize(200, 20)
        self.name_answer.move(50, 30)
        self.name_answer.setDisabled(False)

        #Ввод кол-ва символов пароля
        self.name_numsym = QLabel(self)
        self.name_numsym.setText('Количество символов:')
        self.name_numsym.move(700, 30)
        self.name_numsym.resize(120, 20)
        self.numsym = QSpinBox(self)
        self.numsym.setMinimum(6)
        self.numsym.setMaximum(24)
        self.numsym.setValue(6)
        self.numsym.move(700, 50)
        self.numsym.resize(200, 30)

        #Ввод кол-ва паролей
        self.name_numsym = QLabel(self)
        self.name_numsym.setText('Количество паролей:')
        self.name_numsym.move(900, 30)
        self.name_numsym.resize(120, 20)
        self.numpass = QSpinBox(self)
        self.numpass.setMinimum(1)
        self.numpass.setMaximum(50)
        self.numpass.setValue(1)
        self.numpass.move(900, 50)
        self.numpass.resize(200, 30)

        #Выбор экстренных символов
        self.extrasym = QCheckBox(self)
        self.extrasym.move(700, 100)
        self.name_extrasym = QLabel(self)
        self.name_extrasym.setText('Добавить символы')
        self.name_extrasym.move(700, 80)
        self.name_extrasym.resize(120, 30)
        self.extrasym.clicked.connect(self.pre_extrasymbuttons)

        #Дополнительная ф-я ввода своего набора символов
        self.myextrasyms = QPlainTextEdit(self)
        self.myextrasyms.move(1000, 100)
        self.myextrasyms.resize(100, 25)
        self.myextrasyms.setEnabled(False)
        self.myextrasyms_label = QLabel(self)
        self.myextrasyms_label.setText('Введите символы')
        self.myextrasyms_label.setEnabled(False)
        self.myextrasyms_label.move(1000, 80)

        self.myextrasymsradiobutton1 = QRadioButton(self)
        self.myextrasymsradiobutton1.move(850, 100)
        self.myextrasymsradiobutton1.setChecked(True)
        self.myextrasymsradiobutton1.setEnabled(False)
        self.myextrasymsradiobutton2 = QRadioButton(self)
        self.myextrasymsradiobutton2.move(900, 100)
        self.myextrasymsradiobutton2.setEnabled(False)

        self.extrasym_button_group = QButtonGroup(self)
        self.extrasym_button_group.addButton(self.myextrasymsradiobutton1)
        self.extrasym_button_group.addButton(self.myextrasymsradiobutton2)

        self.extrasym_button_group.buttonClicked.connect(self.extrasymbuttons)

        #Надписи символов
        self.exstrasym1_label = QLabel(self)
        self.exstrasym1_label.setText('Любые')
        self.exstrasym1_label.move(850, 80)
        self.exstrasym2_label = QLabel(self)
        self.exstrasym2_label.setText('Свои')
        self.exstrasym2_label.move(900, 80)
        self.exstrasym1_label.setEnabled(False)
        self.exstrasym2_label.setEnabled(False)

        #Добавление цифр в пароль
        self.nums = QCheckBox(self)
        self.nums.move(700, 140)
        self.name_nums = QLabel(self)
        self.name_nums.setText('Добавить цифры')
        self.name_nums.move(700, 120)
        self.name_nums.resize(120, 30)

        #Добавить буквы в пароль
        self.letters = QCheckBox(self)
        self.letters.move(700, 180)
        self.letters.setChecked(True)
        self.letters.clicked.connect(self.letterscheck)
        self.name_letters = QLabel(self)
        self.name_letters.setText('Добавить буквы')
        self.name_letters.move(700, 160)
        self.name_letters.resize(120, 30)

        #БЛОК СОХРАНЕНИЯ В TXT
        self.saveas_button = QPushButton(self)
        self.saveas_button.setText('Сохранить как')
        self.saveas_button.resize(90, 30)
        self.saveas_button.move(390, 530)
        self.saveas_button.clicked.connect(self.saveasfile)

        self.save_button = QPushButton(self)
        self.save_button.setText('Сохранить')
        self.save_button.resize(90, 30)
        self.save_button.move(480, 530)
        self.save_button.clicked.connect(self.savefile)
        self.save_button.setEnabled(False)

        self.open_button = QPushButton(self)
        self.open_button.setText('Открыть')
        self.open_button.resize(90, 30)
        self.open_button.move(570, 530)
        self.open_button.clicked.connect(self.openfile)

        #ОБЪЕДИНЕНИЕ ВСЕХ ПАРАМЕТРОВ
        self.checkboxex_group = [self.extrasym, self.nums, self.letters]

        #Радио-кнопки выбора регистра
        self.label = QLabel('Current')

        self.radio_button_1 = QRadioButton(self)
        self.radio_button_1.move(900, 180)
        self.radio_button_1.setChecked(True)

        self.radio_button_2 = QRadioButton(self)
        self.radio_button_2.move(1000, 180)
        self.radio_button_3 = QRadioButton(self)
        self.radio_button_3.move(1100, 180)

        self.name_radio_button_1 = QLabel(self)
        self.name_radio_button_1.setText('Любые')
        self.name_radio_button_1.move(890, 160)
        self.name_radio_button_2 = QLabel(self)
        self.name_radio_button_2.setText('Заглавные')
        self.name_radio_button_2.move(980, 160)
        self.name_radio_button_3 = QLabel(self)
        self.name_radio_button_3.setText('Строчные')
        self.name_radio_button_3.move(1080, 160)

        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_button_1)
        self.button_group.addButton(self.radio_button_2)
        self.button_group.addButton(self.radio_button_3)

        self.button_group.buttonClicked.connect(self._on_radio_button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.radio_button_1)
        layout.addWidget(self.radio_button_2)
        layout.addWidget(self.radio_button_3)

        self.setLayout(layout)

        #КНОПКА ВТОРОГО ОКНА(МОДАЛЬНОГО)
        self.secondwindow = QPushButton(self)
        self.secondwindow.setText("Настройки")
        self.secondwindow.resize(180, 35)
        self.secondwindow.clicked.connect(self.opensecondwindow)

        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self)
        self.setLayout(self.vbox)
        self.count = 0

    def _on_radio_button_clicked(self, button):
        print(button)
        self.label.setText('Current: ' + button.text())

    def pre_extrasymbuttons(self):
        if self.extrasym.isChecked():
            self.myextrasymsradiobutton1.setEnabled(True)
            self.myextrasymsradiobutton2.setEnabled(True)
            self.exstrasym1_label.setEnabled(True)
            self.exstrasym2_label.setEnabled(True)
            if self.myextrasymsradiobutton2.isChecked():
                self.myextrasyms_label.setEnabled(True)
                self.myextrasyms.setEnabled(True)
            else:
                self.myextrasyms_label.setEnabled(False)
                self.myextrasyms.setEnabled(False)
        else:
            self.myextrasymsradiobutton1.setEnabled(False)
            self.myextrasymsradiobutton2.setEnabled(False)
            self.exstrasym1_label.setEnabled(False)
            self.exstrasym2_label.setEnabled(False)
            self.myextrasymsradiobutton1.setChecked(True)
            self.myextrasyms.setEnabled(False)

    def extrasyminput(self):
        self.extrasymsletters = '!#$%&()*+-./:;<=>?@[\]^_`{|}~'
        if self.myextrasymsradiobutton1.isChecked():
            return self.extrasymsletters
        elif self.myextrasymsradiobutton2.isChecked() and self.myextrasyms.toPlainText() != '':
            return self.myextrasyms.toPlainText()
        else:
            return ''
        pass

    def extrasymbuttons(self):
        if self.myextrasymsradiobutton2.isChecked():
            self.myextrasyms.setEnabled(True)
        else:
            self.myextrasyms.setEnabled(False)


    def letterscheck(self):
        if not self.letters.isChecked():
            self.radio_button_1.setEnabled(False)
            self.name_radio_button_1.setEnabled(False)
            self.radio_button_2.setEnabled(False)
            self.name_radio_button_2.setEnabled(False)
            self.radio_button_3.setEnabled(False)
            self.name_radio_button_3.setEnabled(False)
        else:
            self.radio_button_1.setEnabled(True)
            self.name_radio_button_1.setEnabled(True)
            self.radio_button_2.setEnabled(True)
            self.name_radio_button_2.setEnabled(True)
            self.radio_button_3.setEnabled(True)
            self.name_radio_button_3.setEnabled(True)
        pass

    def pre_generate(self): #Фунция проверяет все чекбоксы и готовит набор символов для генерации пароля
        abc = 'abcdefghigklmnopqrstuvyxwz'
        ABC = 'ABCDEFGHIGKLMNOPQRSTUVYXWZ'
        nums = '1234567890'
        self.extrasymsletters = '!#$%&()*+-./:;<=>?@[\]^_`{|}~'
        self.passlet = ''
        for i in self.checkboxex_group:
            if i.isChecked():
                if self.checkboxex_group.index(i) == 0:
                    self.passlet += self.extrasyminput()
                elif self.checkboxex_group.index(i) == 1:
                    self.passlet += nums
                elif self.checkboxex_group.index(i) == 2:
                    if self.radio_button_1.isChecked():
                        self.passlet += abc + ABC
                    elif self.radio_button_2.isChecked():
                        self.passlet += ABC
                    else:
                        self.passlet += abc
        return self.passlet


    def generate(self): #ГЕНЕРАЦИЯ паролей
        if self.pre_generate() != '':
            passw = self.passlet
            self.status.showMessage('Работаем')
            for i in range(self.numpass.value()):
                self.count += 1
                pas = ''
                for x in range(self.numsym.value()):
                    pas = pas + random.choice(list(passw))  # Символы, из которых будет составлен пароль
                self.answer.appendPlainText(f'{pas} <--- пароль №{self.count}')
        else:
            self.status.showMessage('Выберите параметры')
            self.showerror()

    def cleartext(self): #очистка вывода
        self.count = 0
        self.answer.clear()

    def showerror(self):
        infoBox = QMessageBox()
        infoBox.setText("Ошибка")
        infoBox.setInformativeText("Не выбрано ни одного параметра!")
        infoBox.setWindowTitle("Внимание")
        infoBox.setStandardButtons(QMessageBox.Ok)
        infoBox.setIcon(QMessageBox.Critical)
        infoBox.setWindowIcon(QtGui.QIcon('icon.png'))
        infoBox.exec_()

    def opensecondwindow(self):
        self.app2 = Modal()
        self.app2.show()

    def showDialog(self):
        default_dir = "/home/qt_user/Documents"
        default_filename = os.path.join(default_dir)
        self.saveasfilename, _ = QFileDialog.getSaveFileName(
            self, "Save audio file", default_filename, "Txt files (*.txt)"
        )
        if self.saveasfilename:
            return self.saveasfilename
        else:
            pass

    def openDialog(self):
        default_dir = "/home/qt_user/Documents"
        default_filename = os.path.join(default_dir)
        self.openfilename, _ = QFileDialog.getOpenFileName(
            self, "Сохранить текстовый документ", default_filename, "Txt files (*.txt)"
        )
        if self.openfilename:
            return self.openfilename

    def savefile(self):
        self.filenameopensave.write(self.answer.toPlainText())
        self.filenameopensave.close()
        self.save_button.setEnabled(False)
        self.open_button.setEnabled(True)
        self.cleartext()
        self.answer.appendPlainText(self.data)

    def openfile(self):
        name = self.openDialog()
        if name != None:
            self.data = self.answer.toPlainText()
            self.filenameopensave = open(name, 'r+')
            dataopen = self.filenameopensave
            self.cleartext()
            for i in dataopen:
                self.answer.appendPlainText(i.rstrip())
            self.save_button.setEnabled(True)
            self.open_button.setEnabled(False)

    def saveasfile(self):
        name = self.showDialog()
        if name != None:
            filename = open(name, 'w')
            filename.write(self.answer.toPlainText())
            filename.close()

    def closeEvent(self, e):
        result = QtWidgets.QMessageBox.question(self, "Подтверждение закрытия окна",
           "Вы действительно хотите закрыть окно?",
           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
           QtWidgets.QMessageBox.No)
        if result == QtWidgets.QMessageBox.Yes:
            e.accept()
            QtWidgets.QWidget.closeEvent(self, e)
        else:
            e.ignore()

if __name__ == "__main__":
    con = sl.connect("settings.sqlite")
    cur = con.cursor()
    result = cur.execute("""SELECT parameters FROM settings_table
                WHERE id = 1""").fetchone()
    if result[0] == 0:
        app1 = QApplication(sys.argv)
        window = welcome_modal()
        cur.execute("""UPDATE settings_table SET parameters = 1 WHERE id = 1""")
        con.commit()
        con.close()
        window.show()
        app1.exec_()
    else:
        pass
    app = QApplication(sys.argv)
    window = MyPillow()
    window.show()
    sys.exit(app.exec())