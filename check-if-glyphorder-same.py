from vanilla.dialogs import *

glyphOrderDict = {}

# help(CurrentFont().removeGlyph())

inputFonts = getFile("select masters for var font", allowsMultipleSelection=True, fileTypes=["ufo"])

for fontPath in inputFonts:
    f = OpenFont(fontPath, showInterface=False)
    
    glyphs = []
    # # open the fonts, then:
    for glyphName in f.glyphOrder:
        # print(glyphName)
        glyphs.append(glyphName)
    
    # print(glyphs)
    glyphOrderDict[f.info.styleName] = glyphs
        
    # print(glyphOrderDict)
    f.save()
    f.close()
    
# print(glyphOrderDict)
    
glyphOrderList = []

for val in glyphOrderDict.values():
    glyphOrderList.append(tuple(val))
    # print(val)

glyphOrderSet = set(glyphOrderList)

# 

if len(glyphOrderSet) >= 2:
    print("different glyph sets")
else:
    print("same glyph sets \n")
    print(glyphOrderSet)
    