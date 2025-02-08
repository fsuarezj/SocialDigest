import pytest
import os
import json
from data_sources import DataSources


@pytest.fixture(autouse=True)
def setup_and_teardown():
    test_file_path = 'test_data_sources.json'
    test_data = [
        {"twitter_account": "account1", "type": "news", "bias": "neutral"},
        {"twitter_account": "account2", "type": "blog", "bias": "left"},
        {"twitter_account": "account3", "type": "news", "bias": "right"}
    ]
    with open(test_file_path, 'w') as file:
        json.dump(test_data, file)
    yield test_data
    os.remove(test_file_path)


def test_load_data_sources(setup_and_teardown):
    uganda_data_sources = DataSources('test_data_sources.json')
    assert len(uganda_data_sources.data_sources) == 3


def test_check_for_duplicates(setup_and_teardown):
    test_data = setup_and_teardown
    uganda_data_sources = DataSources('test_data_sources.json')
    duplicates = uganda_data_sources.check_for_duplicates()
    assert len(duplicates) == 0
    uganda_data_sources.data_sources.append(test_data[0])
    duplicates = uganda_data_sources.check_for_duplicates()
    assert len(duplicates) == 1


def test_add_new_data_source(setup_and_teardown):
    uganda_data_sources = DataSources('test_data_sources.json')
    new_source = {"twitter_account": "account4", "type": "news", "bias": "neutral"}
    result = uganda_data_sources.add_new_data_source(new_source)
    assert result
    assert len(uganda_data_sources.data_sources) == 4
    result = uganda_data_sources.add_new_data_source(new_source)
    assert not result


def test_get_all_data_sources(setup_and_teardown):
    uganda_data_sources = DataSources('test_data_sources.json')
    accounts = uganda_data_sources.get_all_data_sources()
    assert accounts == ["account1", "account2", "account3"]


def test_filter_data_sources(setup_and_teardown):
    uganda_data_sources = DataSources('test_data_sources.json')
    filtered_sources = uganda_data_sources.filter_data_sources(source_type="news")
    assert len(filtered_sources) == 2
    filtered_sources = uganda_data_sources.filter_data_sources(bias="left")
    assert len(filtered_sources) == 1
    filtered_sources = uganda_data_sources.filter_data_sources(source_type="news", bias="neutral")
    assert len(filtered_sources) == 1