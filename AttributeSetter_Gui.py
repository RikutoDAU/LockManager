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
        
        self.layout = qw.QVBoxLayout(self)
        self.layout.setSpacing(10)

        #表示する説明文
        explainText = (
            "選択されているオブジェクトのうち、ユーザーが入力した語尾が一致するものに対して操作されます"
            )
        self.explain = qw.QLabel(explainText)
        self.layout.addWidget(self.explain)

        #指定する語尾の入力
        self.endNameInput = qw.QLineEdit()
        self.endNameInput.setPlaceholderText("操作したい語尾を入力してください。:例(_FK)")
        self.layout.addWidget(self.endNameInput)

        #ロック設定できるアトリビュートのリスト
        self.lockCbList = []
        attrsList = [
            ("tx", "X位置"), ("ty", "Y位置"), ("tz", "Z位置"), 
            ("rx", "X回転"), ("ry", "Y回転"), ("rz", "Z回転"),
            ("sx", "Xスケール"), ("sy", "Yスケール"), ("sz", "Zスケール"),
        ]
        #それぞれのアトリビュートに行う設定の表示
        for attr, attrName in attrsList:
            cb = qw.QCheckBox(attrName + "のロック")
            cb.setProperty("attr", attr)
            cb.setChecked(False)
            self.layout.addWidget(cb)
            self.lockCbList.append(cb)

        #不可視にするかのチェックボックスを表示
        self.isInvisible = qw.QCheckBox("ロックした属性を不可視にする")
        self.isInvisible.setChecked(True)
        self.layout.addWidget(self.isInvisible)

        #色を変化させるかのチェックボックスを表示
        self.changeColor = qw.QCheckBox("ワイヤーの色を変更する")
        self.changeColor.setChecked(True)
        self.layout.addWidget(self.changeColor)
        
        self.layout.addWidget(qw.QLabel("ワイヤーの色を選択 (0-255)"))

        #rgbの値の保存用リスト
        self.rgbIndexList = []
        rgbList = ["Red", "Green", "Blue"]

        #r,g,b,それぞれのスライダーと数値入力の追加
        for rgb in rgbList:
            line = qw.QHBoxLayout()
            colorName = qw.QLabel(rgb)

            #スライダー設定
            slider = qw.QSlider(qc.Qt.Horizontal)
            slider.setRange(0, 255) 
            slider.setValue(0)

            #テキスト部分
            indexInput = qw.QLineEdit("0")

            #スライダー操作時に更新
            slider.valueChanged.connect(lambda index, i=indexInput: i.setText(str(index)))
            slider.valueChanged.connect(self.updateColorPreview)

            #テキスト入力後に更新
            indexInput.editingFinished.connect(lambda s=slider, i=indexInput: self.synchroSlider(s, i))

            #ウィンドウに表示
            line.addWidget(colorName)
            line.addWidget(slider)
            line.addWidget(indexInput)
            self.layout.addLayout(line)

            #rgbを保存
            self.rgbIndexList.append(slider)

        #入力されているRGBによる色を表示
        self.colorPreview = qw.QWidget()
        self.colorPreview.setFixedHeight(30)
        self.layout.addWidget(self.colorPreview)
        self.updateColorPreview()

        #実行ボタンの表示
        self.doButton = qw.QPushButton("実行")
        self.doButton.clicked.connect(self.do)
        self.layout.addWidget(self.doButton)

    #色設定のテキストとスライダーの数値を同期させる
    def synchroSlider(self, rgbSlider, rgbIndexText):

        text = rgbIndexText.text()

        #数値のみか確認と数値の修正
        if text.isdecimal():
            index = int(text)

            if index < 0:
                index = 0
            elif index > 255:
                index = 255

            #スライダーとテキストに同じ値を入れる
            rgbSlider.setValue(index)
            rgbIndexText.setText(str(index))

        else:
            rgbIndexText.setText(str(rgbSlider.value()))

        
    #プレビュー用の色の更新
    def updateColorPreview(self):

        #現在の指定されたrgb値を取得
        r = self.rgbIndexList[0].value()
        g = self.rgbIndexList[1].value()
        b = self.rgbIndexList[2].value()

        #背景色としてrgb値を元に表示
        self.colorPreview.setStyleSheet(f"background-color:rgb({r},{g},{b});")
        

    def do(self):
        
        #指定された語尾取得
        endName = self.endNameInput.text()

        if not endName:
            cmds.error("語尾が入力されていない")

        #ロックする属性をリスト化
        doLockList = []

        for cb in self.lockCbList:
            if cb.isChecked():
                doLockList.append(cb)
        
        invisible = self.isInvisible.isChecked()

        changeColor = self.changeColor.isChecked()

        #現在の指定されたrgb値を取得
        r = self.rgbIndexList[0].value()
        g = self.rgbIndexList[1].value()
        b = self.rgbIndexList[2].value()
        rgbIndexList = [r, g, b]
    


        #実行
        self.logicClass.doByGui(endName, doLockList, invisible, changeColor, rgbIndexList)

        self.close()

openWindow = attrSetGui()

openWindow.setObjectName(openWindow.windowName)
openWindow.show()
