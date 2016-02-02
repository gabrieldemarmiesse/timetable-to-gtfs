import csv
import os
import re
import io
from difflib import SequenceMatcher

threshold = None
def read_csv(path, func):
    """
    This method execute a function for each line of a file (except the first one)
    :param path: the path of the file to open
    :param func: the function to execute at each line of the file
    :return: return true if the file didn't exist
    """

    try:
        with io.open(path, 'r', encoding="utf-8") as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for i, row in enumerate(spamreader):
                if i > 0:
                    func(row)
            return False
    except :
        # There was an issue while opening the file
        return True


def list_to_csv(list_of_elements):
    # Convert a list of elements to a csv line

    line = ""
    for element in list_of_elements:
        csv_element = ",\"" + str(element) + "\""
        line += csv_element

    line += "\n"

    # There is a comma at the beggining
    line_witout_first_comma = line[1:]
    return line_witout_first_comma


def export_in_csv(objects_list, filename):
    if len(objects_list) > 0:
        first_line = objects_list[0].get_first_line_csv()
        path = "gtfs/" + filename
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        file = io.open(path, 'w', encoding="utf-8")
        file.write(first_line + "\n")
        for my_object in objects_list:
            file.write(list_to_csv(my_object.to_list()))

        print("finished exporting " + filename)
    else:
        print("The list of objects was empty")


def to_real_time(string):
    # Convert 6:34 in 06:34:00
    if len(string) == 8 or len(string) == 0:
        return string
    elif len(string) == 5:
        return string + ":00"
    elif len(string) == 4:
        return "0" + string + ":00"


# This function create an id for the stop from it's file name.
def to_id(string):
    stop_id2 = string.replace(" ", "")
    stop_id1 = stop_id2.replace(".", "")
    stop_id3 = stop_id1.replace("'", "")
    stop_id = stop_id3.replace("-", "")
    return stop_id.lower()


# This function parse a line containing element separated by multiple separators
def split_by(string, separator):
    if separator == "\t":
        separator = "\\t"

    string1 = string.replace("\n", "")
    return re.split(" *" + separator + "+ *", string1)


def init_the_threshold():
    pass


def store_the_threshold():
    pass


# We should put a variable threshold
def similar(a, b):
    global threshold
    if threshold is None:
        init_the_threshold()

    p = SequenceMatcher(None, a, b).ratio()
    if p > threshold:

        # We ask for user's feedback
        user_input = input("Is " + a + "the same as " + b + " ?  ")
        if user_input == "":
            threshold -= 0.0015
            return True
        else:
            threshold += 0.01
            return False

    else:
        return False