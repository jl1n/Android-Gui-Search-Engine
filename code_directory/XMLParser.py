import xml.dom.minidom
from xml.dom.minidom import Node
from collections import OrderedDict

class XMLParser:

    def __init__(self):
        val = 0

    def incrementVal(self):
        #val += 1
        return

    def getElement(self):
        #return element
        return

    def setFile(self, file):
        self.file = file

    def getFile(self):
        #return file
        return

if __name__ == "__main__":
    dom = xml.dom.minidom.parse("test_file.xml")

    #file = XMLParser()
    #file.setFile(dom)

    hmap=OrderedDict([("id", 0), ("app_id", 0), ("layout", 0), ("ImageView", 0),
          ("TextView", 0), ("ListView", 0), ("Button", 0), ("Spinner", 0),
          ("Checkbox", 0), ("Picker", 0), ("Radio", 0), ("Toggle", 0)])

    for elem in dom.getElementsByTagName("*"):
        if(elem.tagName in hmap):
            hmap[elem.tagName] = hmap[elem.tagName]+ 1
        if(elem.tagName == "RelativeLayout" or elem.tagName == "LinearLayout" or elem.tagName == "FrameLayout"):
            hmap["layout"] = hmap["layout"]+ 1


    for i in hmap:
        print(hmap[i], end='')
