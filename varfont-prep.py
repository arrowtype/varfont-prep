# varfont prep

from vanilla.dialogs import *
import os
import shutil
import datetime
from fontTools.designspaceLib import BaseDocReader, DesignSpaceDocument

from helpers.removeGlyphs import removeGlyphs

report = """
Var Prep Report
********************************************  
  
"""

now = datetime.datetime.now()

def getSourcePathsFromDesignspace():

    designspacePath = getFile("select designspace for variable font",
                              allowsMultipleSelection=True, fileTypes=["designspace"])[0]

    designspace = DesignSpaceDocument.fromfile(designspacePath)

    inputFontPaths = []
    for source in designspace.sources:
        inputFontPaths.append(source.path)

    return designspacePath, inputFontPaths

def openFontsInDict(fontPaths):
    fontsDict = {}
    for path in fontPaths:
        f = OpenFont(path, showInterface=False)
        fontsDict[path] = f

    return fontsDict


def checkIfSameFamilyName(fontsDict):
    fontFamilyNames = []
    global report

    for f in fontsDict.values():
        familyName = f.info.familyName
        fontFamilyNames.append(familyName)

    sameName = all(x == fontFamilyNames[0] for x in fontFamilyNames)

    if sameName == True:
        return sameName, fontFamilyNames[0]
    else:
        errorMsg = "The input UFOs have different font family names: " + \
            str(set(fontFamilyNames))
        # generateReport(inputFontPaths, errorMsg)

        report += errorMsg + "\n"

        return False, fontFamilyNames[0]
        # return errorMsg




def makeVarFontPrepFolder(fontsDict, designspacePath):

    sameFamily, familyName = checkIfSameFamilyName(fontsDict)

    # # check that selected fonts have same family name
    if sameFamily == True:
        # get family name
        familyName = familyName
    else:
        familyName = "ERROR: families have different names"

    # make new folder name with font family name and "varfontprep" label
    newFolderName = familyName.replace(" ", "_").lower() + "-varfontprep"

    # get head of font path
    head, tail = os.path.split(designspacePath)

    # make new folder path
    newFolderPath = head + "/" + newFolderName

    now = datetime.datetime.now()
    newFolderPath += "-" + now.strftime("%Y_%m_%d-%H_%M_%S")
    os.mkdir(newFolderPath)
    print(newFolderPath)
    return str(newFolderPath)


def copyFonts(inputFontPaths, newFolderPath):
    for fontPath in inputFontPaths:
        head, tail = os.path.split(fontPath)

        newPath = newFolderPath + "/" + tail

        if os.path.exists(newPath) == False:

            # copy UFO into newFolderPath
            # "+ /varprep- +"  was formerly added to path, before tail
            shutil.copytree(fontPath, newPath)


designspacePath, inputFontPaths = getSourcePathsFromDesignspace()
fontsDict = openFontsInDict(inputFontPaths)
newFolderPath = makeVarFontPrepFolder(fontsDict, designspacePath)
copyFonts(inputFontPaths, newFolderPath)


###############################################
######### copy and update designspace #########


def copyDesignSpace(designspacePath, newFolderPath):

    # duplicate designspace into new folder
    inputDStail = os.path.split(designspacePath)[1]
    outputDSpath = newFolderPath + "/" + inputDStail

    shutil.copyfile(designspacePath, outputDSpath)

    # update source & instance paths in designspace as needed
    outputDS = DesignSpaceDocument.fromfile(outputDSpath)

    # updates path if sources were originally in a different directory than designspace file
    for source in outputDS.sources:
        newFontPath = newFolderPath + '/' + os.path.split(source.path)[1]
        source.path = newFontPath

    outputDS.write(outputDSpath)


copyDesignSpace(designspacePath, newFolderPath)





#########################################
######### make fonts compatible #########
#########################################

glyphLists = []

copiedFonts = []

# get paths
for file in os.listdir(newFolderPath):
    if os.path.splitext(file)[1] == ".ufo":
        copiedFonts.append(file)


def addGlyphListToGlyphLists(f):

    fontName = f.info.familyName + " " + f.info.styleName

    print(fontName)

    glyphs = []

    for g in f:
        glyphs.append(g.name)

    glyphLists.append(glyphs)

# should you only remove glyphs ONCE? make list of compatible AND similar glyphs?
def constrainCharSetToSimilarGlyphs(f, commonGlyphs):

    report += "Unique glyphs removed from " + \
        f.info.familyName + " " + f.info.styleName + ":\n"

    print(f.info.familyName + " " + f.info.styleName)

    uncommonGlyphs = []
    for g in f:
        print(g.name)

        if g.name not in commonGlyphs:
            uncommonGlyphs.append(g.name)
            print(g.name + " removed from " + f.info.styleName)

            report += g.name + "; "

    removeGlyphs(f, uncommonGlyphs)

    report += "\n \n"

# --------------------------------------------------------------------------------------------------------
# decompose non-exporting glyphs (glyphs with a dot leading in their name, such as ".arrowhead")

def nonExporting(glyphName):
    if glyphName[0] == "_":
        return True

def findAndDecomposeComponents(font, componentNames):
    for g in font:
        if len(g.components) > 0:
            for component in g.components:
                if component.baseGlyph in componentNames:
                    component.decompose()

def decomposeNonExportingComponents(f):
    nonExportingGlyphs = []

    for g in f:
        if nonExporting(g.name) == True:
            # add to list
            nonExportingGlyphs.append(g.name)

    findAndDecomposeComponents(f, nonExportingGlyphs)
    removeGlyphs(f, nonExportingGlyphs)

    report += f"Decomposed and removed non-exporting glyphs: {nonExportingGlyphs}"

# --------------------------------------------------------------------------------------------------------
# remove guides


def removeGuides(f):
    report += "******************* \n"
    report += "Guides removed from " + \
        f.info.familyName + " " + f.info.styleName + ":\n"

    for g in f:
        if g.guidelines != ():
            g.clearGuidelines()
            report += g.name + "; "

    report += "\n \n"

    f.save()
    f.close()

# --------------------------------------------------------------------------------------------------------
# compatiblity checks

def findCompatibleGlyphs(fontsDict):
    nonCompatibleGlyphs = []
    nonCompatibleGlyphsReport = ""
    
    for g in fontsDict.values()[0]:
        # f in all fonts
        for checkingFont in fontsDict.values():
            # test glyphCompatibility
            glyphCompatibility = g.isCompatible(checkingFont[g.name])

            if glyphCompatibility[0] != True:
                nonCompatibleGlyphs.append(g.name)
                nonCompatibleGlyphsReport += g.name + \
                    "\n" + str(glyphCompatibility) + "\n"

    report += "\n ******************* \n"
    report += "non-compatible glyphs removed: \n"
    report += nonCompatibleGlyphsReport

    return nonCompatibleGlyphs

# remove glyphs that aren't compatible in every font
def removeNonCompatibleGlyphs(f, nonCompatibleGlyphs):

    removeGlyphs(f, nonCompatibleGlyphs)

    for g in f.templateKeys():
        f.removeGlyph(g)

    if 'space' not in f.keys():
        f.newGlyph('space')
        f['space'].unicode = '0020'
        f['space'].width = 600

    if f['space'].width == 0:
        f['space'].width = 600


# --------------------------------------------------------------------------------------------------------
# FIX FILES

# in first pass, decompose nonExporting glyphs, remove guides, and find common glyphs
for f in fontsDict.values():
    # decompose non-exporting glyphs
    decomposeNonExportingComponents(f)
    # remove guides
    removeGuides(f)

# in second pass, remove glyphs that aren't present in every font
for f in fontsDict.values():
    # create lists of glyphs in each font
    addGlyphListToGlyphLists(fontFile)
    # create one list of glyphs present in every font
    commonGlyphs = set(glyphLists[0]).intersection(*glyphLists[1:])

    constrainCharSetToSimilarGlyphs(f, commonGlyphs)

# find compatible glyphs
nonCompatibleGlyphs = findCompatibleGlyphs(fontsDict)

# remove nonCompatibleGlyphs from each font
for f in fontsDict.values():
    removeNonCompatibleGlyphs(f, nonCompatibleGlyphs)

for f in fontsDict.values():
    f.save()
    f.close()


#########################################################  ################
############# TO DO: sort fonts in the same way ##############
######################################################### ################

#########################################################  ################
############# TO DO?: check kerning compatibility ##############
# check that kerning exists in every UFO. If it doesn't, add blank kerning.
######################################################### ################


#########################################################  ################
############# TO DO: check anchor compatibility ? ##############
######################################################### ################

#########################################
############# write report ##############
#########################################

reportOutput = open(newFolderPath + "/" + 'varfontprep-report.txt', 'w')
reportOutput.write(now.strftime("%H:%M:%S; %d %B, %Y\n\n"))
reportOutput.write("*******************\n")
reportOutput.write(report)
reportOutput.close()
