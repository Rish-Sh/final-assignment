from data_cleaning_formatting import load_and_clean_data
from matplotlib.backends.backend_tkagg import \
    FigureCanvasTkAgg  # TkAgg backend for embedding matplotlib plots in Tkinter

# Loading and Cleaning Australian Domestic Flight
# The 'load_and_clean_data' function is invoked with the path to a CSV file containing australian domestic flight data.
# This function returns a cleaned pandas DataFrame, stored in the "data" variable, ready for analysis and visualization.
data = load_and_clean_data('dom_city_pair.csv')

# Function to update the Tkinter canvas 

def update_canvas(fig, canvas):

  # Clear existing children widgets from the canvas, if there are any
  if canvas.children:
    for child in canvas.winfo_children():
      child.destroy()

  # Embed the new figure in the Tkinter canvas and display the canvas 
  figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
  figure_canvas_agg.draw()
  figure_canvas_agg.get_tk_widget().pack(side = 'top', fill = 'both', expand = 1)
  
  
  
