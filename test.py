import io

with io.open("lol.txt", "r", encoding="utf-8") as f:
    bla = f.readline()


file = io.open("lolfjr.txt", "w", encoding="utf-8")
file.write(bla)
file.close()
