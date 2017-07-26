# bb_setup.py
from bbfreeze import Freezer

f = Freezer(distdir="bb-binary")
f.addScript("cyto_tissue_comp.py", gui_only=True)
# f.setIcon('favicon.ico')
f()
