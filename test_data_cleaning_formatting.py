import unittest
import pandas as pd
from data_cleaning_formatting import load_and_clean_data


class TestLoadAndCleanData(unittest.TestCase):
    """
    Unit tests for the load_and_clean_data function in the data_cleaning_formatting module.

    This test class contains three tests:
    - Testing the function with a valid CSV file.
    - Testing the function's response to a non-existent file.
    - Testing the function's response to an empty file.
    """

    
    def test_load_and_clean_valid_data(self):
        """
        Test loading and cleaning data from a valid CSV file.

        This test ensures that the function correctly reads data from a valid CSV file,
        performs the necessary cleaning operations, and returns a DataFrame with
        specific columns. It checks that the returned object is a DataFrame, is not empty,
        and contains the expected columns.

        Example:
        data = load_and_clean_data('dom_city_pair.csv')
        """
        
        # Test loading and cleaning data from a valid CSV file
        data = load_and_clean_data('dom_city_pair.csv')
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
        self.assertIn('City1', data.columns)
        self.assertIn('City2', data.columns)
        self.assertIn('Date', data.columns)

    
    def test_file_not_found(self):
        """
        Test the function with a non-existent file path.

        This test ensures that the function raises a FileNotFoundError when it tries to
        load data from a file path that does not exist.

        Example:
        with self.assertRaises(FileNotFoundError):
            load_and_clean_data('nonexistent_file.csv')
        """
        
        # Test the function with a non-existent file path
        with self.assertRaises(FileNotFoundError):
            load_and_clean_data('nonexistent_file.csv')

    
    def test_empty_file(self):
        """
        Test the function with an empty CSV file.

        This test ensures that the function raises a pandas.errors.EmptyDataError when it
        tries to load data from an empty CSV file.

        Example:
        with self.assertRaises(pd.errors.EmptyDataError):
            load_and_clean_data('empty_file.csv')
        """
        
        # Test the function with an empty CSV file
        with self.assertRaises(pd.errors.EmptyDataError):
            load_and_clean_data('empty_file.csv')


if __name__ == '__main__':
    unittest.main()

