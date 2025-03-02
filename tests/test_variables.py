import json
import pytest
from variables import Variables

@pytest.fixture
def temp_variables_file(tmp_path, monkeypatch):
    # Create a temporary file to simulate variables.json.
    temp_file = tmp_path / "variables.json"
    monkeypatch.setattr("builtins.open", lambda f, mode="r": open(temp_file, mode))
    return temp_file

def test_save_and_load_variables(tmp_path):
    # Use a temporary directory for the test
    variables_path = tmp_path / "variables.json"
    vars = Variables()
    vars.channels = ["channel1", "channel2"]
    vars.filter_query = "test query"
    vars.filter_strength = 4
    vars.subscribers = {12345, 67890}
    vars.channels = {"channel1": 10}

    # Save variables
    vars.save_variables()
    # Read file directly
    with open("variables.json", "r") as f:
        data = json.load(f)

    assert data["channels_list"] == vars.channels
    assert data["filter_query"] == vars.filter_query
    assert data["filter_strength"] == vars.filter_strength
    # Note: subscribers will be saved as a list, so compare sets.
    assert set(data["subscribers"]) == vars.subscribers
    assert data["last_message_ids"] == vars.channels

    # Now, create a new instance to load the saved data
    new_config = Variables()
    # It should load the same values
    assert new_config.channels == vars.channels
    assert new_config.filter_query == vars.filter_query
    assert new_config.filter_strength == vars.filter_strength
    assert new_config.subscribers == vars.subscribers
    assert new_config.channels == vars.channels



