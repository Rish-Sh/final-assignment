from data_cleaning_formatting import load_and_clean_data
from matplotlib.backends.backend_tkagg import \
    FigureCanvasTkAgg  # TkAgg backend for embedding matplotlib plots in Tkinter
import matplotlib.pyplot as plt  # Matplotlib for plotting graphs
import PySimpleGUI as sg  # PySimpleGUI is used for creating the graphical user interface

# Loading and Cleaning Australian Domestic Flight
# The 'load_and_clean_data' function is invoked with the path to a CSV file containing australian domestic flight data.
# This function returns a cleaned pandas DataFrame, stored in the "data" variable, ready for analysis and visualization.
data = load_and_clean_data('dom_city_pair.csv')



# Function to update the Tkinter canvas 
def update_canvas(fig, canvas):
    """
    Updates the specified canvas with a new matplotlib figure.
    
    This function is responsible for updating the Tkinter canvas widget with a new matplotlib figure.
    If the canvas already has any children widgets (previous plots), they are removed before
    updating the canvas with the new figure.
    
    Parameters:
    fig (matplotlib.figure.Figure): The matplotlib figure to display on the canvas.
    canvas (tkinter.Canvas): The Tkinter canvas widget to be updated with the figure.
    """

  # Clear existing children widgets from the canvas, if there are any
  if canvas.children:
    for child in canvas.winfo_children():
      child.destroy()

  # Embed the new figure in the Tkinter canvas and display the canvas 
  figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
  figure_canvas_agg.draw()
  figure_canvas_agg.get_tk_widget().pack(side = 'top', fill = 'both', expand = 1)



# Function to fetch city pair data
def get_city_pair_data(city1, city2):
    """
    Retrieve domestic flight data for a specific pair of cities.
    
    This function searches within the flight dataset 'data' for entries where
    'City1' matches 'city1' and 'City2' matches 'city2'. If no matching data is found,
    the function returns None, otherwise it returns the corresponding data.
    
    Parameters:
    city1 (str): The name of the first city in the city pair.
    city2 (str): The name of the second city in the city pair.
    
    Returns:
    DataFrame or None: The subset of the 'data' DataFrame corresponding to the 
    specified city pair, or None if no data is found for that city pair.
    """

    # Get data for the specific city pair
    city_pair_data = data[(data['City1'] == city1)
                          & (data['City2'] == city2)
                          ]

    # If no data is found for the specified city pair display a popup
    if city_pair_data is None:
        return
    else:
        return city_pair_data



# Function to plot the passenger trips trend of a city pair
def plot_trend(city_pair_data, canvas):
        """
        Plots the passenger trips trend between two cities on a canvas.

        This function takes two city names and a Tkinter canvas, and plots the trend of passenger trips
        between these cities over time. If no data is found for the specified city pair, it displays a popup message.
        The plot is then updated on the provided canvas.

        Parameters:
        city1 (str): Name of the first city in the city pair.
        city2 (str): Name of the second city in the city pair.
        canvas (tkinter.Canvas): The Tkinter canvas widget to display the plot.
        """
    
    # Check if city_pair_data is empty
    if city_pair_data.empty:
        return sg.popup("No data found for the city pair")

    # Fetch the city names from the city_pair_data
    city1 = city_pair_data.iloc[0]['City1']
    city2 = city_pair_data.iloc[0]['City2']

    # Create and format the plot to display the passenger trips trend
    fig = plt.figure(figsize=(5, 4))
    plt.plot(city_pair_data['Date'], city_pair_data['Passenger_Trips'])
    plt.title(f'Passenger Trips Trend for {city1} - {city2}')
    plt.xlabel('Date')
    plt.ylabel('Passenger Trips')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Update the canvas with new plot of the city pair passenger trips trend
    update_canvas(fig, canvas)



# Function to compare two city pairs
def compare_two_city_pairs(pair1, pair2, canvas):
    """
    Compares passenger trips between two pairs of cities and plots the data on a given canvas.

    This function takes two city pairs (each pair consisting of two city names separated by ' - ') and
    a Tkinter canvas.
    It plots the trend of passenger trips for each city pair on the same graph for a comparative visualization.

    Parameters:
    pair1 (str): The first city pair in the format 'City1 - City2'.
    pair2 (str): The second city pair in the format 'City1 - City2'.
    canvas (tkinter.Canvas): The Tkinter canvas widget where the plot will be displayed.
    """
    
    # Set up the figure for plotting
    fig, ax = plt.subplots(figsize=(5, 4))

    # Loop through each city pair and plot their data
    for pair in [pair1, pair2]:
        city1, city2 = pair.split(' - ')

        # Use the get_city_pair_data function to retrieve data for each city pair
        pair_data = get_city_pair_data(city1, city2)

        # Continue only if there is data for the city pair
        if pair_data is not None:
            ax.plot(pair_data['Date'], pair_data['Passenger_Trips'], label=f"{city1} - {city2}")
            
    # Set plot titles and labels
    ax.set_title('Comparison of Passenger Trips Between Two City Pairs')
    ax.set_xlabel('Date')
    ax.set_ylabel('Passenger Trips')
    plt.xticks(rotation=45)
    ax.legend()
    plt.tight_layout()

    # Update the canvas with the new plot of the passenger trips trends of the two city pairs
    update_canvas(fig, canvas)


def analyze_load_factor(city1, city2, canvas):
    """
    Analyze and plot the load factor for a specific city pair.
    Retrieves the data for the given city pair from the global 'data' DataFrame and plots the load factor over time. 
    If no data is found, a popup will alert the user.

    Arguments:

    city1: The first city in the city pair.

    city2: The second city in the city pair.

    canvas: The Tkinter canvas object to update with the plot.

    Results:
        A matplotlib figure will be updated on the canvas showing the trend of load factor over time for the
        specified city pair. The figure includes a line plot with the dates of flights on the x-axis and the
        corresponding load factors on the y-axis. The plot is titled 'Passenger Load Factor for Sydney - Melbourne'
        and includes a legend and appropriate labels for both axes.

    Example:
        analyze_load_factor('Sydney', 'Melbourne', canvas)

        This will query the dataset for flights between Sydney and Melbourne and plot the load factor
        trend on the canvas. The graph will have 'Date' on the x-axis and 'Load Factor (%)' on the y-axis.
        If there are no flights between these cities in the dataset, a popup will appear stating:
        "No data found for the city pair: Sydney - Melbourne."
    """

    # Query the dataset for the specified city pair.

    pair_data = data.query("City1 == @city1 and City2 == @city2")

    # If no data is found for the city pair, display a popup and return early.

    if pair_data.empty:
        popup_message = f"No data found for the city pair: {city1} - {city2}"

        sg.popup(popup_message)

        return

        # Begin plotting the data if it exists.

    fig = plt.figure(figsize=(5, 4))

    plot_dates = pair_data['Date']

    plot_values = pair_data['Passenger_Load_Factor']

    plt.plot(plot_dates, plot_values, label="Passenger Load Factor")

    # Configure plot aesthetics.

    plt.title(f'Passenger Load Factor for {city1} - {city2}')

    plt.xlabel('Date')

    plt.ylabel('Load Factor (%)')

    plt.xticks(rotation=45)

    plt.legend(loc="best")

    plt.grid(True)

    plt.tight_layout()

    # Display the updated plot on the canvas.

    update_canvas(fig, canvas)


# Prepare the list of city pairs from the data for dropdowns or listboxes in the GUI.

city_pairs = [f"{city1} - {city2}" for city1, city2 in zip(data['City1'], data['City2'])]



def calculate_city_stats(city, dataset):
    """
    Calculate and return key statistics for a given city based on the 'dataset'.

    The function computes the total number of trips from the city, the average load factor,
    and the most traveled to city from the given city.

    Arguments:
    city (str): The city to compute statistics for.
    dataset (DataFrame): The DataFrame containing the flight data.

    Returns:
    dict: A dictionary with computed statistics: total number of trips, average load factor,
    and the most traveled to destination city.

    Example:
        Given a DataFrame 'flights_data' with the following columns: ['City1', 'City2', 'Passenger_Load_Factor'],
        if we call calculate_city_stats('New York', flights_data), the function might return:
        {
            'total_trips': 120,
            'avg_load_factor': 78.5,
            'most_traveled_to_city': 'Los Angeles'
        }
        This indicates that from New York, there were 120 trips recorded in the dataset, 
        the average load factor for these trips was 78.5%, and the most common destination city was Los Angeles.
    """
        # Filter the dataset for the selected city.

    city_data = dataset[dataset['City1'] == city]

    # Calculate the total number of trips and the average load factor.

    total_trips = city_data.shape[0]

    avg_load_factor = city_data['Passenger_Load_Factor'].mean() if total_trips > 0 else float('nan')

    # Determine the most traveled to city.

    most_traveled_to_city = (city_data['City2'].mode()[0]

                             if not city_data['City2'].empty

                             else "No data")

    # Construct the results dictionary.

    results = {

        'total_trips': total_trips,

        'avg_load_factor': avg_load_factor,

        'most_traveled_to_city': most_traveled_to_city

    }

    return results


def analyze_distance_vs_load(canvas):
        """
    Plot a hexbin chart to analyze the relationship between flight distance and passenger load factor.

    The hexbin chart uses color coding to represent the density of points in the plot, with each hexagonal 
    bin displaying the count of occurrences within that bin. The plot is created on a Tkinter canvas passed 
    to the function. The function also calculates and displays the Pearson Correlation Coefficient to quantify 
    the linear relationship between distance and load factor.

    Arguments:
    canvas (Canvas): The Tkinter canvas object on which the hexbin chart will be plotted.

    Results:
    The function will render a hexbin chart on the provided canvas object. This chart will visualize the 
    relationship between the great-circle distance of flights and their corresponding passenger load factors, 
    along with an annotation for the correlation coefficient.

    Example:
    Assuming 'data' is a DataFrame that contains two columns: 'Distance_GC_(km)' and 'Passenger_Load_Factor', 
    with each row representing a flight, calling `analyze_distance_vs_load(canvas)` will generate a plot such 
    as the following:

    +--------------------------------------------------------+
    |                                                        |
    |     Distance vs. Passenger Load Factor                 |
    |     Correlation: 0.76                                  |
    |                                                        |
    |     ^                                                  |
    |     |  [Dense area with dark color indicating          |
    |     |   high passenger load factor at various distances]|
    |     |                                                  |
    |     |  [Less dense area with lighter color indicating   |
    |     |   lower load factors at various distances]        |
    |     |                                                  |
    |     +-------------------------------------------------->|
    |       Route Distance (km)                              |
    |                                                        |
    +--------------------------------------------------------+
    """
    
    # Extract the relevant columns from the dataset.
    distance = data['Distance_GC_(km)']
    load_factor = data['Passenger_Load_Factor']

    # Create a new figure for plotting.
    fig, ax = plt.subplots(figsize=(6, 5))

    # Generate the hexbin plot with the data.
    hexbin_plot = ax.hexbin(distance, load_factor, gridsize=50, cmap='viridis')

    # Calculate and annotate the Pearson Correlation Coefficient.
    relevant_data = data[['Distance_GC_(km)', 'Passenger_Load_Factor']]
    correlation = relevant_data.corr(method='pearson').at['Distance_GC_(km)', 'Passenger_Load_Factor']
    correlation_annotation = f'Correlation: {correlation:.2f}'
    ax.annotate(correlation_annotation, xy=(0.5, 1.15), xycoords="axes fraction", ha='center')

    # Set the plot's title and labels.
    ax.set_title('Distance vs. Passenger Load Factor')
    ax.set_xlabel('Route Distance (km)')
    ax.set_ylabel('Passenger Load Factor (%)')

    # Add a color bar to interpret the bin counts.
    color_bar = fig.colorbar(hexbin_plot, ax=ax)
    color_bar.set_label('Count in bin')


    # Display the plot on the canvas.
    update_canvas(fig, canvas)



def filter_most_passenger_trips(data):
    #This function sorts and filters the dtaa to find the top 10 entries

    #Sorting is done in descending order based on the passenger_trips column

    sorted_data = data.sort_values(by ='Passenger_Trips', ascending = False)

    #Next, top 10 rows with the highest passenger trips are retrieved

    top_passenger_trips = sorted_data.head(10)

    return top_passenger_trips



def filter_most_aircraft_trips(data): 

    # This function sorts and filters the data to find the top 10 entries with the most aircraft trips. 
 
    # It sorts the data in descending order based on the 'Aircraft_Trips' column. 

    sorted_data = data.sort_values(by='Aircraft_Trips', ascending=False) 

    # Retrieves the top 10 rows with the highest 'Aircraft_Trips' 

    top_aircraft_trips = sorted_data.head(10) 

    return top_aircraft_trips 



def filter_highest_load_factor(data): 

    # This function sorts and filters the data to find the top 10 entries with the highest passenger load factor. 

    # It sorts the data in descending order based on the 'Passenger_Load_Factor' column. 
 
    sorted_data = data.sort_values(by='Passenger_Load_Factor', ascending=False) 
 
    # Retrieves the top 10 rows with the highest 'Passenger_Load_Factor' 

    highest_load_factor = sorted_data.head(10) 

    return highest_load_factor 



def filter_lowest_load_factor(data): 

    # This function sorts and filters the data to find the top 10 entries with the lowest passenger load factor. 

    # It sorts the data in ascending order based on the 'Passenger_Load_Factor' column. 

    sorted_data = data.sort_values(by='Passenger_Load_Factor', ascending=True) 

    # Retrieves the top 10 rows with the lowest 'Passenger_Load_Factor' 
    
    lowest_load_factor = sorted_data.head(10) 

    return lowest_load_factor 



# Function to create and handle the data exploration window 
def data_exploration_window(): 

    # Define the layout of the window with various UI elements 

    layout = [ 

        # Section for filter options 

        [sg.Text('Filter Options:')], 

        # Input fields for City 1 and City 2 with corresponding labels 

        [sg.Text('City 1:'), sg.InputText(key='-FILTER_CITY1-'), sg.Text('City 2:'), 

         sg.InputText(key='-FILTER_CITY2-')], 

        # Input fields for selecting a date range 

        [sg.Text('Date Range:'), sg.InputText(key='-DATE_START-'), sg.Text('to'), sg.InputText(key='-DATE_END-')], 

        # Buttons for selecting different types of data filters 

        [sg.Button('Most Passenger Trips'), sg.Button('Most Aircraft Trips'), 

         sg.Button('Highest Passenger Load Factor Trips'), sg.Button('Lowest Passenger Load Factor Trips')], 

        # Buttons to apply or reset the selected filters 

        [sg.Button('Apply Filter'), sg.Button('Reset Filter')], 

        # Table to display the data with row numbers and adjustable columns 

        [sg.Table(values=data.values.tolist(), headings=data.columns.tolist(), display_row_numbers=True, 
                  auto_size_columns=False, num_rows=10, key='-TABLE-', enable_click_events=True)], 
        
        # Back button to exit the window 
        
        [sg.Button('Back')] 

    ] 

    
    # Create the window with the specified layout 
    
    window = sg.Window('Data Exploration', layout, finalize=True) 

    # Event loop to handle user interactions 

    while True: 

        event, values = window.read() 

        # Check for window close or 'Back' button events 

        if event in (sg.WIN_CLOSED, 'Back'): 

            break 

        # Handle events for filtering data based on different criteria 
        
        elif event == 'Most Passenger Trips': 
            
            filtered_data = filter_most_passenger_trips(data) 

            window['-TABLE-'].update(values=filtered_data.values.tolist()) 
            

        elif event == 'Most Aircraft Trips': 

            filtered_data = filter_most_aircraft_trips(data) 

            window['-TABLE-'].update(values=filtered_data.values.tolist()) 
            

        elif event == 'Highest Passenger Load Factor Trips': 

            filtered_data = filter_highest_load_factor(data) 

            window['-TABLE-'].update(values=filtered_data.values.tolist()) 
            

        elif event == 'Lowest Passenger Load Factor Trips': 

            filtered_data = filter_lowest_load_factor(data) 

            window['-TABLE-'].update(values=filtered_data.values.tolist()) 
            
            
            # Event to apply custom filters 

        elif event == 'Apply Filter': 

            filtered_data = apply_filters(values) 

            window['-TABLE-'].update(values=filtered_data.values.tolist()) 
            

            # Event to reset the filters and display the original data 

        elif event == 'Reset Filter': 

            window['-TABLE-'].update(values=data.values.tolist()) 
            
            
    # Close the window once the loop is exited 
    window.close()



def apply_filters(values): 

    # Start with the original dataset 

    filtered_data = data 

    # Check if a filter for 'City 1' is applied. 

    # If so, filter the data to include only those entries where 'City1' matches the input value. 

    if values['-FILTER_CITY1-']: 

        filtered_data = filtered_data[filtered_data['City1'] == values['-FILTER_CITY1-']]  
        

    # Check if a filter for 'City 2' is applied. 
    
    # If so, filter the data to include only those entries where 'City2' matches the input value. 

    if values['-FILTER_CITY2-']: 

        filtered_data = filtered_data[filtered_data['City2'] == values['-FILTER_CITY2-']] 
        

    # Check if both start and end dates are provided for filtering.

    # If so, filter the data to include only those entries within the specified date range. 
    
    if values['-DATE_START-'] and values['-DATE_END-']: 

        filtered_data = filtered_data[ 
        
            (filtered_data['Date'] >= values['-DATE_START-']) & 

            (filtered_data['Date'] <= values['-DATE_END-']) 

            ] 

    
    # Return the filtered dataset
    
    return filtered_data 

# Function to create the overall dashboard
def create_dashboard_window():
        """ 
        Creates and returns the main dashboard window for the Australia Domestic Flights Analysis application. 
 
        This function sets up the graphical user interface for the application's main dashboard. It offers 
        several analysis options, each represented by a button, allowing the user to explore different aspects 
        of domestic flight data in Australia. 
 
        The dashboard provides the following options: 
        - Explore Data: To view and explore the dataset. 
        - Show Passenger Trips Trend: To visualize trends in passenger trips. 
        - Compare Passenger Trips Trends of Two City Pairs: To compare trends between two specific city pairs. 
        - Analyze Load Factor of City Pair: To analyze the load factor for a specific city pair. 
        - City Specific Data Summary: To view summary statistics for a specific city. 
        - Distance vs Passenger Load analysis: To analyze the relationship between distance and passenger load. 
        - Exit: To close the application. 
 
        Returns: 
        sg.Window: The main dashboard window of the application with the specified layout and size. 
        """ 
    # Layout definition for the main GUI window
    layout = [
        [sg.Text("Choose an analysis option:")],
        [sg.Button('Explore Data', key='-EXPLORE_DATA-')],
        [sg.Button('Show Passenger Trips Trend', key='-SHOW_TREND-')],
        [sg.Button('Compare Passenger Trips Trends of Two City Pairs', key='-COMPARE_CITY_PAIRS-')],
        [sg.Button('Analyze Load Factor of City Pair', key='-ANALYZE_LOAD_FACTOR-')],
        [sg.Button('City Specific Data Summary', key='-CITY_SUMMARY-')],
        [sg.Button('Distance vs Passenger Load analysis', key='-DIST_VS_LOAD-')],
        [sg.Button('Exit')]
    ]

    # Returns the main dashboard window
    return sg.Window('Australia Domestic Flights Analysis', layout, size=(400, 250))
    
# Function to create and handle the trend analysis window 
def trend_analysis_window(): 
    """
    Creates and manages the passenger trips trend analysis window.

    This function sets up a window for trend analysis where users can enter two city names
    and view the trend of passenger trips between these cities. The window includes input fields
    for the city names, a button to trigger the trend display, and a canvas where the trend plot is shown.

    The function handles the following user interactions:
    - Reading city names from input fields and displaying the trend on the canvas.
    - Showing a popup message if both city names are not entered.
    - Closing the window either when the user clicks 'Back' or closes the window.

    Output:
    If valid city names are entered and the 'Show Trend' button is clicked, the function will
    display a line plot on the canvas showing the trend of passenger trips over time for the
    specified city pair. The plot will have 'Date' on the x-axis and 'Passenger Trips' on the y-axis.
    If the entered cities do not have associated trip data, the user will be notified via a popup message.
    """
    
    # Layout definition for the passenger trips trend analysis GUI window 
    layout = [ 
        [sg.Text("City 1:"), sg.InputText(key='-CITY1-')], 
        [sg.Text("City 2:"), sg.InputText(key='-CITY2-')], 
        [sg.Button('Show Trend')], 
        [sg.Canvas(key='-CANVAS-')], 
        [sg.Button('Back')] 
    ] 
    
    # Create the window with the specified layout 
    window = sg.Window('Show Trend', layout, finalize=True) 
    canvas = window['-CANVAS-'].TKCanvas 
    
    # Event loop for user interaction handling 
    while True: 
        event, values = window.read() 
        
        if event in (sg.WIN_CLOSED, 'Back'): 
            break 
            
        if event == 'Show Trend': 
            city1, city2 = values['-CITY1-'], values['-CITY2-'] 
            
            if city1 and city2: 
                # Plot the trend for the entered city pair 
                plot_trend(get_city_pair_data(city1, city2), canvas) 
                
            else: 
                sg.popup("Please enter both City 1 and City 2.") 
                
    window.close() 

# Function to create and handle the city pair comparison window 
def compare_city_pairs_window(): 
    """
    Creates and manages the window for comparing passenger trips trends between two city pairs.

    This function sets up a window where users can select two city pairs from a list and compare their
    passenger trips trends. The window includes two list boxes for selecting city pairs, a button to trigger
    the comparison, and a canvas where the comparison plot is displayed.

    Parameters:
    city_pairs (list): A list of city pair strings to choose from for comparison.

    The function handles the following user interactions:
    - Selecting city pairs from the list boxes and displaying their comparison on the canvas.
    - Showing a popup message if both city pairs are not selected.
    - Closing the window either when the user clicks 'Back' or closes the window.

    Output/Result:
    Upon successful selection of two city pairs and clicking the 'Compare' button, the function will
    render a plot on the canvas illustrating the comparative trend of passenger trips between the
    selected city pairs. The plot will have 'Date' on the x-axis and 'Passenger Trips' on the y-axis,
    with each city pair represented as a separate line on the graph. This visual comparison allows users
    to easily discern differences and similarities in travel trends between the two city pairs. If the comparison
    cannot be made due to missing data or unselected city pairs, the user will be notified with a popup message.
    """
    
    # Layout definition for the compare two city pairs GUI window  
    layout = [ 
        [sg.Text("Select First City Pair for Comparison:")], 
        [sg.Listbox(city_pairs, select_mode='single', size=(30, 6), key='-CITYPAIR1-')], 
        [sg.Text("Select Second City Pair for Comparison:")], 
        [sg.Listbox(city_pairs, select_mode='single', size=(30, 6), key='-CITYPAIR2-')], 
        [sg.Button('Compare')], 
        [sg.Canvas(key='-CANVAS-')], 
        [sg.Button('Back')] 
    ] 

    # Create the window with the specified layout 
    window = sg.Window('Compare City Pairs', layout, finalize=True) 
    canvas = window['-CANVAS-'].TKCanvas 

 

    # Event loop for user interaction handling 
    while True: 
        event, values = window.read() 
        
        if event in (sg.WIN_CLOSED, 'Back'): 
            break 
            
        if event == 'Compare': 
            # Check if both city pairs are selected 
            if not values['-CITYPAIR1-'] or not values['-CITYPAIR2-']: 
                sg.popup("Please select two city pairs for comparison.") 
                continue 

                # Call function to compare the selected city pairs 
            compare_two_city_pairs(values['-CITYPAIR1-'][0], values['-CITYPAIR2-'][0], canvas) 
            
    window.close() 

# Function to create the load factor analysis window
def load_factor_analysis_window(): 
    """ 
        Create and handle the load factor analysis window. 
        In this window, the user can input two city names (City 1 and City 2) and then trigger an analysis 
        of the load factor between these cities by clicking the 'Analyze Load Factor' button. A graph will be 
        plotted displaying the load factor trend over time on a canvas within the GUI. The user is required 
        to enter valid names for both cities before the analysis can proceed. If either city name is left 
        blank, a message will prompt the user to fill in both fields. 
        The window also contains a 'Back' button to return to the previous menu. 
    
        Example: 
            If the user inputs 'Sydney' for City 1 and 'Melbourne' for City 2 and then clicks the 
            'Analyze Load Factor' button, the function will display a graph showing the trend of load 
            factors for flights between Sydney and Melbourne. 
        """ 

    # Define GUI layout elements 
    layout = [ 
        [sg.Text("Load Factor Analysis")], 
        [sg.Text("City 1:"), sg.InputText(key='-LOAD_CITY1-')], 
        [sg.Text("City 2:"), sg.InputText(key='-LOAD_CITY2-')], 
        [sg.Button('Analyze Load Factor')], 
        [sg.Canvas(key='-CANVAS-')], 
        [sg.Button('Back')] 
    ] 

    # Initialize window with layout 
    window = sg.Window('Load Factor Analysis', layout, finalize=True) 
    canvas = window['-CANVAS-'].TKCanvas 

    # Event processing loop 
    while True: 
        event, values = window.read() 
        # Check for window close or navigation events if program closed then quit the program
        if event in (sg.WIN_CLOSED, 'Back'): 
            break 
        # Analyze load factor upon button click 
        if event == 'Analyze Load Factor': 
            city1, city2 = values['-LOAD_CITY1-'], values['-LOAD_CITY2-'] 
            # Proceed only if both city names are provided 
            if city1 and city2: 
                analyze_load_factor(city1, city2, canvas) 
            else: 
                # Prompt user for missing city names 
                sg.popup("Both City 1 and City 2 are required for load factor analysis.") 
                # Clean up and close the window 

    window.close()

# Function to create the city summary window
def city_summary_window(): 

    # Define the layout of the city summary window 
    layout = [ 
        # Dropdown menu to select a city from the unique cities in the dataset 
        [sg.Text('Select City:'), sg.Combo(data['City1'].unique(), key='-CITY-')], 
        # Buttons for showing the city summary and going back 
        [sg.Button('Show Summary'), sg.Button('Back')] 
    ] 

    # Create the window with the given layout and a title 
    window_title = 'City Specific Data Summary' 
    window = sg.Window(window_title, layout, finalize=True) 

    # Event loop to process user actions 
    while True: 
        # Read the next event and the values entered by the user 
        event, values = window.read() 
        
        # Check if the user wants to close the window or go back 
        if event in (sg.WIN_CLOSED, 'Back'):
            # Exit the loop 
            break 
            
        # Respond to 'Show Summary' button click 
        if event == 'Show Summary': 
            # Extract the chosen city from the user input 
            city_selected = values['-CITY-'] 
            
            # Ensure a city has been selected before proceeding
            if not city_selected:
                # Show a warning popup if no city is selected 
                sg.popup("Please select a city to show the summary.") 
                continue 
                
            # Calculate the statistics for the selected city 
            stats = calculate_city_stats(city_selected, data) 
            
            # Prepare the message to display in the popup 
            total_trips_message = f"Total Trips: {stats['total_trips']}" 
            average_load_message = f"Average Load Factor: {stats['avg_load_factor']:.2f}%" 
            most_traveled_message = f"Most Traveled to City: {stats['most_traveled_to_city']}" 
            summary_message = "\n".join([total_trips_message, 
                                         average_load_message, 
                                         most_traveled_message]) 

            # Display the statistics in a popup window 
            sg.popup(summary_message) 
            
    # Close the window when the loop is exited 
    window.close() 

