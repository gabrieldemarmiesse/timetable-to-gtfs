import csv


def read_cvs(path, func):
    try:
        with open(path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i, row in enumerate(spamreader):
                if i > 0:
                    func(row)
            return False
    except :
        # There was an issue while opening the file
        return True
