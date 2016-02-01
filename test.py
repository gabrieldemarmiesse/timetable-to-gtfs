import codecs

with codecs.open("lol.txt", encoding="utf-8") as f:
    bla = f.readline()


file = codecs.open("lolfjr.txt", "w", "utf-8")
file.write(bla)
file.close()