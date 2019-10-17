from vanilla.dialogs import *
files = getFile("Select files to check for character set similarity", allowsMultipleSelection=True, fileTypes=["ufo"])

for file in files:
    f = OpenFont(file, showInterface=False)
    
    for g in f:
        g.decompose()
        g.clearAnchors()
        
        
    f.save()
    
    f.close()