import json
import pytest
from variables import BotConfig

@pytest.fixture
def temp_variables_file(tmp_path, monkeypatch):
    # Create a temporary file to simulate variables.json.
    temp_file = tmp_path / "variables.json"
    monkeypatch.setattr("builtins.open", lambda f, mode="r": open(temp_file, mode))
    return temp_file

def test_save_and_load_variables(tmp_path):
    # Use a temporary directory for the test
    variables_path = tmp_path / "variables.json"
    config = BotConfig()
    config.channels_list = ["channel1", "channel2"]
    config.filter_query = "test query"
    config.filter_strength = 4
    config.subscribers = {12345, 67890}
    config.last_message_ids = {"channel1": 10}

    # Save variables
    config.save_variables()
    # Read file directly
    with open("variables.json", "r") as f:
        data = json.load(f)

    assert data["channels_list"] == config.channels_list
    assert data["filter_query"] == config.filter_query
    assert data["filter_strength"] == config.filter_strength
    # Note: subscribers will be saved as a list, so compare sets.
    assert set(data["subscribers"]) == config.subscribers
    assert data["last_message_ids"] == config.last_message_ids

    # Now, create a new instance to load the saved data
    new_config = BotConfig()
    # It should load the same values
    assert new_config.channels_list == config.channels_list
    assert new_config.filter_query == config.filter_query
    assert new_config.filter_strength == config.filter_strength
    assert new_config.subscribers == config.subscribers
    assert new_config.last_message_ids == config.last_message_ids
