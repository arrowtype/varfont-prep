import os
from mojo.UI import AskString
from vanilla.dialogs import *

# copy-paste to fill this list with whatever glyphs fontMake flags as not being interpolatable
# glyphsToDelete = ['LISTOFGLYPHSHERE']

glyphsToDelete = AskString(
    'Space-separated set of glyphnames to delete').replace("'", "").replace(",", "").split(" ")

# help(CurrentFont().removeGlyph())

instruction = f"select masters to remove {glyphsToDelete} from"

inputFonts = getFile(
    instruction, allowsMultipleSelection=True, fileTypes=["ufo"])

for fontPath in inputFonts:
    f = OpenFont(fontPath, showInterface=False)
    # # open the fonts, then:
    for glyphName in glyphsToDelete:
        if glyphName in f.glyphOrder:
            f.removeGlyph(glyphName)
            print(f"removed {glyphName} from '{os.path.basename(fontPath)}'")
    print("done!")
    f.save()
    f.close()
