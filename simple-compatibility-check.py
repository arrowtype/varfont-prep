cf=CurrentFont()

glyphToCheck= "uni0162"

for f in AllFonts():
    print(f.info.styleName)
    print(cf[glyphToCheck].isCompatible(f[glyphToCheck]))