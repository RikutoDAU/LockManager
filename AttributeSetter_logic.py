import maya.cmds as cmds
import traceback
import importlib

class attrSetter():

    def __init__(self):        
        pass

    def getEndName(self, selection, endName):

        objList = []

        for obj in selection:
            if obj.endswith(endName):
                objList.append(obj)

        return objList                

    def attrLock(self, setObjList, lockAttrList, isInvisibility):

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

    def applyColor(self, setObjList, colorRGBIndex):

        for obj in setObjList:
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
            
            if shapes:

                for s in shapes:
                    cmds.setAttr(f"{s}.overrideEnabled", 1)

                    if isinstance(colorRGBIndex, (list, tuple)):
                        cmds.setAttr(f"{s}.overrideRGBColors", 1)

                        r = colorRGBIndex[0] / 255.0
                        g = colorRGBIndex[1] / 255.0
                        b = colorRGBIndex[2] / 255.0
                        cmds.setAttr(f"{s}.overrideColorRGB", r, g, b)

                    else:
                        cmds.setAttr(f"{s}.overrideEnabled", 0)
                        cmds.setAttr(f"{s}.overrideColor", colorRGBIndex)

            else:
                pass


    def doByGui(self, endName, doLockList, invisible, color):

        cmds.undoInfo(openChunk=True)

        selection = cmds.ls(selection= True, long=True)
        if not selection:
            cmds.warning("何も選択されていません。")
            return
        
        targetObjList = self.getEndName(selection, endName)
        if not targetObjList:
            cmds.warning("指定した語尾のオブジェクトがありません")
            return
        
        try:
            self.attrLock(targetObjList, doLockList, invisible)

            self.applyColor(targetObjList, color)

        except Exception as e:
            print(e)

        finally:
            cmds.undoInfo(closeChunk=True)
