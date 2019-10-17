from vanilla.dialogs import *


inputFonts = getFile("select masters to add feature code to",
                     allowsMultipleSelection=True, fileTypes=["ufo"])


feaText = """\
languagesystem DFLT dflt;
languagesystem latn dflt;

"""


def addFeatureCode(f):
    f.features.text = feaText


for fontPath in inputFonts:
    f = OpenFont(fontPath, showInterface=False)
    addFeatureCode(f)
    fontName = f.info.familyName + " " + f.info.styleName
    print("feature code added to " + fontName)
    f.save()
    f.close()
