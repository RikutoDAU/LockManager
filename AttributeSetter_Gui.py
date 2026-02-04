import maya.cmds as cmds

from PySide6 import QtWidgets as qw ,QtCore as qc

import AttributeSetter as aS
import importlib
importlib.reload(aS)


class attrSetGui(qw.QDialog):

    windowName = "AttributeSetter"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.logicClass = aS.attrSetter()
        


        #ウィンドウの設定
        self.setWindowFlags(self.windowFlags() | qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.windowName)
        self.resize(400,400)
        #self.uiWindow()

        
        self.layout = qw.QVBoxLayout(self)
        self.layout.setSpacing(10)

        #表示する説明文
        explainText = (
            "選択されているオブジェクトのうち、ユーザーが入力した語尾が一致するものに対して操作されます"
            )
        self.explain = qw.QLabel(explainText)
        self.layout.addWidget(self.explain)

        self.endNameInput = qw.QLineEdit()
        self.endNameInput.setPlaceholderText("操作したい語尾を入力してください。:例(_FK)")
        self.layout.addWidget(self.endNameInput)

        '''
        self.lockTrsXCb = qw.QCheckBox("X位置のロック")
        self.lockTrsYCb = qw.QCheckBox("Y位置のロック")
        self.lockTrsZCb = qw.QCheckBox("Z位置のロック")

        self.lockRotXCb = qw.QCheckBox("X回転のロック")
        self.lockRotYCb = qw.QCheckBox("Y回転のロック")
        self.lockRotZCb = qw.QCheckBox("Z回転のロック")

        self.lockTrsXCb.setChecked(True)
        self.lockTrsYCb.setChecked(True)
        self.lockTrsZCb.setChecked(True)

        self.lockRotXCb.setChecked(True)
        self.lockRotYCb.setChecked(True)
        self.lockRotZCb.setChecked(True)
'''
        '''
        self.lockTrsXCb.setProperty("attr", "tx")
        self.lockTrsYCb.setProperty("attr", "ty")
        self.lockTrsZCb.setProperty("attr", "tz")
        self.lockRotXCb.setProperty("attr", "rx")
        self.lockRotYCb.setProperty("attr", "ry")
        self.lockRotZCb.setProperty("attr", "rz")
        '''

        self.lockCbList = []
        attrsList = [
            ("tx", "X位置"), ("ty", "Y位置"), ("tz", "Z位置"), 
            ("rx", "X回転"), ("ry", "Y回転"), ("rz", "Z回転"),
            ("sx", "Xスケール"), ("sy", "Yスケール"), ("sz", "Zスケール"),
        ]

        for attr, attrName in attrsList:
            cb = qw.QCheckBox(attrName + "のロック")
            cb.setProperty("attr", attr)
            cb.setChecked(False)
            self.layout.addWidget(cb)
            self.lockCbList.append(cb)

        
        self.isInvisible = qw.QCheckBox("ロックした属性を不可視にする")
        self.isInvisible.setChecked(True)
        self.layout.addWidget(self.isInvisible)

        #self.setColor = 

        self.layout.addWidget(qw.QLabel("ワイヤーの色を選択 (0-255)"))

        self.rgbIndexList = []

        rgbList = ["Red", "Green", "Blue"]

        for rgb in rgbList:
            line = qw.QHBoxLayout()
            colorName = qw.QLabel(rgb)
            slider = qw.QSlider(qc.Qt.Horizontal)
            slider.setRange(0, 255) 
            slider.setValue(0)

            indexInput = qw.QLineEdit("0")




            slider.valueChanged.connect(lambda index, i=indexInput: i.setText(str(index)))
            slider.valueChanged.connect(self.updateColorPreview)

            indexInput.editingFinished.connect(lambda s=slider, i=indexInput: self.synchroSlider(s, i))

            line.addWidget(colorName)
            line.addWidget(slider)
            line.addWidget(indexInput)
            self.layout.addLayout(line)

            self.rgbIndexList.append(slider)

        self.colorPreview = qw.QWidget()
        self.colorPreview.setFixedHeight(30)
        self.layout.addWidget(self.colorPreview)
        self.updateColorPreview()



        
        '''
        colorLayout = qw.QHBoxLayout()
        
        self.colorSlider = qw.QSlider(qc.Qt.Horizontal)
        self.colorSlider.setRange(0, 31)
        self.colorSlider.setValue(13)
        
        self.colorLabel = qw.QLabel("13")
        
        colorLayout.addWidget(self.colorSlider)
        colorLayout.addWidget(self.colorLabel)
        self.layout.addLayout(colorLayout)


        self.colorSlider.valueChanged.connect(lambda v: self.colorLabel.setText(str(v)))
        '''
        self.doButton = qw.QPushButton("実行")
        self.doButton.clicked.connect(self.do)
        self.layout.addWidget(self.doButton)

    def synchroSlider(self, rgbSlider, rgbIndexText):

        text = rgbIndexText.text()

        #数値のみか確認
        if text.isdecimal():
            index = int(text)

            if index < 0:
                index = 0
            elif index > 255:
                index = 255

            rgbSlider.setValue(index)
            rgbIndexText.setText(str(index))

        else:
            rgbIndexText.setText(str(rgbSlider.value()))

        

    def updateColorPreview(self):
        r = self.rgbIndexList[0].value()
        g = self.rgbIndexList[1].value()
        b = self.rgbIndexList[2].value()

        self.colorPreview.setStyleSheet(f"background-color:rgb({r},{g},{b});")
        

    def do(self):

        endName = self.endNameInput.text()

        if not endName:
            cmds.error("語尾が入力されていない")

        doLockList = []

        for cb in self.lockCbList:
            if cb.isChecked():
                doLockList.append(cb)
        
        invisible = self.isInvisible.isChecked()

        r = self.rgbIndexList[0].value()
        g = self.rgbIndexList[1].value()
        b = self.rgbIndexList[2].value()
        rgbIndexList = [r, g, b]

        #color = self.colorSlider.value()


        self.logicClass.doByGui(endName, doLockList, invisible, rgbIndexList)

        self.close()

        #self.logicClass.attrLock(objList, self.lockList, self.isInvisible)

        #self.logicClass.applyColor(objList, )

'''
openWindow = attrSetGui()

openWindow.setObjectName(openWindow.windowName)
openWindow.show()
'''
openWindow = attrSetGui()

openWindow.setObjectName(openWindow.windowName)
openWindow.show()
