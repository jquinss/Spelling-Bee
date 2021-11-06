# helper class to format the output of a string

class Formatter:
    @staticmethod
    def iterable_to_string(iterable, separator=""):
        return separator.join(str(item) for item in iterable)

    @staticmethod
    def insert_into_string(index_dict, string):
        new_string = []
        last_index = 0
        for index in index_dict.keys():
            new_string.append(string[last_index:index])
            new_string.append(index_dict[index])
            last_index = index
        new_string.append(string[last_index:])
        return Formatter.iterable_to_string(new_string)
