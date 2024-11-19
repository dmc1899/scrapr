import pytest
import json
import csv
import os
from scrapr.action.persist import write_to_json, write_to_csv

@pytest.fixture
def sample_data():
    return [
        {"name": "John", "age": "30", "city": "New York"},
        {"name": "Alice", "age": "25", "city": "London"}
    ]

@pytest.fixture
def cleanup_files():
    yield
    # Cleanup files after tests
    files_to_remove = ['test_output.json', 'test_output.csv']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)

def test_write_to_json(sample_data, cleanup_files, capsys):
    filename = "test_output.json"
    write_to_json(sample_data, filename)

    # Check if file exists
    assert os.path.exists(filename)

    # Verify file contents
    with open(filename, 'r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data == sample_data

    # Check console output
    captured = capsys.readouterr()
    assert f"Data has been written to {filename} in JSON format." in captured.out

def test_write_to_csv(sample_data, cleanup_files, capsys):
    filename = "test_output.csv"
    write_to_csv(sample_data, filename)

    # Check if file exists
    assert os.path.exists(filename)

    # Verify file contents
    saved_data = []
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            saved_data.append(row)
    assert saved_data == sample_data

    # Check console output
    captured = capsys.readouterr()
    assert f"Data has been written to {filename} in CSV format." in captured.out

def test_write_to_csv_empty_data(cleanup_files, capsys):
    filename = "test_output.csv"
    write_to_csv([], filename)

    # Check that file wasn't created
    assert not os.path.exists(filename)

    # Verify console output
    captured = capsys.readouterr()
    assert "The data list is empty. No CSV file will be created." in captured.out

def test_write_to_json_invalid_path():
    with pytest.raises(OSError):
        write_to_json([{"test": "data"}], "/invalid/path/test.json")

def test_write_to_csv_invalid_path():
    with pytest.raises(OSError):
        write_to_csv([{"test": "data"}], "/invalid/path/test.csv")
