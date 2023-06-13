import sys
import os
import tkinter as tk
import numpy as np
from tensorflow import keras

from PySide2.QtCore import (
    Qt
)

from PySide2.QtWidgets import (
    QWidget,
    QApplication,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QCheckBox,
    QComboBox,
    QLabel
)

from PySide2.QtGui import (
    QIcon
)

from lib.gui.playersWidget import WidgetPlayerWindow
import lib.gui.commonFunctions as comFunc
import lib.core.file_manipulation as file_manip

import lib.core.RockPaperScissor as rps

_PROJECT_FOLDER = os.path.normpath(os.path.realpath(__file__) + '/../../../')

_INT_SCREEN_WIDTH = tk.Tk().winfo_screenwidth()  # get the screen width
_INT_SCREEN_HEIGHT = tk.Tk().winfo_screenheight()  # get the screen height
_INT_WIN_WIDTH = 1024  # this variable is only for the if __name__ == "__main__"
_INT_WIN_HEIGHT = 512  # this variable is only for the if __name__ == "__main__"

_INT_MAX_STRETCH = 100000  # Spacer Max Stretch
_INT_BUTTON_MIN_WIDTH = 50  # Minimum Button Width

_STR_CLASSIFIER_MODEL_PATH = '../../lib/models/rock_paper_scissor.h5'
_MODEL_SIZE_W = 150
_MODEL_SIZE_H = 150

# _STR_CLASSIFIER_MODEL_PATH = '../../lib/models/CNN2D_rps.h5'
# _MODEL_SIZE_W = 64
# _MODEL_SIZE_H = 64


_STR_COMPUTER_ROCK_IMAGE_PATH = '../../lib/imgs/computer_rock.jpg'
_STR_COMPUTER_PAPER_IMAGE_PATH = '../../lib/imgs/computer_paper.jpg'
_STR_COMPUTER_SCISSOR_IMAGE_PATH = '../../lib/imgs/computer_scissor.jpg'

_DICT_COMPUTER_CHOICES_PATHS = {
    rps.getRock(): _STR_COMPUTER_ROCK_IMAGE_PATH,
    rps.getPaper(): _STR_COMPUTER_PAPER_IMAGE_PATH,
    rps.getScissors(): _STR_COMPUTER_SCISSOR_IMAGE_PATH
}

_NEW_GAME_MESSAGE = 'A New Game has been started. Good Luck!'


class WidgetCentral(QWidget):
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

        # ---------------------- #
        # ----- Set Button ----- #
        # ---------------------- #
        _buttonStyle = '''
            QPushButton {
                
            }
        '''

        self.button_Ready = QPushButton('Ready')
        self.button_UploadImage = QPushButton('Upload Image')
        self.button_CameraCapture = QPushButton('Capture')
        self.button_CameraCapture.setShortcut('C')
        self.button_CameraCapture.setEnabled(False)
        self.button_ResetCapture = QPushButton('Reset Capture')
        self.button_ResetCapture.setShortcut('R')
        self.button_ResetCapture.setEnabled(False)

        # ------------------------ #
        # ----- Set Checkbox ----- #
        # ------------------------ #
        self.checkbox_UseCamera = QCheckBox('Use Camera: ')
        self.checkbox_UseCamera.setStyleSheet(
            '''
                QCheckBox {
                    font-weight: bold;
                }
            '''
        )
        self.checkbox_UseCamera.setMaximumWidth(100)

        # ------------------------ #
        # ----- Set Combobox ----- #
        # ------------------------ #
        self.combobox_PlayersChoices = QComboBox()

        # ----------------------------- #
        # ----- Set Other Widgets ----- #
        # ----------------------------- #
        self.computerScreen = WidgetPlayerWindow(w=512, h=512, minW=16, minH=16, maxW=2048, maxH=2048)
        self.playerScreen = WidgetPlayerWindow(w=512, h=512, minW=16, minH=16, maxW=2048, maxH=2048)

        # -------------------------- #
        # ----- Set Classifier ----- #
        # -------------------------- #
        self.imageClassifier = keras.models.load_model(_STR_CLASSIFIER_MODEL_PATH)

        self.predictionIndex = 1
        self.predictionDict = {
            rps.getPaper(): 0,
            rps.getRock(): 1,
            rps.getScissors(): 2
        }

        self.isImageCaptured = False

        # --------------------------------- #
        # ----- Set RockPaperScissors ----- #
        # --------------------------------- #
        self.RockPaperScissor = rps.RockPaperScissor()
        self.RockPaperScissor.setPlayers(how_many=2)

        self.roundCounter = 0

        # ------------------------- #
        # ----- Set QLineEdit ----- #
        # ------------------------- #
        self.label_WinnerAnnounce = QLabel(_NEW_GAME_MESSAGE)
        self.label_WinnerAnnounce.setStyleSheet(
            '''
            QLabel {
                font-size: 12pt;
                font-weight: bold;
                color: rgb(255, 0, 0);
                background-color: rgb(0, 0, 0);
            }
            '''
        )
        self.label_WinnerAnnounce.setMaximumHeight(32)
        self.label_WinnerAnnounce.setAlignment(Qt.AlignCenter)

    def setWidget(self):
        self.computerScreen.setWidget()
        self.computerScreen.setPlayerName('Computer')
        self.playerScreen.setWidget()
        self.playerScreen.setPlayerName('Player')

        # label_UseCamera = QLabel('Use Camera: ')

        self.combobox_PlayersChoices.addItem(rps.getRock())
        self.combobox_PlayersChoices.addItem(rps.getPaper())
        self.combobox_PlayersChoices.addItem(rps.getScissors())

        hbox_PlayersLayout = QHBoxLayout()
        hbox_PlayersLayout.addWidget(self.computerScreen)
        hbox_PlayersLayout.addWidget(self.playerScreen)

        vbox_PlayersLayout = QVBoxLayout()
        vbox_PlayersLayout.addWidget(self.label_WinnerAnnounce)
        vbox_PlayersLayout.addLayout(hbox_PlayersLayout)

        hbox_PlayerButtons = QHBoxLayout()
        # Add combobox with PlayerChoices
        hbox_PlayerButtons.addWidget(self.combobox_PlayersChoices)
        # Add checkbox with UseCamera
        hbox_PlayerButtons.addWidget(self.checkbox_UseCamera)
        # Add button for CameraCapture
        hbox_PlayerButtons.addWidget(self.button_CameraCapture)
        # Add button for ResetCapture
        hbox_PlayerButtons.addWidget(self.button_ResetCapture)
        # Add button for UploadImage
        hbox_PlayerButtons.addWidget(self.button_UploadImage)
        # Add button for Ready
        hbox_PlayerButtons.addWidget(self.button_Ready)

        self.vbox_main_layout.addLayout(vbox_PlayersLayout)
        self.vbox_main_layout.addLayout(hbox_PlayerButtons)

        self.setEvents_()

    def setEvents_(self):
        # Checkbox
        self.checkbox_UseCamera.stateChanged.connect(self.action_UseCameraStateChanged)
        # Buttons
        self.button_CameraCapture.clicked.connect(self.action_CameraCaptureClicked)
        self.button_ResetCapture.clicked.connect(self.action_ResetCaptureClicked)
        self.button_UploadImage.clicked.connect(self.action_UploadImageClicked)
        self.button_Ready.clicked.connect(self.action_ReadyClicked)

    # *********************** #
    # *****   ACTIONS   ***** #
    # *********************** #

    def action_UseCameraStateChanged(self):
        state = self.checkbox_UseCamera.isChecked()
        self.button_CameraCapture.setEnabled(state)
        self.button_ResetCapture.setEnabled(state)
        self.playerScreen.getInputFromCamera(state)

        if not state:
            self.playerScreen.clearImg()
            self.isImageCaptured = False

    def action_CameraCaptureClicked(self):
        if not self.isImageCaptured:
            img = self.playerScreen.getCurrentShownImage()
            self.playerScreen.stopInputFromCameraAndKeepImage()

            tmp_path = '../../tmpExport/tmpImage.png'
            keras.preprocessing.image.save_img(tmp_path, img)
            # Make Prediction
            self.predictionIndex = self.makePredictionFromImagePath(tmp_path)
            self.combobox_PlayersChoices.setCurrentText(self.predictionIndex)
            self.isImageCaptured = True

    def action_ResetCaptureClicked(self):
        self.action_UseCameraStateChanged()
        self.isImageCaptured = False

    def action_UploadImageClicked(self):
        success, dialog = comFunc.openFileDialog(
            self,
            dialogName='Choose an Image',
            dialogOpenAt=file_manip.PATH_HOME,
            dialogFilters=['Image Files (*.png *.jpg *.jpeg *.bmp)'],
            dialogMultipleSelection=False
        )

        if success:
            filePath = dialog.selectedFiles()[0]
            # Make Prediction
            self.predictionIndex = self.makePredictionFromImagePath(filePath)
            self.combobox_PlayersChoices.setCurrentText(self.predictionIndex)

    def action_ReadyClicked(self):
        # Set Choice for Computer
        self.RockPaperScissor.setRandomChoiceForPLayerIndex(0)
        computerChoice = self.RockPaperScissor.getChoiceOfPlayerIndex(0)
        # print(computerChoice)
        imgPath = _DICT_COMPUTER_CHOICES_PATHS[computerChoice]
        self.computerScreen.setImageForView(imgPath)

        # Set Choice for Player
        playerChoice = self.combobox_PlayersChoices.currentText()
        self.RockPaperScissor.setChoiceForPlayerIndex(1, playerChoice)

        results = self.RockPaperScissor.getResults()
        winningIndex = results[0][2]
        winningScore = results[0][3]

        self.roundCounter += 1
        if winningScore > 0:
            if winningIndex == 0:
                self.computerScreen.addToScore(1)
                self.label_WinnerAnnounce.setText('Round ' + str(self.roundCounter) + ': The winner of this round is the COMPUTER!')
            elif winningIndex == 1:
                self.playerScreen.addToScore(1)
                self.label_WinnerAnnounce.setText('Round ' + str(self.roundCounter) + ': The winner of this round is our HUMBLE PLAYER!')
        else:
            self.label_WinnerAnnounce.setText('Round ' + str(self.roundCounter) + ': There\'s no winner for this round. You DRAW!')

    def makePredictionFromImagePath(self, path):
        img = keras.preprocessing.image.load_img(path, target_size=(_MODEL_SIZE_W, _MODEL_SIZE_H))
        x = keras.preprocessing.image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        img = np.vstack([x])
        prediction = self.imageClassifier.predict(img, batch_size=10)[0]
        prediction = [int(pred) for pred in prediction]
        # print(prediction)
        if 1 in prediction:
            prediction = prediction.index(1)

            # print(prediction)
            for _key_ in self.predictionDict.keys():
                # print(self.predictionDict[_key_])
                if prediction == self.predictionDict[_key_]:
                    # print(_key_)
                    return _key_
        else:
            for _key_ in self.predictionDict.keys():
                # print(self.predictionDict[_key_])
                if self.predictionIndex == self.predictionDict[_key_]:
                    # print(_key_)
                    return _key_

    def resetTheGame(self):
        self.computerScreen.resetTheScore()
        self.playerScreen.resetTheScore()
        self.label_WinnerAnnounce.setText(_NEW_GAME_MESSAGE)
        self.roundCounter = 0


# ******************************************************* #
# ********************   EXECUTION   ******************** #
# ******************************************************* #

def exec_app(w=512, h=512, minW=256, minH=256, maxW=512, maxH=512, winTitle='My Window', iconPath=''):
    myApp = QApplication(sys.argv)  # Set Up Application
    widgetWin = WidgetCentral(w=w, h=h, minW=minW, minH=minH, maxW=maxW, maxH=maxH,
                              winTitle=winTitle, iconPath=iconPath)  # Create MainWindow

    widgetWin.setWidget()
    widgetWin.show()  # Show Window
    myApp.exec_()  # Execute Application
    sys.exit(0)  # Exit Application


if __name__ == "__main__":
    exec_app(w=1024, h=512, minW=512, minH=256, maxW=512, maxH=512,
             winTitle='WidgetTemplate', iconPath=_PROJECT_FOLDER + '/icon/crabsMLearning_32x32.png')
