import unittest
import pandas as pd
from data_cleaning_formatting import load_and_clean_data


class TestLoadAndCleanData(unittest.TestCase):

    def test_load_and_clean_valid_data(self):
        # Test loading and cleaning data from a valid CSV file
        data = load_and_clean_data('dom_city_pair.csv')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
        self.assertIn('City1', data.columns)
        self.assertIn('City2', data.columns)
        self.assertIn('Date', data.columns)

    def test_file_not_found(self):
        # Test the function with a non-existent file path
        with self.assertRaises(FileNotFoundError):
            load_and_clean_data('nonexistent_file.csv')

    def test_empty_file(self):
        # Test the function with an empty CSV file
        with self.assertRaises(pd.errors.EmptyDataError):
            load_and_clean_data('empty_file.csv')


if __name__ == '__main__':
    unittest.main()

