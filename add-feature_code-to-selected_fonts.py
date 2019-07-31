from vanilla.dialogs import *


inputFonts = getFile("select masters to add feature code to",
                     allowsMultipleSelection=True, fileTypes=["ufo"])


feaText = """\
languagesystem DFLT dflt;
languagesystem latn dflt;

@defaultletters    = [a        c        d        e        f        g        h        i        j        k        l        m        n        r        s        u        v        w        x        y        z];
@trueitalics       = [a.italic c.italic d.italic e.italic f.italic g.italic h.italic i.italic j.italic k.italic l.italic m.italic n.italic r.italic s.italic u.italic v.italic w.italic x.italic y.italic z.italic ];

feature ss01 {
    featureNames {
		name 3 1 0x0409 "italic alternates"; # Win  Unicode  English US
		name 1 0 0 "italic alternates"; #   Mac  Roman  English
	};
    sub @defaultletters by @trueitalics;
} ss01;
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
