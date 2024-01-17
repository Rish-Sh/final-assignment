from data_cleaning_formatting import load_and_clean_data

# Loading and Cleaning Australian Domestic Flight
# The 'load_and_clean_data' function is invoked with the path to a CSV file containing australian domestic flight data.
# This function returns a cleaned pandas DataFrame, stored in the "data" variable, ready for analysis and visualization.
data = load_and_clean_data('dom_city_pair.csv')

