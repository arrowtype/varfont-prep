from vanilla.dialogs import *

inputFonts = getFile("select masters for var font", allowsMultipleSelection=True, fileTypes=["ufo"])

for fontPath in inputFonts:
    f = OpenFont(fontPath, showInterface=False)
    newGlyphOrder = f.naked().unicodeData.sortGlyphNames(f.glyphOrder, sortDescriptors=[dict(type="cannedDesign", ascending=True, allowPseudoUnicode=True)])
    f.glyphOrder = newGlyphOrder
    f.save()
    f.close()