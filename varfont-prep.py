# varfont prep

from vanilla.dialogs import *
import os
import shutil
import datetime
from fontTools.designspaceLib import BaseDocReader, DesignSpaceDocument

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


def checkIfSameFamilyName(inputFontPaths):
    fontFamilyNames = []
    global report

    for fontPath in inputFontPaths:
        f = OpenFont(fontPath, showInterface=False)
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


def copyFonts(inputFontPaths, newFolderPath):
    for fontPath in inputFontPaths:
        head, tail = os.path.split(fontPath)

        # copy UFO into newFolderPath
        # "+ /varprep- +"  was formerly added to path, before tail
        shutil.copytree(fontPath, newFolderPath + "/" + tail)


def makeVarFontPrepFolder(inputFontPaths):

    # # check that selected fonts have same family name
    if checkIfSameFamilyName(inputFontPaths)[0] == True:
        # get family name
        familyName = checkIfSameFamilyName(inputFontPaths)[1]
    else:
        familyName = "error"

    # make new folder name with font family name and "varfontprep" label
    newFolderName = familyName.replace(" ", "_").lower() + "-varfontprep"

    # get path of first input font
    path = inputFontPaths[0]

    # get head of font path
    head, tail = os.path.split(path)

    # make new folder path
    newFolderPath = head + "/" + newFolderName

    now = datetime.datetime.now()
    newFolderPath += "-" + now.strftime("%Y_%m_%d-%H_%M_%S")
    os.mkdir(newFolderPath)
    print(newFolderPath)
    return str(newFolderPath)

    # if font family names are different, print the returned error
    # else:
    #     print(checkIfSameFamilyName(inputFontPaths))
    #     print("sorry, fonts have different family names")


def duplicateFontsToFontPrepFolder(inputFontPaths, newFolderPath):
    # # check that selected fonts have same family name
    if checkIfSameFamilyName(inputFontPaths)[0] == True:
        # newFolderPath = makeVarFontPrepFolder(inputFontPaths)

        print(newFolderPath)

        copyFonts(inputFontPaths, newFolderPath)
    else:
        print("sorry, fonts have different family names")


designspacePath, inputFontPaths = getSourcePathsFromDesignspace()
newFolderPath = makeVarFontPrepFolder(inputFontPaths)
duplicateFontsToFontPrepFolder(inputFontPaths, newFolderPath)

###############################################
######### copy and update designspace #########
###############################################


def copyDesignSpace(designspacePath):

    # duplicate designspace into new folder
    inputDStail = os.path.split(designspacePath)[1]
    outputDSpath = newFolderPath + "/" + inputDStail

    shutil.copyfile(designspacePath, outputDSpath)

    # update source & instance paths in designspace as needed
    outputDS = DesignSpaceDocument.fromfile(outputDSpath)

    for source in outputDS.sources:
        print(source.filename)  # prints the original value

        fontFilename = os.path.split(source.path)[1]
        setattr(source, 'filename', fontFilename)

        print(source.filename)  # this does change to the value I want

    # this doesn't overwrite the designspace file...
    outputDS.write(outputDSpath)


copyDesignSpace(designspacePath)

# #########################################
# ######### make fonts compatible #########
# #########################################

# glyphLists = []

# # create lists of glyphs in each font
# for fontFile in os.listdir(newFolderPath):
#     print(fontFile)
#     fullFontPath = newFolderPath + "/" + fontFile
#     print(fullFontPath)
#     f = OpenFont(fullFontPath, showInterface=False)
#     fontName = f.info.familyName + " " + f.info.styleName

#     print(fontName)

#     glyphs = []

#     for g in f:
#         glyphs.append(g.name)

#     glyphLists.append(glyphs)

# print(glyphLists)

# # create one list of glyphs present in every font
# commonGlyphs = set(glyphLists[0]).intersection(*glyphLists[1:])
# print(commonGlyphs)

# # remove glyphs that aren't present in every font
# for fontFile in os.listdir(newFolderPath):
#     fullFontPath = newFolderPath + "/" + fontFile
#     f = OpenFont(fullFontPath, showInterface=False)

#     report += "Unique glyphs removed from " + \
#         f.info.familyName + " " + f.info.styleName + ":\n"

#     print(f.info.familyName + " " + f.info.styleName)
#     for g in f:
#         print(g.name)

#         if g.name not in commonGlyphs:
#             f.removeGlyph(g.name)
#             print(g.name + " removed from " + f.info.styleName)

#             report += g.name + "; "

#     report += "\n \n"
#     f.save()
#     f.close()


# # decompose all glyphs to keep things compatible
# # TO DO: is this realy needed?
# # for fontFile in os.listdir(newFolderPath):
# #     fullFontPath = newFolderPath + "/" + fontFile
# #     f = OpenFont(fullFontPath, showInterface=False)

# #     report += "Glyphs decomposed for " + f.info.familyName + " " + f.info.styleName + ":\n"

# #     print(f.info.familyName + " " + f.info.styleName)
# #     for g in f:
# #         g.decompose()

# #     report += "\n \n"
# #     f.save()
# #     f.close()


# # set up empty list for compatible glyphs
# compatibleGlyphs = ["space"]
# nonCompatibleGlyphs = []
# compatibleGlyphsReport = ""
# nonCompatibleGlyphsReport = ""

# compatibilityChecked = False

# for fontFile in os.listdir(newFolderPath):
#     print(fontFile)
#     fullFontPath = newFolderPath + "/" + fontFile
#     print(fullFontPath)
#     f = OpenFont(fullFontPath, showInterface=False)
#     fontName = f.info.familyName + " " + f.info.styleName

#     # if compatibility has not yet been checked
#     if compatibilityChecked == False:
#         # for g in font1
#         for g in f:
#             # f in all fonts
#             for fontFile in os.listdir(newFolderPath):
#                 fullFontPath = newFolderPath + "/" + fontFile
#                 checkingFont = OpenFont(fullFontPath, showInterface=False)
#                 fontName = f.info.familyName + " " + f.info.styleName

#                 # test glyphCompatibility
#                 glyphCompatibility = g.isCompatible(checkingFont[g.name])

#                 if glyphCompatibility[0] == True:
#                     compatibleGlyphs.append(g.name)
#                     # compatibleGlyphsReport += g.name + "\n" + str(glyphCompatibility) + "\n"
#                 else:
#                     nonCompatibleGlyphs.append(g.name)
#                     nonCompatibleGlyphsReport += g.name + \
#                         "\n" + str(glyphCompatibility) + "\n"

#     # set to true to stop unnecessary looping
#     compatibilityChecked = True

# report += "\n ******************* \n"
# compatibleGlyphsSet = set(compatibleGlyphs)
# report += "compatibleGlyphs are " + str(compatibleGlyphsSet)

# # report += "\n ******************* \n"
# # report += "compatible glyphs: \n"
# # report += compatibleGlyphsReport

# report += "\n ******************* \n"
# report += "non-compatible glyphs: \n"
# report += nonCompatibleGlyphsReport

# # remove glyphs that aren't compatible in every font
# for fontFile in os.listdir(newFolderPath):
#     fullFontPath = newFolderPath + "/" + fontFile
#     f = OpenFont(fullFontPath, showInterface=False)

#     report += "\n ******************* \n"
#     report += "Non-compatible glyphs removed from " + \
#         f.info.familyName + " " + f.info.styleName + ":\n"

#     for g in f:
#         print(g.name)

#         if g.name in nonCompatibleGlyphs:
#             f.removeGlyph(g.name)

#             print(g.name + " removed from " + f.info.styleName)

#             report += " - " + g.name + "\n"

#     f.save()

#     for g in f.templateKeys():
#         f.removeGlyph(g)

#     f.save()

#     if 'space' not in f.keys():
#         f.newGlyph('space')
#         f['space'].unicode = '0020'
#         f['space'].width = 600

#     if f['space'].width == 0:
#         f['space'].width = 600

#     f.save()
#     f.close()

# # remove guides
# for fontFile in os.listdir(newFolderPath):
#     fullFontPath = newFolderPath + "/" + fontFile
#     f = OpenFont(fullFontPath, showInterface=False)

#     report += "******************* \n"
#     report += "Guides removed from " + \
#         f.info.familyName + " " + f.info.styleName + ":\n"

#     for g in f:
#         if g.guidelines != ():
#             g.clearGuidelines()
#             report += g.name + "; "

#     report += "\n \n"

#     f.save()
#     f.close()

# # decompose components
# # for fontFile in os.listdir(newFolderPath):
# #     fullFontPath = newFolderPath + "/" + fontFile
# #     f = OpenFont(fullFontPath, showInterface=False)

# #     report += "******************* \n"
# #     report += "Glyphs decomposes in " + f.info.familyName + " " + f.info.styleName + ":\n"

# #     for g in f:
# #         # if glyph has components
# #             # decompose components

# #     f.save()
# #     f.close()

# #########################################################  ################
# ############# TO DO: sort fonts in the same way ##############
# ######################################################### ################

# #########################################################  ################
# ############# TO DO?: check kerning compatibility ##############
# ######################################################### ################


# #########################################################  ################
# ############# TO DO: check anchor compatibility ##############
# ######################################################### ################


# #########################################################  ################
# ############# TO DO?: include designspace file handling? ##############
# ######################################################### ################

# # allow .designspace file extension to be selected

# # if a file is UFO, do the UFO stuff
# # if a file is designspace, move to new folder, with filenames updated to include varfontprep
#     # (if you want to add those to names)
#     # does adding stuff to the filename matter?


# #########################################
# ############# write report ##############
# #########################################

# reportOutput = open(newFolderPath + "/" + 'varfontprep-report.txt', 'w')
# reportOutput.write(now.strftime("%H:%M:%S; %d %B, %Y\n\n"))
# reportOutput.write("*******************\n")
# reportOutput.write(report)
# reportOutput.close()
