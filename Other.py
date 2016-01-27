import csv


def read_cvs(path, func):
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
    # Convert a list of elements to a cvs line

    line = ""
    for element in list_of_elements:
        csv_element = ",\"" + element + "\""
        line += csv_element

    line += "\n"

    # There is a comma at the beggining
    line_witout_first_comma = line[1:]
    return line_witout_first_comma


def export_in_csv(objects_list, first_line, filename):
    pass

    # TODO
