from data_cleaning_formatting import load_and_clean_data
from matplotlib.backends.backend_tkagg import \
    FigureCanvasTkAgg  # TkAgg backend for embedding matplotlib plots in Tkinter
import matplotlib.pyplot as plt  # Matplotlib for plotting graphs

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
