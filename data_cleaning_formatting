import pandas as pd


def load_and_clean_data(filepath):
    """
        Loads and cleans the city pair data from a CSV file.

        Parameters:
        filepath (str): The path to the CSV file.

        Returns:
        pd.DataFrame: The cleaned data as a pandas DataFrame.
        """

    file_not_found = FileNotFoundError
    file_is_empty = pd.errors.EmptyDataError

    try:

        data = pd.read_csv(filepath)
        data['City1'] = data['City1'].str.title()
        data['City2'] = data['City2'].str.title()
        data['Date'] = pd.to_datetime(data['Month'], format='%b-%y')

        return data

    except file_not_found:
        print('File not found.')
        return None

    except file_is_empty:
        print('File is empty.')

    except Exception as e:
        print(f'An error occurred: {e}')
        return None
