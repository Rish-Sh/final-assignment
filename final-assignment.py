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
