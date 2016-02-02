from difflib import SequenceMatcher


class Comparator:

    def __self__(self, first_list_differentiation, second_list_differentiation,
                 list_of_list_of_identical_stops, threshold):

        self.first_list_differentiation = first_list_differentiation
        self.second_list_differentiation = second_list_differentiation
        self.list_of_list_of_identical_stops = list_of_list_of_identical_stops
        self.threshold = threshold

    @classmethod
    def init_from_files(cls):
        pass

    def compare(self, first_stop_name, second_stop_name):
        a_lower = first_stop_name.lower()
        b_lower = second_stop_name.lower()

        p = SequenceMatcher(None, a_lower, b_lower).ratio()
        if p > self.threshold:

            # We need to check if the names were in the files
            result_files_search = self.compare_from_files(first_stop_name, second_stop_name)
            if result_files_search:
                return True
            elif not result_files_search:
                return False
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
        pass

    def store_relation(self, matching, first_stop_name, second_stop_name):
        pass
