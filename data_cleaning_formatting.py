import pandas as pd

# Function to load the flight data and perform data cleaning measures
def load_and_clean_data(filepath) -> pd.DataFrame:
    """
    Loads and cleans the city pair data from a CSV file.
    This function reads a CSV file containing city pair data. It performs cleaning operations
    which include standardizing the case of city names and converting the 'Month' column to
    datetime format. The cleaned data is then returned as a pandas DataFrame.

    Parameters:
    filepath (str): The path to the CSV file.

    Returns:
    pd.DataFrame: The cleaned data as a pandas DataFrame.

    Exceptions:
    - FileNotFoundError: Raised when the specified file is not found at the provided filepath.
    - pd.errors.EmptyDataError: Raised when the file is found but contains no data.
    - Exception: Catches any other exceptions, with the error message printed to the console.

    Examples:
    data = load_and_clean_data('city_pairs.csv')
    This would load data from 'city_pairs.csv' and clean it.

    data = load_and_clean_data('nonexistent_file.csv')
    This would attempt to load data from 'nonexistent_file.csv' and print 'File not found.'
    """

    # Define exceptions to be caught
    file_not_found = FileNotFoundError
    file_is_empty = pd.errors.EmptyDataError

    try:
        
        # Load data from the CSV file into a DataFrame
        data = pd.read_csv(filepath)

        # Standardize the case of city names
        data['City1'] = data['City1'].str.title()
        data['City2'] = data['City2'].str.title()

        # Convert the month column to datetime format
        data['Date'] = pd.to_datetime(data['Month'], format='%b-%y')

        # Return the cleaned DataFrame
        return data

    except file_not_found:
        
        # Print error message if file is not found
        print('File not found.')

    except file_is_empty:
        
        # Print error message if file is empty
        print('File is empty.')

    except Exception as e:
        
        # Print a generic error message for any other exception
        print(f'An error occurred: {e}')
