import sys
import hashlib
import pyperclip

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui


from HashGenerator import Ui_MainWindow_HashGenerator
# hash_alav --> hash algorithms_available
hash_alav = list(hashlib.algorithms_available)
hash_alav.remove("md4")
hash_alav.remove("md5")
hash_alav.remove("sm3")
hash_alav.remove("mdc2")
hash_alav.remove("sha1")
hash_alav.remove("blake2b")
hash_alav.remove("blake2s")
hash_alav.remove("whirlpool")
hash_alav.remove("ripemd160")
hash_alav.remove("shake_128")
algorithms_list = hash_alav


class UiHashGenerator(QMainWindow):
    textfromfile = ""
    textfromopenfile = ""
    value = 0
    value100 = 0
    appendhashkist = []
    appendhash = ""
    counter = 0

    def __init__(self):
        QMainWindow.__init__(self)
        self.uihashgenerator = Ui_MainWindow_HashGenerator()
        self.uihashgenerator.setupUi(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.uihashgenerator.help_btn.clicked.connect(self.help)

        self.uihashgenerator.comboBox.addItems(algorithms_list)

        self.btns()
        self.show()

    def mousePressEvent(self, evt):
        self.oldpos = evt.globalPos()

    def mouseMoveEvent(self, evt):
        delta = QPoint(evt.globalPos() - self.oldpos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldpos = evt.globalPos()

    def btns(self):
        self.uihashgenerator.generatehash.clicked.connect(self.hashgenerator)
        self.uihashgenerator.selectfile.clicked.connect(self.selectpathh)
        self.uihashgenerator.pasttext.clicked.connect(self.textpaste)
        self.uihashgenerator.copyhash.clicked.connect(self.copyhash)



    def textpaste(self):
        self.uihashgenerator.yourtext.setPlainText(pyperclip.paste())

    def copyhash(self):
        if ((self.uihashgenerator.complete.text()) == "Complete ..."):
            try:
                pyperclip.copy(self.uihashgenerator.yourhash.toPlainText())
                msg = QMessageBox.information(self, "Copy Hash", "Hash Copied")
            except:
                pass
        else:
            msg = QMessageBox.information(self, "Copy Hash Error", "Please wait until hash is generated")
    def selectpathh(self):
        self.textfromfile = ""
        self.textfromopenfile = ""
        file = str(QFileDialog.getOpenFileName(self, "Select Path"))

        textfile  = list(file)
        textfile.remove("(")
        for i in textfile:
            self.textfromfile += i

        self.textfromfile = self.textfromfile[1:-1]
        self.textfromfile = self.textfromfile.split(",")[0]
        self.textfromfile = self.textfromfile.replace('/' , '\\')
        self.textfromfile = self.textfromfile[:2] + "\\" + self.textfromfile[2:-1]

        with open(self.textfromfile , "r") as text:

            for t in text:
                self.textfromopenfile += t

        self.uihashgenerator.yourtext.setPlainText(self.textfromopenfile)


    def hashgenerator(self):
        self.uihashgenerator.progressBar.setTextVisible(True)
        self.uihashgenerator.complete.setText("")
        self.value = 0
        self.value100 = 0
        self.appendhashkist = []
        self.appendhash = ""
        self.counter = 0

        select_algorithm = self.uihashgenerator.comboBox.currentText()
        textstring = str(self.uihashgenerator.yourtext.toPlainText())



        try:
            h = hashlib.new(str(select_algorithm))
            h.update(textstring.encode())
            # hh = h.hexdigest()
            self.hash = h.hexdigest()
            self.lentimer = len(self.hash)
            self.lentimerp = self.lentimer
            for i in self.hash:
                self.appendhashkist.append(i)

            self.timer = QTimer(self)
            self.timer.timeout.connect(self.timerr)
            self.timer.start(100)
        except:
            msg = QMessageBox.information(self, "Hash Algorithm Error", "Please select the Hash Algorithm")


    def timerr(self):

        if (self.lentimer > 0):


            self.appendhash = self.appendhash + self.appendhashkist[self.counter]
            self.counter += 1
            self.lentimer = self.lentimer - 1
            self.uihashgenerator.yourhash.setPlainText(self.appendhash)


            self.value100 += self.value
            self.uihashgenerator.progressBar.setValue(self.value)


            if self.value < self.lentimerp:
                self.value += 1

        else :
            if self.value100 > self.lentimerp:
                self.uihashgenerator.progressBar.setValue(100)
                self.timer.stop()
                self.uihashgenerator.progressBar.setTextVisible(False)
                self.uihashgenerator.complete.setText("Complete ...")

    def help(self):

            message_box = QtWidgets.QMessageBox()

            message_box.setWindowTitle("Developer information")
            message_box.setWindowIcon(QtGui.QIcon('royal_lionn.ico'))
            message_box.setIcon(QMessageBox.Information)

            message_box.setText("Developer : Amin Jafari\n"
                                "---------------------------------\n"
                                "Gmail : Aminjjjeffrey@gmail.com\n")
            message_box.exec_()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    root = UiHashGenerator()
    sys.exit(app.exec_())