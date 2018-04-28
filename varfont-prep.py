### varfont prep

from vanilla.dialogs import *
import os
import datetime

now = datetime.datetime.now()
# from mojo.UI import AskYesNoCancel

# take in multiple fonts
    # give user the finder UI to select multiple fonts
    # or allow all open fonts
help(getFile)
inputFonts = getFile("select masters for var font", allowsMultipleSelection=True, fileTypes=["ufo"])

# print(inputFonts)

# help(OpenFont)

def checkIfSameFamilyName(inputFonts):
    fontFamilyNames = []

    for fontPath in inputFonts:
        f = OpenFont(fontPath, showUI=False)
        familyName = f.info.familyName
        fontFamilyNames.append(familyName)
        
    sameName = all(x==fontFamilyNames[0] for x in fontFamilyNames)
    
    if sameName == True:
        return sameName, fontFamilyNames[0]
    else:
        errorMsg = "The input UFOs have different font family names: " + str(set(fontFamilyNames))
        return errorMsg


# def uniqueFolderPath(path, number):
#     if os.path.exists(path):
#         number += 1
#         uniquePath += "-" + str(number)
#         uniqueFolderPath(uniquePath, number)
#     else:
#         print(path)
#         print(type(path))
#         return path # why doesn't this return the string??


def duplicateFontsToFolder(inputFonts):
    

    if checkIfSameFamilyName(inputFonts)[0] == True:
        
        # get family name
        familyName = checkIfSameFamilyName(inputFonts)[1]
        
        # make new folder name with font family name and "varfontprep" label
        newFolderName = familyName.replace(" ","_").lower() + "-varfontprep"
        
        # get path of first input font
        path = inputFonts[0]
        
        # get head of font path
        head, tail = os.path.split(path)

        # make new folder path
        newFolderPath = head + "/" + newFolderName

        if not os.path.exists(newFolderPath):
            os.mkdir(newFolderPath)
        else:
            newFolderPath += "-" now.strftime("%Y_%m_%d-%H_%M_%S")
            os.mkdir(newFolderPath)

    
    else:
        print(checkIfSameFamilyName(inputFonts))

duplicateFontsToFolder(inputFonts)

# duplicate these fonts, deleting all glyphs which can not be interpolated

    # check that font info matches
        # if not, 
            # send report 
            # stop process 

    # duplicate UFOs into new folder 
        # folderName = familyName + varfontprep

    # make a list of drawn glyphs in each
    # commonGlyphs = compare lists and come up with new list containing common items

    # for each item in commonGlyphs
    # count contours and points 
    # if there is a mismatch, delete glyph froom each input file and 
    # send "point mismatch" notice to report generator

# also generate a report of what glyphs can not be interpolated, and specify why not
    # different number of points
    # points/ contours out of order
