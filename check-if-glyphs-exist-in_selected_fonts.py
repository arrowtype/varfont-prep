
from vanilla.dialogs import *

inputFonts = getFile("select UFOs", allowsMultipleSelection=True, fileTypes=["ufo"])

lettersToCheckFor = ["a","f","g","i","l","r","y","a.roman","f.roman","g.roman","i.roman","l.roman","r.roman","y.roman", "a.italic","f.italic","g.italic","i.italic","l.italic","r.italic","y.italic"]




for fontPath in inputFonts:
    f = OpenFont(fontPath, showInterface=False)

    # do stuff to the font, e.g. sort, check anchors, add fea code, etc
    for gName in lettersToCheckFor:
        if gName not in f:
            print(f.info.styleName + " is missing glyph " + gName)

    f.save()
    f.close()