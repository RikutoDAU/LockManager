import maya.cmds as cmds
import traceback
import AttributeSetterGui as asg

class attrSetter():

    def __init__(self):

        guiClass = asg.attrSetGui
        self.selectedList = guiClass.selectedList

        self.lockAttrList = []
        self.lockAttrList = guiClass.lockList

        self.endName = guiClass.endNameInput

    def getEndName(self, endName):

        objList = []

        for obj in self.selectedList:
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

    def applyColor(self, setObjList, colorIndex):

        for obj in setObjList:
            shapes = cmds.listRelatives(obj, shapes=True, fullPath=True)
            
            if shapes:

                for s in shapes:
                    cmds.setAttr(f"{s}.overrideEnabled", 1)
                    cmds.setAttr(f"{s}.overrideColor", colorIndex)

            else:
                pass


    def do(self):

        
