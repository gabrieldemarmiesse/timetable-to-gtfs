from difflib import SequenceMatcher
import io
import Other
import re

def read_string(element, have_to_get_name):
    if have_to_get_name:
        return element.name
    else:
        return element

def write_string(element, new_string, have_to_get_name):
    if have_to_get_name:
        element.name = new_string
        return element
    else:
        element = new_string
        return element

def fuse_two_stops(real_name, alias):
    real_id = Other.to_id(real_name)
    alias_id = Other.to_id(alias)

    # We first take care of stops.txt
    Other.replace_in_file("gtfs/stops.txt", alias, delete_line=True)

    # Now we take care of stop_times.txt
    Other.replace_in_file("gtfs/stop_times.txt", alias_id, real_id)

class Comparator:
    """ This class is here to compare two stops and tell if they're the same.
        An example is "Chap. Combes" and "Chapelle des Combes"
        The main deciding factor is SequenceMatcher.
        But after that, the user is always asked for his decision.
        Results of user's feedback is stored in files, so that the program won't ask him again.
        list_of_list_of_identical_stops contain what is in the file same_stops.txt
        first_list_differentiation, second_list_differentiation come from different_stops.txt
    """

    def __init__(self):

        self.list_differentiation = list()
        self.list_of_list_of_identical_stops = list()
        self.threshold = None

        try:
            with io.open("sgtfs/same_stops.txt", encoding="utf-8") as f:
                equalities = f.readlines()
        except FileNotFoundError:
            print("same_stops.txt not found")
            equalities = list()
        try:
            with io.open("sgtfs/different_stops.txt", encoding="utf-8") as f:
                differences = f.readlines()
        except FileNotFoundError:
            print("different_stops.txt not found")
            differences = list()

        for line in equalities:
            list_of_same_names = Other.split_by(line, "=")
            self.list_of_list_of_identical_stops.append(list_of_same_names)

        for line in differences:
            different_stops = Other.split_by(line, "!")
            self.list_differentiation.append(different_stops)

        try:
            with io.open("threshold.txt", encoding="utf-8") as f:
                line = f.readline()
                threshold = re.sub("\\n", "", line)
                threshold = threshold[1:]
        except FileNotFoundError:
            print("threshold.txt not found")
            threshold = "0.6"

        self.threshold = float(threshold)

    def compare(self, first_stop_name, second_stop_name, force_compare=False):

        # We need to check if the names were in the files
        found, result_files_search = self.compare_from_files(first_stop_name, second_stop_name)
        if found:
            return result_files_search
        else:

            a_lower = first_stop_name.lower()
            b_lower = second_stop_name.lower()

            p = SequenceMatcher(None, a_lower, b_lower).ratio()
            if p > self.threshold or force_compare:

                # We ask for user's feedback
                user_input = input("Is " + first_stop_name + " the same as " + second_stop_name + " ?  ")
                if user_input == "":
                    if not force_compare:
                        self.threshold -= 0.0015
                    self.store_relation(True, first_stop_name, second_stop_name)
                    return True
                else:
                    if not force_compare:
                        self.threshold += 0.01
                    self.store_relation(False, first_stop_name, second_stop_name)
                    return False

            else:
                return False

    def get_ressemblance(self, first_stop_name, second_stop_name):
        a_lower = first_stop_name.lower()
        b_lower = second_stop_name.lower()

        p = SequenceMatcher(None, a_lower, b_lower).ratio()
        return p

    def compare_from_files(self, first_stop_name, second_stop_name):
        """
        This function will check is this query has already be perfomed
        :param first_stop_name: The name of the first stop to lookup
        :param second_stop_name: The name of the second node to lookup
        :return: The first variable is if the query had already been made,
          The second one is if it's really the same stop (None if we don't know from previous experiences)
        """

        # Here we compare with the stops in the differencition file
        a = [first_stop_name, second_stop_name]
        b = [second_stop_name, first_stop_name]
        if a in self.list_differentiation or b in self.list_differentiation:
            return True, False

        # Now we look into the sames stops that have different names
        # for equality in self.list_of_list_of_identical_stops:
        #     if first_stop_name in equality and second_stop_name in equality:
        #         return True, True

        return False, None

    def store_relation(self, matching, first_stop_name, second_stop_name):
        if matching:
            self.store_same_stops(first_stop_name, second_stop_name)
        else:
            self.store_different_stops(first_stop_name, second_stop_name)

    def store_different_stops(self, first_stop_name, second_stop_name):
        self.list_differentiation.append([first_stop_name, second_stop_name])

    def store_same_stops(self, first_stop_name, second_stop_name):
        for equality in self.list_of_list_of_identical_stops:
            for stop in equality:
                if stop == first_stop_name:
                    equality.append(second_stop_name)
                    return
                if stop == second_stop_name:
                    equality.append(first_stop_name)
                    return
        self.list_of_list_of_identical_stops.append([first_stop_name, second_stop_name])

    def look_for_stop(self, stop_name):
        # This function look in the file same_stops.txt to see if the real name of the stop is known.

        for line in self.list_of_list_of_identical_stops:
            for name in line:
                if name.lower() == stop_name.lower():
                    return line[0]
        return stop_name

    def __exit__(self, *err):
        self.write_to_disk()

    def write_to_disk(self):
        # Here we write the data from the object in files so that it can be destroyed
        Other.write_list_of_list_in_file("sgtfs/same_stops.txt", self.list_of_list_of_identical_stops, "=")
        Other.write_list_of_list_in_file("sgtfs/different_stops.txt", self.list_differentiation, "!")
        Other.write_list_of_list_in_file("threshold.txt", [str(self.threshold), ], "")

    def __enter__(self):
        print('creating comparator')
        return self  # this is bound to the `as` part

    def update_list(self, list1, list2):
        # In the lists, it can be a string, a stop, or a stopOfGraph.
        # In consequences there are two function in charger of getting and
        # reading the string so that update_list works with those 3 types of objects.

        result_list = list()

        try:
            have_to_get_name_list1 = list1[0].__class__.__name__ != "str"
            have_to_get_name_list2 = list2[0].__class__.__name__ != "str"
        except IndexError:
            return

        for element in list1:

            # First we look in the same_stops.txt to check if we didn't already see this case
            new_name = self.look_for_stop(read_string(element, have_to_get_name_list1))

            if new_name == read_string(element, have_to_get_name_list1):
                # That means we didn't find the true name of the stop

                for element2 in list2:
                    string_element2 = read_string(element2, have_to_get_name_list2)
                    if self.compare(new_name, string_element2):
                        new_name = string_element2

            new_element = write_string(element, new_name, have_to_get_name_list1)
            result_list.append(new_element)

        return result_list

    def fuse_all_stops(self):
        for line in self.list_of_list_of_identical_stops:

            # The first element of line is supposed to be the real name so it's not in the for loop
            for alias in line[1:]:
                fuse_two_stops(line[0], alias)
