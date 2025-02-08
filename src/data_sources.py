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

    def add_new_data_source(self, new_source):
        """
        Add a new data source to the list of data sources.

        Args:
            new_source (dict): dictionary of the new data source.

        Returns:
            bool: True if the source was added, False if it already exists.
        """
        if new_source['twitter_account'] not in [source['twitter_account'] for source in self.data_sources]:
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

    def get_all_data_sources(self):
        """
        Return a list of all the data sources as a list of strings.

        Returns:
            list: list of strings of the data sources.
        """
        return [source['twitter_account'] for source in self.data_sources]

    def filter_data_sources(self, source_type=None, bias=None):
        """
        Filter the data sources by source type and bias.

        Args:
            source_type (str): type of source to filter by.
            bias (str): bias of source to filter by.

        Returns:
            list: list of dictionaries of the filtered data sources.
        """
        filtered_sources = self.data_sources
        if source_type:
            filtered_sources = [source for source in filtered_sources if source['type'] == source_type]
        if bias:
            filtered_sources = [source for source in filtered_sources if source['bias'] == bias]
        return filtered_sources
