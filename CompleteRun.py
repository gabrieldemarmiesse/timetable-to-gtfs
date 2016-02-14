import Agency
import Other
import os


# Here we check that the files are really in UTF-8 without BOM
a = os.listdir("sgtfs")
for filename in a:
    Other.delete_BOM("sgtfs/" + filename)


Agency.Agency.update()
