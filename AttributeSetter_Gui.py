import maya.cmds as cmds

from PySide6 import QtWidgets as qw ,QtCore as qc
#from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton

import AttributeSetter as aS
import importlib

#logicClass = aS.attrSetter

class attrSetGui(qw.QDialog):

    windowName = "AttributeSetter"

    def __init__(self, parent=None):
        super().__init__(parent)

        logicClass = aS.attrSetter()
        
        self.selectedList = cmds.ls(selection = True, long = True)

        #ウィンドウの設定
        self.setWindowFlags(self.windowFlags() | qc.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(self.windowName)
        self.resize(400,400)
        #self.uiWindow()

    #def uiWindow(self):
        
        self.layout = qw.QVBoxLayout(self)
        self.layout.setSpacing(10)

        #表示する説明文
        explainText = (
            "\n"
            )
        self.explain = qw.QLabel(explainText)

        self.endNameInput = qw.QLineEdit()
        self.endNameInput.setPlaceholderText("操作したい語尾を入力してください。:例(_FK)")
        self.layout.addWidget(self.endNameInput)


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

        self.lockTrsXCb.setProperty("attr", "tx")
        self.lockTrsYCb.setProperty("attr", "ty")
        self.lockTrsZCb.setProperty("attr", "tz")
        self.lockRotXCb.setProperty("attr", "rx")
        self.lockRotYCb.setProperty("attr", "ry")
        self.lockRotZCb.setProperty("attr", "rz")
        
        self.lockList = [
            self.lockTrsXCb,self.lockTrsYCb,self.lockTrsZCb,
            self.lockRotXCb,self.lockRotYCb,self.lockRotZCb,
        ]

        
        self.isInvisivil = qw.QCheckBox("ロックした属性を不可視にする")
        self.lockTrsZCb.setChecked(True)

        #self.setColor = 

        self.layout.addWidget(qw.QLabel("Curve Color (Index):"))
        
        color_layout = qw.QHBoxLayout()
        
        # 
        self.colorSlider = qw.QSlider(qc.Qt.Horizontal)
        self.colorSlider.setRange(0, 31)
        self.colorSlider.setValue(13)
        
        #
        self.colorLabel = qw.QLabel("13")
        
        color_layout.addWidget(self.colorSlider)
        color_layout.addWidget(self.colorLabel)
        self.layout.addLayout(color_layout)


        self.colorSlider.valueChanged.connect(lambda v: self.colorLabel.setText(str(v)))

        self.doButton = qw.QPushButton("実行")
        self.doButton.clicked.connect(self.do)

        #ウィンドウに表示
        for i in self.lockList:
            self.layout.addWidget(i)

        
        self.layout.addWidget(self.doButton)




        

    def do(self):
        
        objList = self.logicClass.getEndName(self.endNameinput)

        self.logicClass.attrLock(objList, self.lockList, self.isInvisivil)

        self.logicClass.applyColor(objList, )

'''
openWindow = attrSetGui()

openWindow.setObjectName(openWindow.windowName)
openWindow.show()
'''
openWindow = attrSetGui()

openWindow.setObjectName(openWindow.windowName)
openWindow.show()
