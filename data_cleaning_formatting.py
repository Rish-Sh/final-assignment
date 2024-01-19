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
    - If the file 'city_pairs.csv' contains valid data:
    data = load_and_clean_data('city_pairs.csv')
    This would load and clean the data from 'city_pairs.csv', standardizing city names and converting dates.

    - If the file 'nonexistent_file.csv' does not exist:
    data = load_and_clean_data('nonexistent_file.csv')
    This would raise a FileNotFoundError.

    - If the file 'empty_file.csv' exists but is empty:
    data = load_and_clean_data('empty_file.csv')
    This would raise a pd.errors.EmptyDataError.
    """

    # Load data from the CSV file into a DataFrame
    data = pd.read_csv(filepath)

    # Define the empty file error
    file_is_empty = data.empty

    # Check if the file is empty
    if file_is_empty:
        raise pd.errors.EmptyDataError("The file is empty.")

    # Standardize the case of city names
    data['City1'] = data['City1'].str.title()
    data['City2'] = data['City2'].str.title()

    # Convert the month column to datetime format
    data['Date'] = pd.to_datetime(data['Month'], format='%b-%y')

    # Return the cleaned DataFrame
    return data
