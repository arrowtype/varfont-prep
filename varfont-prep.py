# varfont prep



from vanilla.dialogs import *
import os
import shutil
import datetime
from fontTools.designspaceLib import BaseDocReader, DesignSpaceDocument
from mojo.UI import OutputWindow
import helpers
from helpers.removeGlyphs import *


debug = True

if debug == True:
    import importlib
    importlib.reload(helpers.removeGlyphs)
    from helpers.removeGlyphs import *


OutputWindow().show()
OutputWindow().clear()

report = """
Var Prep Report
********************************************  
  
"""

now = datetime.datetime.now()

def getSourcePathsFromDesignspace():

    designspacePath = getFile("select designspace for variable font",
                              allowsMultipleSelection=False, fileTypes=["designspace"])[0]

    designspace = DesignSpaceDocument.fromfile(designspacePath)

    inputFontPaths = []
    for source in designspace.sources:
        inputFontPaths.append(source.path)

    return designspacePath, inputFontPaths

def openFontsInList(fontPaths):
    fontsList = []
    for path in fontPaths:
        f = OpenFont(path, showInterface=False)
        fontsList.append(f)

    return fontsList


def checkIfSameFamilyName(fontsList):
    fontFamilyNames = []
    global report

    for f in fontsList:
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


def makeVarFontPrepFolder(fontsList, designspacePath):

    sameFamily, familyName = checkIfSameFamilyName(fontsList)

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

inputFontsList = openFontsInList(inputFontPaths)

newFolderPath = makeVarFontPrepFolder(inputFontsList, designspacePath)
copyFonts(inputFontPaths, newFolderPath)

print(inputFontsList)

for f in inputFontsList:
    f.close()

# open copied fonts in new dictionary
copiedFontPaths = []
for fontPath in inputFontPaths:
    head, tail = os.path.split(fontPath)
    newPath = newFolderPath + "/" + tail
    copiedFontPaths.append(newPath)
    print(newPath)

fontsList = openFontsInList(copiedFontPaths)

print(fontsList)


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



copiedFonts = []

# get paths
for file in os.listdir(newFolderPath):
    if os.path.splitext(file)[1] == ".ufo":
        copiedFonts.append(file)

listOfGlyphsLists = []

def addGlyphListToGlyphLists(f):

    fontName = f.info.familyName + " " + f.info.styleName

    # print(fontName)

    glyphs = []

    for g in f:
        glyphs.append(g.name)

    listOfGlyphsLists.append(glyphs)

# should you only remove glyphs ONCE? make list of compatible AND similar glyphs?
def constrainCharSetToSimilarGlyphs(f, commonGlyphs):
    global report

    report += "Unique glyphs removed from " + \
        f.info.familyName + " " + f.info.styleName + ":\n"

    # print(f.info.familyName + " " + f.info.styleName)

    # print(f.keys())

    diff = set(f.keys()) - set(commonGlyphs)

    print('diff of font keys vs commonGlyphs')
    # print(list(diff).sort())
    print(diff)

    uncommonGlyphs = []
    for g in f:
        if g.name not in commonGlyphs:
            uncommonGlyphs.append(g.name)
            # print(g.name + " removed from " + f.info.styleName)

            report += g.name + ", "

    print("removing uncommon glyphs from ", f.info.styleName)
    # print(list(uncommonGlyphs).sort())
    print(uncommonGlyphs)

    diffDiffs = set(diff) - set(uncommonGlyphs)

    print("\n--------------------------")
    print('diff of diffs?')
    print(diffDiffs)

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
    global report
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
    global report
    report += "******************* \n"
    report += "Guides removed from " + \
        f.info.familyName + " " + f.info.styleName + ":\n"

    for g in f:
        if g.guidelines != ():
            g.clearGuidelines()
            report += g.name + "; "

    report += "\n \n"

# --------------------------------------------------------------------------------------------------------
# compatiblity checks

def findCompatibleGlyphs(fontsList):
    global report

    nonCompatibleGlyphs = []
    nonCompatibleGlyphsReport = ""
    
    for g in fontsList[0]:
        # print(g.name)
        # f in all fonts
        for checkingFont in fontsList:
            # test glyphCompatibility
            if g.name in checkingFont.keys():
                glyphCompatibility = g.isCompatible(checkingFont[g.name])

                if glyphCompatibility[0] != True:
                    print(glyphCompatibility[0])
                    nonCompatibleGlyphs.append(g.name)
                    nonCompatibleGlyphsReport += g.name + \
                        "\n" + str(glyphCompatibility) + "\n"
            else :
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
print("\n---------------------------------------------------\n")
print("first pass: decompose nonExporting glyphs, remove guides, and find common glyphs")
for f in fontsList:
    # decompose non-exporting glyphs
    decomposeNonExportingComponents(f)
    # remove guides
    removeGuides(f)


# TODO (Urgent) – fix function to find uncommon glyphs. Currently seems to be failing

# in second pass, remove glyphs that aren't present in every font
print("\n---------------------------------------------------\n")
print("second pass: remove glyphs that aren't present in every font")

for f in fontsList:
    # create lists of glyphs in each font
    addGlyphListToGlyphLists(f)

# print("\n---------------------------------------------------\n")
# print("listOfGlyphsLists")
# print(listOfGlyphsLists)

# create one list of glyphs present in every font
commonGlyphs = set(listOfGlyphsLists[0]).intersection(*listOfGlyphsLists[1:])
# commonGlyphs = set(fontsList[0].keys()).intersection(*fontsList[1:].keys())

print("commonGlyphs")
print(commonGlyphs)

for f in fontsList:
    constrainCharSetToSimilarGlyphs(f, commonGlyphs)


# find compatible glyphs
nonCompatibleGlyphs = findCompatibleGlyphs(fontsList)

# remove nonCompatibleGlyphs from each font
for f in fontsList:
    removeNonCompatibleGlyphs(f, nonCompatibleGlyphs)


# --------------------------------------------------------------------------------------------------------
# kerning compatibility

# check if there is kerning in any of the UFOs
kerningInFonts = False

for f in fontsList:
    if len(f.kerning) > 0:
        kerningInFonts = True

# if there is kerning in some UFOs, check others and add blank kerning if needed
if kerningInFonts:
    report += "\n ******************* \n"
    for f in fontsList:
        if len(f.kerning) == 0:
            f.kerning[("A", "A")] = 0

            print("adding blank kerning to ", f.info.styleName)
            report += f"Adding blank kerning to {f.info.styleName}\n"

    report += "\n ******************* \n"


# --------------------------------------------------------------------------------------------------------
# sort fonts

print("\nsorting fonts\n")

def sortFont(font):
    # the new default is at the end, so this will re-apply a "smart sort" to the font
    newGlyphOrder = font.naked().unicodeData.sortGlyphNames(font.glyphOrder, sortDescriptors=[dict(type="cannedDesign", ascending=True, allowPseudoUnicode=True)])
    font.glyphOrder = newGlyphOrder

for f in fontsList:
    sortFont(f)


# --------------------------------------------------------------------------------------------------------
# close fonts

for f in fontsList:
    f.save()
    f.close()




#########################################################################
############# TO DO: present vanilla.ProgressBar ########################
#########################################################################

#########################################################################
############# TO DO: sort fonts in the same way #########################
#########################################################################

#########################################################################
############# TO DO: check anchor compatibility ? #######################
#########################################################################

#########################################
############# write report ##############
#########################################

reportOutput = open(newFolderPath + "/" + 'varfontprep-report.txt', 'w')
reportOutput.write(now.strftime("%H:%M:%S; %d %B, %Y\n\n"))
reportOutput.write("*******************\n")
reportOutput.write(report)
reportOutput.close()
