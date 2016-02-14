import os
import Other

a = os.listdir("sgtfs")
for filename in a:
    Other.delete_BOM("sgtfs/" + filename)