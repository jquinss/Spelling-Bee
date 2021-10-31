class Formatter:
    @staticmethod
    def collection_to_string(collection, separator=None):
        output = ''
        if separator is not None and separator != "":
            for i in range(len(collection)):
                output += str(collection[i]) + str(separator)
            output = output[:-1]
        else:
            for element in collection:
                output += str(element)
        return output

    @staticmethod
    def insert_into_string(index_dict, string):
        new_string = []
        last_index = 0
        for index in index_dict.keys():
            new_string.append(string[last_index:index])
            new_string.append(index_dict[index])
            last_index = index
        new_string.append(string[last_index:])
        return Formatter.collection_to_string(new_string)
