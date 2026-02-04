import maya.cmds as cmds
import traceback
import importlib

class attrSetter():

    def __init__(self):        
        pass
    
    #語尾の取得
    def getEndName(self, selection, endName):

        objList = []

        for obj in selection:
            if obj.endswith(endName):
                objList.append(obj)

        return objList                

    #アトリビュートをロックする
    def attrLock(self, setObjList, lockAttrList, isInvisibility):

        #指定されたオブジェクト1つ1つに対して、ロックするアトリビュートをそれぞれにロックや不可視化の操作
        for obj in setObjList:

            for i in lockAttrList:
                
                if i:
                    attrName = i.property("attr")
                    try:
                        cmds.setAttr(obj + "." + attrName, lock=True)

                        if isInvisibility:
                            cmds.setAttr(obj + "." + attrName, keyable=False, channelBox=False)

                    except Exception as e:
                        print("アトリビュート見つからない" + {e})

    #色の適用
    def applyColor(self, setObjList, colorRGBIndex):

        for obj in setObjList:
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
            
            if shapes:

                #描画オーバーライドの項目をオンにする
                for s in shapes:
                    cmds.setAttr(f"{s}.overrideEnabled", 1)

                    #rgb値のリストの値を元に色を適用していく
                    if isinstance(colorRGBIndex, (list, tuple)):
                        cmds.setAttr(f"{s}.overrideRGBColors", 1)

                        r = colorRGBIndex[0] / 255.0
                        g = colorRGBIndex[1] / 255.0
                        b = colorRGBIndex[2] / 255.0
                        cmds.setAttr(f"{s}.overrideColorRGB", r, g, b)

                    else:
                        cmds.setAttr(f"{s}.overrideRGBColors", 0)
                        cmds.setAttr(f"{s}.overrideColor", colorRGBIndex)

            else:
                pass

    #実行
    def doByGui(self, endName, doLockList, invisible, changeColor, color):

        cmds.undoInfo(openChunk=True)

        #選択中のオブジェクトを取得
        selection = cmds.ls(selection= True, long=True)
        if not selection:
            cmds.warning("何も選択されていません。")
            return
        
        #語尾が一致するオブジェクトを取得してリスト化
        targetObjList = self.getEndName(selection, endName)
        if not targetObjList:
            cmds.warning("指定した語尾のオブジェクトがありません")
            return
        
        #アトリビュートのロックと必要なら色の変更
        try:
            self.attrLock(targetObjList, doLockList, invisible)

            if changeColor:

                self.applyColor(targetObjList, color)

        except Exception as e:
            cmds.undo()
            print(e)

        finally:
            cmds.undoInfo(closeChunk=True)
