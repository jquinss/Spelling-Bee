import json
from random import randint
from abc import ABC, abstractmethod


class LookupService(ABC):
    def __init__(self, source_files_dict=None):
        if source_files_dict is not None:
            self.data_source = self.load_data_source(source_files_dict)
        else:
            self.data_source = None

    @abstractmethod
    def load_source_file(self, source_file): # loads data from a file to a dictionary
        """Primitive operation. It needs to be overriden. Different implementations may exist, depending on the data
        source format (e.g. JSON, XML, etc.)"""
        pass

    def lookup_entry(self, data_source_index, entry_index):
        """
            :param data_source_index: index of the dictionary
            :param entry_index: index of the entry inside the dictionary
            :return: dictionary entry or None (if no entry is found)
        """
        if self.data_source is None:
            raise InvalidDataSourceException("No data source has been provided. Load a data source file first")
        if entry_index in self.data_source[data_source_index]:
            return self.data_source[data_source_index][entry_index]
        return None

    def get_random_entry_index(self, data_source_index):
        """
            :param data_source_index: index of the dictionary
            :return: random index inside the dictionary
        """
        if self.data_source is None:
            raise InvalidDataSourceException("No data source has been provided. Load a data source file first")
        rand_num = randint(0, len(self.data_source[data_source_index]))
        random_index = list(self.data_source[data_source_index].keys())[rand_num]
        return random_index

    def load_data_source(self, source_files_dict): # loads data from multiples files to a dictionary of dictionaries
        data_source = {}
        for source_file_index in source_files_dict:
            data_source[source_file_index] = self.load_source_file(source_files_dict[source_file_index])
        return data_source

    def add_source_files(self, source_files_dict):
        self.data_source = self.load_data_source(source_files_dict)


class JSONLookupService(LookupService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_source_file(self, json_source_file):
        with open(json_source_file) as json_file:
            data = json.load(json_file)
        return data


class LookupServiceFactory:
    def create_lookup_service(self, lookup_type, source_files_dict):
        if lookup_type == 'JSON':
            return JSONLookupService(source_files_dict=source_files_dict)
        else:
            raise ValueError(lookup_type)


class InvalidDataSourceException(Exception):
    pass
