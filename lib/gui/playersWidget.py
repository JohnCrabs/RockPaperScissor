import sys
import os
import tkinter as tk
from PySide2.QtCore import (
    Qt
)
from PySide2.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QSpacerItem
)
from PySide2.QtGui import (
    QIcon,
    QFont
)

import lib.gui.showImageWidget as showImageWidget

_PROJECT_FOLDER = os.path.normpath(os.path.realpath(__file__) + '/../../../')

_INT_SCREEN_WIDTH = tk.Tk().winfo_screenwidth()  # get the screen width
_INT_SCREEN_HEIGHT = tk.Tk().winfo_screenheight()  # get the screen height
_INT_WIN_WIDTH = 1024  # this variable is only for the if __name__ == "__main__"
_INT_WIN_HEIGHT = 512  # this variable is only for the if __name__ == "__main__"

_INT_MAX_STRETCH = 100000  # Spacer Max Stretch
_INT_BUTTON_MIN_WIDTH = 50  # Minimum Button Width


class WidgetPlayerWindow(QWidget):
    def __init__(self, w=512, h=512, minW=256, minH=256, maxW=512, maxH=512,
                 winTitle='My Window', iconPath=''):
        super().__init__()
        # ---------------------- #
        # ----- Set Window ----- #
        # ---------------------- #
        self.setWindowTitle(winTitle)  # Set Window Title
        self.setWindowIcon(QIcon(iconPath))  # Set Window Icon
        self.setGeometry(_INT_SCREEN_WIDTH / 4, _INT_SCREEN_HEIGHT / 4, w, h)  # Set Window Geometry
        self.setMinimumWidth(minW)  # Set Window Minimum Width
        self.setMinimumHeight(minH)  # Set Window Minimum Height
        if maxW is not None:
            self.setMaximumWidth(maxW)  # Set Window Maximum Width
        if maxH is not None:
            self.setMaximumHeight(maxH)  # Set Window Maximum Width

        self.vbox_main_layout = QVBoxLayout(self)  # Create the main vbox

        # --------------------------- #
        # ----- ImageViewerArea ----- #
        # --------------------------- #
        self.imageViewer = showImageWidget.WidgetImageViewer(w=256, h=256,
                                                             minW=16, minH=16,
                                                             maxW=2048, maxH=2048)

        # ------------------------------------ #
        # ----- Set QLabel and Variables ----- #
        # ------------------------------------ #
        self.playerName = 'A Player'
        self.scoreValue = 0

        self.label_Score = QLabel(self.playerName + '\'s Score: ' + str(self.scoreValue).zfill(4))
        self.label_Score.setAlignment(Qt.AlignCenter)
        self.label_Score.setMaximumHeight(32)

        self.label_Score.setStyleSheet(
            '''
            QLabel {
                font-size: 12pt;
                font-weight: bold;
                color: rgb(255, 0, 0);
                background-color: rgb(0, 0, 0);
            }
            '''
        )

    def setWidget(self):
        # Set buttons in hbox
        hbox_scoreLine = QHBoxLayout()
        hbox_scoreLine.addWidget(self.label_Score)

        vbox_finalLayout = QVBoxLayout()
        vbox_finalLayout.addLayout(hbox_scoreLine)
        vbox_finalLayout.addWidget(self.imageViewer)

        self.vbox_main_layout.addLayout(vbox_finalLayout)

    def setPlayerName(self, name: str):
        self.playerName = name
        self.updateScore()

    def updateScore(self):
        self.label_Score.setText(self.playerName + '\'s Score: ' + str(self.scoreValue).zfill(4))

    def getInputFromCamera(self, state):
        self.imageViewer.setIsInputFromCamera(state)

    def stopInputFromCameraAndKeepImage(self):
        self.imageViewer.stopImageFromCameraAndKeepImage()

    def getCurrentShownImage(self):
        return self.imageViewer.getImgToView()

    def setImageForView(self, path):
        self.imageViewer.setImg(path)

    def addToScore(self, addScore):
        self.scoreValue += addScore
        self.updateScore()

    def clearImg(self):
        self.imageViewer.clearImg()

    def resetTheScore(self):
        self.scoreValue = 0
        self.updateScore()

# ******************************************************* #
# ********************   EXECUTION   ******************** #
# ******************************************************* #

def exec_app(w=512, h=512, minW=256, minH=256, maxW=512, maxH=512, winTitle='My Window', iconPath=''):
    myApp = QApplication(sys.argv)  # Set Up Application
    widgetWin = WidgetPlayerWindow(w=w, h=h, minW=minW, minH=minH, maxW=maxW, maxH=maxH,
                                   winTitle=winTitle, iconPath=iconPath)  # Create MainWindow

    widgetWin.setWidget()
    widgetWin.show()  # Show Window
    myApp.exec_()  # Execute Application
    sys.exit(0)  # Exit Application


if __name__ == "__main__":
    exec_app(w=1024, h=512, minW=512, minH=256, maxW=512, maxH=512,
             winTitle='WidgetTemplate', iconPath=_PROJECT_FOLDER + '/icon/crabsMLearning_32x32.png')
