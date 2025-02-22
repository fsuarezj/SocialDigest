import json

class DataSources:
    """
    Class to manage Twitter data sources.
    """
    def __init__(self, file_path):
        """
        Constructor for DataSources class.

        Args:
            file_path (str): path to the json file containing the data sources.
        """
        self.file_path = file_path
        self.data_sources = self._load_data_sources()
        
        # Ensure all data sources have the same keys
        if self.data_sources:
            self.keys = self.data_sources[0].keys()
            for source in self.data_sources:
                if source.keys() != self.keys:
                    raise ValueError("All data sources must have the same keys")

    def _load_data_sources(self):
        """
        Load data sources from file and return a list of dictionaries.
        """
        with open(self.file_path, 'r') as file:
            return json.load(file)

    def check_for_duplicates(self):
        """
        Check if there are any duplicates in the data sources list.

        Returns:
            list: list of dictionaries of the duplicates.
        """
        seen = set()
        duplicates = []
        for source in self.data_sources:
            if source['twitter_account'] in seen:
                duplicates.append(source)
            else:
                seen.add(source['twitter_account'])
        return duplicates

    def add_new_data_source(self, new_source, duplication_key):
        """
        Add a new data source to the list of data sources.

        Args:
            new_source (dict): dictionary of the new data source.
            duplication_key (str): key to check for duplicates. Defaults to 'twitter_account'.

        Returns:
            bool: True if the source was added, False if it already exists.
        """
        if set(new_source.keys()) == self.keys and new_source[duplication_key] not in [source[duplication_key] for source in self.data_sources]:
            self.data_sources.append(new_source)
            self._save_data_sources()
            return True
        return False

    def _save_data_sources(self):
        """
        Save the data sources to the file.
        """
        with open(self.file_path, 'w') as file:
            json.dump(self.data_sources, file, indent=4)

    def get_all_sources(self):
        """
        Return a list of all the data sources with the given key.

        Args:
            key (str): key to get the values for.

        Returns:
            list: list of strings of the data sources with the given key.
        """
        return self.data_sources

    def get_all_sources_key(self, key):
        """
        Return a list of all the data sources with the given key.

        Args:
            key (str): key to get the values for.

        Returns:
            list: list of strings of the data sources with the given key.
        """
        return [source[key] for source in self.data_sources]

    def filter_data_sources(self, filters=None):
        """
        Filter the data sources by specified criteria.

        Args:
            filters (dict): dictionary where keys are data source keys to filter by, and values are lists of acceptable values.

        Returns:
            list: list of dictionaries of the filtered data sources.
        """
        if filters is None:
            return self.data_sources

        filtered_sources = self.data_sources
        for key, values in filters.items():
            if not isinstance(values, list):
                values = [values]
            filtered_sources = [source for source in filtered_sources if source.get(key) in values]
        return filtered_sources
