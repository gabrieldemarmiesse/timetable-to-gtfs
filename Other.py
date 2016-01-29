import csv
import os

def read_csv(path, func):
    """
    This method execute a function for each line of a file (except the first one)
    :param path: the path of the file to open
    :param func: the function to execute at each line of the file
    :return: return true if the file didn't exist
    """

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
        file = open(path, 'w')
        file.write(first_line + "\n")
        for my_object in objects_list:
            file.write(list_to_csv(my_object.to_list()))

        print("finished exporting " + filename)
    else:
        print("The list of objects was empty")
