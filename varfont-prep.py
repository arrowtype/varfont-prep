### varfont prep

# take in multiple fonts
    # give user the finder UI to select multiple fonts
    # or allow all open fonts


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
