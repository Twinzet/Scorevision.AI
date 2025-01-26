import sys, glob, os, shutil
from PySide2.QtGui import QColor, QMovie, QIntValidator
from PySide2.QtCore import QSize, QRunnable, QThreadPool,QUrl, QObject, Signal, QByteArray, QBuffer, Qt, QMargins, QFileInfo
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QFileDialog, QLabel, QGraphicsOpacityEffect, QTextBrowser, QFrame, QProgressBar, QVBoxLayout, QScrollArea, QLineEdit
from depend import *
from lyAnalysis import *

class Signals(QObject):
    error = Signal(int)
    max = Signal(int)
    addIt = Signal()
    finished = Signal()
    currentPath = Signal(str)
    showLayout2 = Signal()
    makeBox = Signal(str)

class Worker(QRunnable):

    def __init__(self,sourceFolder,fileName):
        super().__init__()
        self.signal = Signals()
        self.sourceFolder = sourceFolder
        self.fileName = fileName

    def run(self):
        if self.sourceFolder != "Select path":

            maxBar = len([name for name in os.listdir('Duplicates') if os.path.isfile(name)])
            currBar = len([name for name in os.listdir('PngOutput') if os.path.isfile(name)])
            self.signal.max.emit(maxBar)
            
            print(self.fileName)

            convert(self.fileName)
            while True:
                if maxBar == currBar:
                    break
                else:
                    continue
                

            self.signal.showLayout2.emit()
            self.signal.finished.emit()

        else:
            if self.sourceFolder == "Select path":
                self.signal.error.emit(0)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.filename = ""

        folderIcon = self.resource_path('resources\\folderIcon.png')
        logoTitle = self.resource_path('resources\\scorevisionlogo.png')
        pauseBack = self.resource_path('resources\\pause-back.png')
        pauseBack1 = self.resource_path('resources\\pause-back1.png')

        self.setWindowTitle("Scorevison.AI")
        self.setFixedSize(QSize(728, 728))

        self.wWidth = 728
        self.wHeight = 728

        self.eWidth = 1600
        self.eHeight = 900

        self.layoutWidget = QWidget(self)

        self.sourceFolder = "Select path"

        self.backImage = QLabel(self.layoutWidget)
        self.backImage.setFixedSize(QSize(self.wWidth, self.wHeight))

        frameDirHeight = self.wHeight * 0.97
        frameDirWidth = self.wWidth * 0.8
        self.frameBox = QLabel(self.layoutWidget)
        self.frameBox.setStyleSheet("background-color: black")
        self.frameBox.setFixedSize(QSize(frameDirWidth, frameDirHeight))
        self.frameBox.move((self.wWidth - frameDirWidth) / 2, (self.wHeight - frameDirHeight) / 2)

        self.titleLogo = QLabel(self.layoutWidget)
        self.titleLogo.setStyleSheet(f"Border-image: url({logoTitle})")
        self.titleLogo.setFixedSize(self.wWidth / 1.7, self.wHeight / 3.3)
        self.titleLogo.move(self.wWidth / 6, self.wHeight / 18.2)

        idealRations = self.wHeight / 26

        sourceFrameHeight = self.wHeight * 0.025
        sourceFrameWidth = self.wWidth * 0.6
        sourceFrameMove = self.wHeight / 2.4
        self.sourceFrame = QLabel(self.layoutWidget)
        self.sourceFrame.setText(" Select path")
        self.sourceFrame.setStyleSheet("background-color: white; color: grey")
        self.sourceFrame.setFixedSize(QSize(sourceFrameWidth, sourceFrameHeight))
        self.sourceFrame.move((self.wWidth - sourceFrameWidth) / 2, sourceFrameMove + idealRations)

        secondFrameDirHeight = self.eHeight * 0.98
        secondFrameDirWidth = self.eWidth * 0.976
        self.secondFrame = QLabel(self.layoutWidget)
        self.secondFrame.setStyleSheet("background-color: white")
        self.secondFrame.setFixedSize(QSize(secondFrameDirWidth, secondFrameDirHeight))
        self.secondFrame.move((self.eWidth - secondFrameDirWidth) / 2, (self.eHeight - secondFrameDirHeight) / 2)

        self.sourceLabel = QLabel(self.layoutWidget)
        self.sourceLabel.setText('Upload photo of sheet music:')
        self.sourceLabel.setStyleSheet("font-Size: 18px; color: white")
        self.sourceLabel.setFixedSize(QSize(sourceFrameWidth, sourceFrameHeight * 2))
        self.sourceLabel.move((self.wWidth - sourceFrameWidth) / 2, sourceFrameMove - sourceFrameHeight * 2 + idealRations)

        self.error1 = QLabel(self.layoutWidget)
        self.error1.setText(" Invalid Path")
        self.error1.setStyleSheet("color:rgb(237, 67, 55)")
        self.error1.setFixedSize(QSize(sourceFrameWidth, sourceFrameHeight))
        self.error1.move((self.wWidth - sourceFrameWidth) / 2, sourceFrameMove + sourceFrameHeight + idealRations)
        self.error1.setVisible(False)

        self.darken = QGraphicsOpacityEffect(opacity=0.3)
        self.frameBox.setGraphicsEffect(self.darken)
        self.secondFrame.setGraphicsEffect(self.darken)

        sourceDirSize = sourceFrameHeight * 1.4
        sourceDirMove = self.wHeight / 2.425
        self.sourceDirButton = QPushButton(self.layoutWidget)
        self.sourceDirButton.clicked.connect(self.sourceClicked)
        self.sourceDirButton.setFixedSize(QSize(sourceDirSize, sourceDirSize))
        self.sourceDirButton.move((self.wWidth + sourceFrameWidth) / 2 + self.wWidth / 204, sourceDirMove + idealRations)
        self.sourceDirButton.setStyleSheet(f"border-image: url({folderIcon});")



        startButtonWidth = self.wWidth / 3.2
        startButtonHeight = self.wHeight / 12
        self.startButton = QPushButton(self.layoutWidget)
        self.startButton.clicked.connect(self.startProcess)
        self.startButton.setFixedSize(QSize(startButtonWidth, startButtonHeight))
        self.startButton.move((self.wWidth - startButtonWidth) / 2, self.wHeight / 1.5)
        self.startButton.setStyleSheet(f"font-size: 18px; color: #171717; border-radius: {startButtonWidth / 80}px; background:white")
        self.startButton.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                color: #1a1a1a;
                border-radius: 4px;
                background:white;
            }
            QPushButton:hover {
                background-color: #cacaca;
            }
            QPushButton:hover:!pressed {
                background:#e2e2e2;
            }
        """)
        self.startButton.setText("Start!")

        self.textbox = QLineEdit(self.layoutWidget)
        self.textbox.setValidator(QIntValidator(1, 999, self))
        self.textbox.setText("0")
        self.textbox.setVisible(False)

        cmdScrollHeight = self.eHeight * 0.7
        self.cmdScroll = QTextBrowser(self.layoutWidget)
        self.cmdScroll.setFixedSize(QSize(secondFrameDirWidth / 2.5, cmdScrollHeight))
        self.cmdScroll.move((self.eWidth - secondFrameDirWidth) / 2 + (secondFrameDirWidth - secondFrameDirWidth/2.5) , (self.eHeight - secondFrameDirHeight) / 2 )
        self.cmdScroll.setStyleSheet("background:rgb(150,150,150)")
        self.cmdScroll.setTextColor(QColor(25,25,25))
        self.cmdScroll.setFontPointSize(13)
        self.cmdScroll.setFrameStyle(QFrame.NoFrame)
        self.cmdScroll.setVisible(False)

        self.vbox = QVBoxLayout()
        self.vbox.setContentsMargins(QMargins())

        self.widgetV = QWidget()
        self.widgetV.setLayout(self.vbox)

        scrollAreaHeight = self.eHeight * 0.98
        self.scrollArea = QScrollArea(self.layoutWidget)
        self.scrollArea.setFixedSize(QSize(secondFrameDirWidth / 1.771, scrollAreaHeight))
        self.scrollArea.move((self.eWidth - secondFrameDirWidth) / 2, (self.eHeight - secondFrameDirHeight) / 2)
        self.scrollArea.setStyleSheet("background:rgb(150,150,150)")
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setVisible(False)

        self.progressValue = 0
        self.progressBar = QProgressBar(self.layoutWidget)
        self.progressBar.setMinimum(0)
        self.progressBar.setFixedSize(QSize(secondFrameDirWidth, sourceFrameHeight/2))
        self.progressBar.move((self.eWidth-secondFrameDirWidth)/2, secondFrameDirHeight)
        self.progressBar.setStyleSheet("QProgressBar::chunk " "{" "background:rgb(255, 102, 170);" "}")
        self.progressBar.setTextVisible(False)
        self.progressBar.setVisible(False)

        menuButtonWidth = self.eWidth / 4
        menuButtonHeight = self.eHeight / 8

        self.textbox.setFixedSize(menuButtonWidth * 0.7, menuButtonHeight * 0.5)
        self.textbox.move(self.eWidth / 1.4, self.eHeight / 1.25)
        self.textbox.setAlignment(Qt.AlignCenter)
        self.textbox.setStyleSheet(f"font-size: 18px; color: #171717; background:white")

        self.menuLabel = QLabel(self.layoutWidget)
        self.menuLabel.setFixedSize(menuButtonWidth * 0.7, menuButtonHeight * 0.7)
        self.menuLabel.move(self.eWidth / 1.4, self.eHeight / 1.15)
        self.menuLabel.setStyleSheet(f"border-image: url({pauseBack1});")
        self.menuLabel.setVisible(False)

        menuStyle1 = """
            QPushButton {
                border-image: url(pause-back);
                border: none;
            }
            QPushButton:hover {
                border-image: url(pause-back1);
            }
        """
        menuStyle2 = menuStyle1.replace("pause-back", pauseBack)
        menuStyle = menuStyle2.replace("pause-back1", pauseBack1)

        self.menuButton = QPushButton(self.layoutWidget)
        self.menuButton.clicked.connect(self.makeBox)
        self.menuButton.setFixedSize(menuButtonWidth * 0.7, menuButtonHeight * 0.7)
        self.menuButton.move(self.eWidth / 1.4, self.eHeight / 1.15)
        self.menuButton.setStyleSheet(menuStyle)
        self.menuButton.setVisible(False)

        self.setCentralWidget(self.layoutWidget)

    ### Use this function To attach files to the exe file (eg - png, txt, jpg etc) using pyinstaller
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """

        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")

        returnPath = os.path.join(base_path, relative_path)

        returnPath = returnPath.replace("\\", "/")

        return returnPath

    def sourceClicked(self):
        url, filter= QFileDialog.getOpenFileName(self, 'Select Sheet Music', '~', 'PNG files (*.png)')
        self.sourceFolder = url
        file = QUrl.fromLocalFile(url).fileName()
        fileSplit, _ = file.split(".")
        self.filename = fileSplit
        print(self.sourceFolder,self.filename)

        if self.sourceFolder == "":
            self.sourceFolder = "Select path"
            self.sourceFrame.setStyleSheet("background-color: white; color: grey")

        else:
            self.sourceFrame.setStyleSheet("background-color: white; color: black")

        self.sourceFrame.setText(f" {self.sourceFolder}")

    
    def appendText(self, message, delete):
        if delete == True:
            self.cmdScroll.clear()
        else:
            self.cmdScroll.append(message)

    def showOldGui(self):
        self.wWidth = 728
        self.wHeight = 728
        self.cmdScroll.clear()
        self.cmdScroll.setVisible(False)
        self.progressBar.setVisible(False)
        self.menuButton.setVisible(False)
        self.menuLabel.setVisible(False)
        self.sourceLabel.setVisible(True)
        self.startButton.setVisible(True)
        self.sourceFrame.setVisible(True)
        self.sourceDirButton.setVisible(True)

    def finishedTransfer(self):
        self.progressBar.setVisible(False)

    def userError(self, num):
        self.showOldGui()
        self.error1.setVisible(False)

        if num == 0 or num == 2:
            self.error1.setVisible(True)

    def progressBarMax(self, max):
        self.progressBar.setMaximum(max)

    def progressBarAdd(self):
        print(self.progressValue)
        self.progressValue = self.progressValue+1
        self.progressBar.setValue(self.progressValue)

    def showLayout2(self):
        self.setFixedSize(QSize(self.eWidth, self.eHeight))
        self.makeBox()
        self.error1.setVisible(False)
        self.startButton.setVisible(False)
        self.sourceFrame.setVisible(False)
        self.sourceDirButton.setVisible(False)
        self.sourceLabel.setVisible(False)
        self.cmdScroll.setVisible(True)
        self.progressBar.setVisible(True)
        self.textbox.setVisible(True)
        self.scrollArea.setVisible(True)
        self.menuButton.setVisible(True)
        self.menuLabel.setVisible(True)

    def makeBox(self):
        y = self.textbox.text()
        y.replace(" ","")

        self.appendText("", True)

        x = int(y)
        print(x)

        if self.vbox.count() != 0:
            while self.vbox.count() != 0:
                self.vbox.removeWidget(self.vbox.itemAt(0).widget())

        if x != 0:
            pngPath = f"PngOutput\\measure{x}"

            for file in os.listdir(pngPath):
                pdfView = QLabel(self.layoutWidget)
                pdfView.setPixmap(pngPath + "\\" + file)
                self.vbox.addWidget(pdfView)

            testArray = accessJ(self.filename,x)
            for s in testArray:
                self.appendText(s,False)
            self.appendText("[-----------------------]", False)

        else:
            for file in os.listdir("measure0"):
                pdfView = QLabel(self.layoutWidget)
                pdfView.setPixmap(f"measure0{file}")
                self.vbox.addWidget(pdfView)

        self.scrollArea.setWidget(self.widgetV)

    def startProcess(self):
        self.worker = Worker(self.sourceFolder,self.filename)
        self.worker.signal.max.connect(self.progressBarMax)
        self.worker.signal.addIt.connect(self.progressBarAdd)
        self.worker.signal.error.connect(self.userError)
        self.worker.signal.finished.connect(self.finishedTransfer)
        self.worker.signal.showLayout2.connect(self.showLayout2)
        QThreadPool.globalInstance().start(self.worker)

app = QApplication(sys.argv)


window = MainWindow()
window.show()

if __name__ == "__main__":
    app.exec_()