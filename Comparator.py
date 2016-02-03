from difflib import SequenceMatcher
import io


class Comparator:
    """ This class is here to compare two stops and tell if they're the same.
        An example is "Chap. Combes" and "Chapelle des Combes"
        The main deciding factor is SequenceMatcher.
        But after that, the user is always asked for his decision.
        Results of user's feedback is stored in files, so that the program won't ask him again.
        list_of_list_of_identical_stops contain what is in the file same_stops.txt
        first_list_differentiation, second_list_differentiation come from different_stops.txt
    """

    def __self__(self):
        try:
            with io.open("same_stops.txt", encoding="utf-8") as f:
                equalities = f.readlines()
        except FileNotFoundError:
            equalities = list()

        try:
            with io.open("different_stops.txt", encoding="uft-8") as f:
                differences = f.readlines()
        except FileNotFoundError:
            differences = list()
        self.first_list_differentiation = first_list_differentiation
        self.second_list_differentiation = second_list_differentiation
        self.list_of_list_of_identical_stops = list_of_list_of_identical_stops
        self.threshold = threshold


    def compare(self, first_stop_name, second_stop_name):
        a_lower = first_stop_name.lower()
        b_lower = second_stop_name.lower()

        p = SequenceMatcher(None, a_lower, b_lower).ratio()
        if p > self.threshold:

            # We need to check if the names were in the files
            found, result_files_search = self.compare_from_files(first_stop_name, second_stop_name)
            if found:
                return result_files_search
            else:

                # We ask for user's feedback
                user_input = input("Is " + first_stop_name + "the same as " + second_stop_name + " ?  ")
                if user_input == "":
                    self.threshold -= 0.0015
                    self.store_relation(True, first_stop_name, second_stop_name)
                    return True
                else:
                    self.threshold += 0.01
                    self.store_relation(False, first_stop_name, second_stop_name)
                    return False

        else:
            return False

    def compare_from_files(self, first_stop_name, second_stop_name):
        """
        This function will check is this query has already be perfomed
        :param first_stop_name: The name of the first stop to lookup
        :param second_stop_name: The name of the second node to lookup
        :return: The first variable is if the query had already been made,
          The second one is if it's really the same stop (None if we don't know from previous experiences)
        """

        # Here we compare with the stops in the differencition file
        for i, stop_name in enumerate(self.first_list_differentiation):
            if first_stop_name == stop_name:
                if second_stop_name == self.second_list_differentiation[i]:
                    return True, False
            elif second_stop_name == stop_name:
                if first_stop_name == self.second_list_differentiation[i]:
                    return True, False

        # Now we look into the sames stops that have different names
        for equality in self.list_of_list_of_identical_stops:
            found_first = False
            found_second = False
            for stop_name in equality:
                if stop_name == first_stop_name:
                    found_first = True
                if stop_name == second_stop_name:
                    found_second = True
            if found_first and found_second:
                return True, True

        return False, None

    def store_relation(self, matching, first_stop_name, second_stop_name):
        if matching:
            self.store_different_stops(first_stop_name, second_stop_name)
        else:
            self.store_same_stops(first_stop_name, second_stop_name)

    def store_different_stops(self, first_stop_name, second_stop_name):
        self.first_list_differentiation.append(first_stop_name)
        self.second_list_differentiation.append(second_stop_name)

    def store_same_stops(self, first_stop_name, second_stop_name):
        for equality in self.list_of_list_of_identical_stops:
            for stop in equality:
                if stop == first_stop_name:
                    equality.append(second_stop_name)
                    return
                if stop == second_stop_name:
                    equality.append(first_stop_name)
                    return

    def __exit__(self, *err):
        self.write_to_disk()

    def write_to_disk(self):
        # Here we write the data from the object in files so that it can be destroyed
        pass

    def __enter__(self):
        print('creating comparator')
        return self  # this is bound to the `as` part
