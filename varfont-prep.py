### varfont prep

from vanilla.dialogs import *
import os
import shutil
import datetime

# take in multiple fonts
inputFonts = getFile("select masters for var font", allowsMultipleSelection=True, fileTypes=["ufo"])

# def generateReport(inputFonts, errors):
#     newFolderPath = makeVarFontPrepFolder(inputFonts)
    
#     report = open(newFolderPath + "/" + 'varfontprep-report.txt','w')
#     report.write(str(errors))
#     report.close()

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
        generateReport(inputFonts, errorMsg)
        # return errorMsg
        

def copyFonts(inputFonts, newFolderPath):
    for fontPath in inputFonts:
        head, tail = os.path.split(fontPath)
        
        # copy UFO into newFolderPath
        shutil.copytree(fontPath, newFolderPath + "/varprep-" + tail)

def makeVarFontPrepFolder(inputFonts):
    
    # # check that selected fonts have same family name
    # if checkIfSameFamilyName(inputFonts)[0] == True:
        
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
        print(newFolderPath)
        return str(newFolderPath)
    else:
        # add current date & time to folder path if the base name is already taken
        now = datetime.datetime.now()
        newFolderPath += "-" + now.strftime("%Y_%m_%d-%H_%M_%S")
        os.mkdir(newFolderPath)
        print(newFolderPath)
        return str(newFolderPath)

    # # if font family names are different, print the returned error
    # else:
    #     print(checkIfSameFamilyName(inputFonts))
    #     print("sorry, fonts have different family names")


def duplicateFontsToFontPrepFolder(inputFonts, newFolderPath):
    # # check that selected fonts have same family name
    if checkIfSameFamilyName(inputFonts)[0] == True:
        # newFolderPath = makeVarFontPrepFolder(inputFonts)
    
        print(newFolderPath)
    
        copyFonts(inputFonts, newFolderPath)
    else:
        print("sorry, fonts have different family names")

newFolderPath = makeVarFontPrepFolder(inputFonts)
duplicateFontsToFontPrepFolder(inputFonts, newFolderPath)

######################################### 
######### make fonts compatible #########
#########################################

glyphLists = []

for fontFile in os.listdir(newFolderPath):
    print(fontFile)
    fullFontPath = newFolderPath + "/" + fontFile 
    print(fullFontPath)
    f = OpenFont(fullFontPath, showUI=False)
    fontName = f.info.familyName + " " + f.info.styleName
    
    print(fontName)
    
    glyphs = []
    
    for g in f:
        glyphs.append(g.name)
    
    glyphLists.append(glyphs)

print(glyphLists)
    






