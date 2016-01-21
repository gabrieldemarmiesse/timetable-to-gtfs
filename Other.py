import csv

def read_cvs(path,func):
    with open(path, 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i, row in enumerate(spamreader):
                if(i>0):
                    func(row)